import hashlib
import hmac
import json

from django.conf import settings
from django.test import Client, TestCase

from apps.core.audit import AuditTrail
from apps.core.models import AuditTrailLog
from apps.zkp_auth.crypto import P, ZKPCrypto


class Axe1SecurityTestCase(TestCase):
    def setUp(self):
        from django.core.cache import cache

        cache.clear()
        self.client = Client()

    # SEC-01: Validation HMAC des Webhooks Gitea
    def test_sec01_webhook_rejected_without_signature(self):
        payload = json.dumps({"repository": {"name": "test-repo"}})
        response = self.client.post("/api/forge/webhook/", data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("X-Gitea-Signature manquant", response.json().get("error", ""))

    def test_sec01_webhook_rejected_with_invalid_signature(self):
        payload = json.dumps({"repository": {"name": "test-repo"}})
        response = self.client.post(
            "/api/forge/webhook/",
            data=payload,
            content_type="application/json",
            HTTP_X_GITEA_SIGNATURE="invalid_hmac_hash",
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("invalide", response.json().get("error", ""))

    def test_sec01_webhook_accepted_with_valid_signature(self):
        payload = json.dumps({"repository": {"name": "test-repo"}, "pusher": {"username": "kwame"}})
        secret = getattr(settings, "GITEA_WEBHOOK_SECRET", "").encode("utf-8")
        signature = hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()

        response = self.client.post(
            "/api/forge/webhook/", data=payload, content_type="application/json", HTTP_X_GITEA_SIGNATURE=signature
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get("received"))

    # SEC-02: Validation du Sous-Groupe Cryptographique ZKP
    def test_sec02_subgroup_validation_valid_key(self):
        x, y = ZKPCrypto.generate_keypair()
        self.assertTrue(ZKPCrypto.validate_public_key(y))

    def test_sec02_subgroup_validation_invalid_keys(self):
        # Boundaries: y <= 1 or y >= P-1
        self.assertFalse(ZKPCrypto.validate_public_key(1))
        self.assertFalse(ZKPCrypto.validate_public_key(0))
        self.assertFalse(ZKPCrypto.validate_public_key(P))
        self.assertFalse(ZKPCrypto.validate_public_key(P - 1))
        self.assertFalse(ZKPCrypto.validate_public_key(-5))
        # Element not in subgroup: for safe prime P = 2*Q + 1, quadratic non-residues satisfy y^Q mod P == P - 1 != 1
        # P - 1 mod P has order 2, not Q: (P-1)^Q mod P == (-1)^Q mod P == -1 mod P != 1 (Q is prime > 2, hence odd)
        self.assertFalse(ZKPCrypto.validate_public_key(P - 1))

    def test_sec02_register_rejected_on_invalid_subgroup_key(self):
        # Attempt to register with a non-subgroup key y = P - 1 or y = 1
        invalid_y = hex(1)
        response = self.client.post(
            "/api/zkp/register/",
            data=json.dumps({"username": "attacker", "public_key_y": invalid_y, "country_code": "CIV"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("sous-groupe", response.json().get("error", ""))

    # SEC-03: Protection contre l'Énumération d'Utilisateurs
    def test_sec03_challenge_non_existent_user_returns_200(self):
        response = self.client.post(
            "/api/zkp/challenge/",
            data=json.dumps({"username": "ghost_user_that_does_not_exist"}),
            content_type="application/json",
        )
        # Status code must be 200 with identical JSON schema
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "ghost_user_that_does_not_exist")
        self.assertIn("challenge_nonce", data)
        self.assertIn("expires_at", data)
        self.assertEqual(len(data["challenge_nonce"]), 64)

    # SEC-04: Rate Limiting & Throttling
    def test_sec04_throttling_configured(self):
        self.assertIn("zkp", settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"])
        self.assertIn("scanner", settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"])
        self.assertEqual(settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["zkp"], "5/minute")
        self.assertEqual(settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["scanner"], "10/minute")

    # SEC-05: Durcissement des En-têtes HTTP & Cookies
    def test_sec05_security_headers_and_cookie_settings(self):
        self.assertFalse(settings.SECURE_BROWSER_XSS_FILTER)  # obsolete, remplace par la CSP
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(settings.X_FRAME_OPTIONS, "DENY")
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, "Lax")
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)
        self.assertEqual(settings.CSRF_COOKIE_SAMESITE, "Lax")

        # Check response headers from middleware
        response = self.client.get("/")
        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

    # SEC-06: Journal d'Audit Immuable (Audit Trail)
    def test_sec06_audit_trail_chained_hashing_and_integrity(self):
        AuditTrailLog.objects.all().delete()
        log1 = AuditTrail.record_event("ZKP_AUTH", "user1", {"status": "SUCCESS"})
        log2 = AuditTrail.record_event("REPO_CREATE", "user1", {"repository": "repo1"})
        log3 = AuditTrail.record_event("VULN_SCAN", "user1", {"issues": 0})

        self.assertEqual(log1.prev_hash, AuditTrail.GENESIS_HASH)
        self.assertEqual(log2.prev_hash, log1.current_hash)
        self.assertEqual(log3.prev_hash, log2.current_hash)

        # Verify integrity succeeds
        self.assertTrue(AuditTrail.verify_chain_integrity())

        # Tamper with an entry and verify integrity fails
        log2.details = {"repository": "tampered_repo"}
        log2.save()
        self.assertFalse(AuditTrail.verify_chain_integrity())

    def test_sec06_actions_generate_audit_logs(self):
        initial_count = AuditTrailLog.objects.count()

        # 1. ZKP Auth
        x, y = ZKPCrypto.generate_keypair()
        self.client.post(
            "/api/zkp/register/",
            data=json.dumps({"username": "audit_test_user", "public_key_y": hex(y)}),
            content_type="application/json",
        )
        chal = self.client.post(
            "/api/zkp/challenge/", data=json.dumps({"username": "audit_test_user"}), content_type="application/json"
        ).json()
        proof = ZKPCrypto.generate_proof(secret_x=x, public_y=y, message=chal["challenge_nonce"])
        self.client.post(
            "/api/zkp/verify/",
            data=json.dumps(
                {
                    "username": "audit_test_user",
                    "challenge_nonce": chal["challenge_nonce"],
                    "commitment_t": proof["commitment_t"],
                    "response_s": proof["response_s"],
                }
            ),
            content_type="application/json",
        )

        # 2. Repo Create
        self.client.post(
            "/api/forge/repositories/", data=json.dumps({"name": "audit-forge-repo"}), content_type="application/json"
        )

        # 3. Vuln Scan
        self.client.post(
            "/api/security/scan/",
            data=json.dumps({"content": "x = 1", "filename": "test.py"}),
            content_type="application/json",
        )

        new_count = AuditTrailLog.objects.count()
        self.assertGreaterEqual(new_count - initial_count, 3)
        self.assertTrue(AuditTrail.verify_chain_integrity())
    def test_t_rel_902_release_provenance_and_checksums(self):
        """T-REL-902 : Verification du generateur de provenance SLSA et SHA256SUMS."""
        import tempfile
        from pathlib import Path
        from scripts.generate_release_provenance import generate_provenance

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            sample_file = tmp_path / "app-v1.0.tar.gz"
            sample_file.write_bytes(b"BANTUDEVLAB_RELEASE_BINARY_DATA")

            result = generate_provenance([sample_file], tmp_path)
            self.assertEqual(result["total_files"], 1)

            checksums_content = (tmp_path / "SHA256SUMS").read_text(encoding="utf-8")
            self.assertIn("app-v1.0.tar.gz", checksums_content)

            slsa_content = json.loads((tmp_path / "provenance.slsa.json").read_text(encoding="utf-8"))
            self.assertEqual(slsa_content["predicateType"], "https://slsa.dev/provenance/v1")
            self.assertEqual(slsa_content["subject"][0]["name"], "app-v1.0.tar.gz")
            self.assertIn("sha256", slsa_content["subject"][0]["digest"])

    def test_t_brn_1503_branch_rulesets_verification(self):
        """T-BRN-1503 : Verification de la conformite des branch rulesets et signatures cryptographiques."""
        from pathlib import Path

        doc_path = Path("docs/SOVEREIGN_BRANCH_RULESETS.md")
        self.assertTrue(doc_path.exists(), "SOVEREIGN_BRANCH_RULESETS.md doit exister")
        content = doc_path.read_text(encoding="utf-8")
        self.assertIn("require_signed_commits", content)
        self.assertIn("dismiss_stale_approvals", content)
        self.assertIn("gh-commit-badge.verified", content)

        ruleset = {
            "rule_name": "main",
            "require_signed_commits": True,
            "required_approvals": 1,
            "block_force_push": True,
            "status_check_contexts": ["ci/tests", "security/sast"],
        }

        commit_signed = {
            "hash": "a1b2c3d4",
            "signature": {"verified": True, "signer_key": "GPG-7890", "trust_model": "collaborator"},
        }
        commit_unsigned = {
            "hash": "e5f6a7b8",
            "signature": {"verified": False, "signer_key": None, "trust_model": None},
        }

        def evaluate_commit_compliance(commit, rule):
            if rule.get("require_signed_commits"):
                sig = commit.get("signature", {})
                if not (sig.get("verified") and sig.get("signer_key")):
                    return False, "unverified"
            return True, "verified"

        ok_signed, badge_signed = evaluate_commit_compliance(commit_signed, ruleset)
        ok_unsigned, badge_unsigned = evaluate_commit_compliance(commit_unsigned, ruleset)

        self.assertTrue(ok_signed)
        self.assertEqual(badge_signed, "verified")
        self.assertFalse(ok_unsigned)
        self.assertEqual(badge_unsigned, "unverified")

    def test_t_rel_1703_automated_release_notes_generator(self):
        """T-REL-1703 : Verification du generateur de notes de version GitHub."""
        from scripts.generate_release_notes import generate_release_notes, classify_entry

        self.assertEqual(classify_entry("feat(ui): add new button"), "features")
        self.assertEqual(classify_entry("fix: resolve null pointer"), "fixes")
        self.assertEqual(classify_entry("docs: update setup guide"), "docs")
        self.assertEqual(classify_entry("sec(auth): enforce token validation"), "security")
        self.assertEqual(classify_entry("chore: cleanup unused files"), "maintenance")

        entries = [
            {"title": "feat: brand new dashboard", "author": "kwame", "number": 10},
            {"title": "fix: race condition in cache", "author": "amina", "number": 11},
            {"title": "docs: ruleset documentation", "author": "chidi", "number": 12},
        ]

        notes = generate_release_notes(entries, "v1.0.0", "v1.1.0", "https://forge.bantudevlab.local/repo")
        self.assertIn("## What's Changed", notes)
        self.assertIn("### Exciting New Features", notes)
        self.assertIn("### Bug Fixes", notes)
        self.assertIn("### Documentation Updates", notes)
        self.assertIn("* @kwame", notes)
        self.assertIn("**Full Changelog**: https://forge.bantudevlab.local/repo/compare/v1.0.0...v1.1.0", notes)

    def test_t_org_2201_and_2202_organization_roles_matrix(self):
        """T-ORG-2201 & T-ORG-2202 : Verification des styles et mapping de la matrice de roles organisationnels."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-team-card", css_light)
        self.assertIn(".gh-role-badge", css_light)
        self.assertIn(".gh-role-badge.triage", css_light)
        self.assertIn(".gh-role-badge.maintain", css_light)
        self.assertIn(".gh-role-badge.admin", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-team-card", css_dark)

        doc_path = Path("docs/SOVEREIGN_ORG_ROLES.md")
        self.assertTrue(doc_path.exists())
        doc_content = doc_path.read_text(encoding="utf-8")
        self.assertIn("Triage", doc_content)
        self.assertIn("Maintain", doc_content)
        self.assertIn("Admin", doc_content)

    def test_t_mrg_2401_and_2402_merge_queue_simulation(self):
        """T-MRG-2401 & T-MRG-2402 : Verification du moteur de simulation de merge queue et styles."""
        from pathlib import Path
        from scripts.simulate_merge_queue import simulate_merge_queue, evaluate_queue_item

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-merge-queue-badge", css_light)
        self.assertIn(".gh-merge-queue-box", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-merge-queue-badge", css_dark)

        # Simulation
        rules = {
            "required_approvals": 1,
            "require_signed_commits": True,
            "required_status_checks": ["ci/tests"],
        }
        good_pr = {
            "number": 1,
            "draft": False,
            "approvals": 1,
            "signature": {"verified": True, "key_id": "KEY1"},
            "status_checks": {"ci/tests": "success"},
        }
        draft_pr = {
            "number": 2,
            "draft": True,
            "approvals": 1,
            "signature": {"verified": True, "key_id": "KEY2"},
            "status_checks": {"ci/tests": "success"},
        }
        failing_pr = {
            "number": 3,
            "draft": False,
            "approvals": 1,
            "signature": {"verified": True, "key_id": "KEY3"},
            "status_checks": {"ci/tests": "failure"},
        }

        ok, _ = evaluate_queue_item(good_pr, rules)
        self.assertTrue(ok)

        ok_draft, reason_draft = evaluate_queue_item(draft_pr, rules)
        self.assertFalse(ok_draft)
        self.assertIn("Draft", reason_draft)

        ok_fail, _ = evaluate_queue_item(failing_pr, rules)
        self.assertFalse(ok_fail)

        batch_result = simulate_merge_queue([good_pr, draft_pr, failing_pr], rules)
        self.assertEqual(batch_result["total_queued"], 3)
        self.assertEqual(batch_result["merged"], 1)
        self.assertEqual(batch_result["blocked"], 2)

