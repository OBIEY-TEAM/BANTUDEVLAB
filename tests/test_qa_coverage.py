"""
QA-03: Tests Additionnels de Couverture Exhaustive (> 95%) pour BANTUDEVLAB.
Cible les branches de code manquantes dans apps/zkp_auth, apps/security_scanner, apps/ai_assistant.
"""

from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, TestCase
from django.utils import timezone

from apps.ai_assistant.gemma import GemmaAssistant
from apps.ai_assistant.models import AIInteractionLog
from apps.security_scanner.models import SecurityAuditReport
from apps.zkp_auth.crypto import P, ZKPCrypto
from apps.zkp_auth.models import GitAccessToken, SovereignIdentity
from apps.zkp_auth.tokens import GitTokenService


class QACoverageExhaustiveTestCase(TestCase):
    """Couverture exhaustive pour atteindre > 95% sur les 3 modules cibles."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(username="coverage_user", email="cov@bantudevlab.africa")
        self.x, self.y = ZKPCrypto.generate_keypair("seed_coverage_test")
        self.identity = SovereignIdentity.objects.create(
            user=self.user, public_key_y=hex(self.y), country_code="CIV", is_verified=True
        )

    # -------------------------------------------------------------
    # 1. apps/ai_assistant (models, gemma live inference, views errors)
    # -------------------------------------------------------------
    def test_ai_assistant_models_and_gemma_live_inference(self):
        # AIInteractionLog __str__
        log_entry = AIInteractionLog.objects.create(
            query_context="code_review",
            prompt_snippet="test prompt",
            ai_response="test response",
            model_used="gemma:5b",
        )
        self.assertIn("code_review", str(log_entry))

        # Gemma live inference (status 200)
        assistant = GemmaAssistant()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"response": "Analyse réussie par Gemma 5B"}
        with patch("requests.post", return_value=mock_resp):
            res = assistant.analyze_code("print('hello')", context="review")
            self.assertTrue(res["success"])
            self.assertEqual(res["mode"], "live_inference")
            self.assertEqual(res["response"], "Analyse réussie par Gemma 5B")

        # Gemma live streaming (status 200)
        mock_stream_resp = MagicMock()
        mock_stream_resp.status_code = 200
        mock_stream_resp.iter_lines.return_value = [
            b'{"response": "Mot1", "done": false}',
            b'{"response": " Mot2", "done": true}',
        ]
        with patch("requests.post", return_value=mock_stream_resp):
            stream_tokens = list(assistant.stream_analyze_code("print('hello')"))
            self.assertIn("Mot1", stream_tokens)
            self.assertIn(" Mot2", stream_tokens)

    def test_ai_assistant_views_edge_cases(self):
        # Missing code in review view
        res = self.client.post("/api/ai/review/", {}, content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("code snippet requis", res.json()["error"])

        # Non-streaming review view with fallback rules (SQL injection + secrets)
        code_with_rules = "cursor.execute('SELECT * FROM ' + table)\napi_token = 'my_secret_token'"
        res_sync = self.client.post(
            "/api/ai/review/", {"code": code_with_rules, "stream": False}, content_type="application/json"
        )
        self.assertEqual(res_sync.status_code, 200)
        self.assertTrue(res_sync.json()["success"])
        self.assertIn("Vulnérabilité SQL", res_sync.json()["response"])

        # Test streaming exception handling
        with patch.object(GemmaAssistant, "stream_analyze_code", side_effect=RuntimeError("Streaming error")):
            res_stream_err = self.client.post(
                "/api/ai/review/", {"code": "print('hello')", "stream": True}, content_type="application/json"
            )
            self.assertEqual(res_stream_err.status_code, 200)
            content = b"".join(res_stream_err.streaming_content).decode("utf-8")
            self.assertNotIn("Streaming error", content)  # SEC-043: pas de fuite de detail interne
            self.assertIn("Erreur interne", content)

        # GET method without code param
        res_get_err = self.client.get("/api/ai/review/")
        self.assertEqual(res_get_err.status_code, 400)

        # Gemma status view
        res_status = self.client.get("/api/ai/status/")
        self.assertEqual(res_status.status_code, 200)

    # -------------------------------------------------------------
    # 2. apps/security_scanner (models, views history & sarif, engine)
    # -------------------------------------------------------------
    def test_security_scanner_models_and_views(self):
        report = SecurityAuditReport.objects.create(
            repository_name="cov-repo",
            file_scanned="main.py",
            total_issues=0,
            critical_count=0,
            high_count=0,
            medium_count=0,
            sovereignty_score=100,
            status_rating="EXCELLENT",
            raw_findings=[],
        )
        self.assertIn("cov-repo", str(report))

        # Missing content in ScanCodeView
        res = self.client.post("/api/security/scan/", {}, content_type="application/json")
        self.assertEqual(res.status_code, 400)

        # SecurityAuditHistoryView
        res_history = self.client.get("/api/security/audits/")
        self.assertEqual(res_history.status_code, 200)
        self.assertTrue(len(res_history.json()["audits"]) >= 1)

        # SARIF Export View (by ID and not found)
        res_sarif = self.client.get(f"/api/security/audits/{report.id}/sarif/")
        self.assertEqual(res_sarif.status_code, 200)
        self.assertEqual(res_sarif.json()["version"], "2.1.0")

        res_sarif_404 = self.client.get("/api/security/audits/999999/sarif/")
        self.assertEqual(res_sarif_404.status_code, 404)

        # SARIF Export View when no reports exist
        SecurityAuditReport.objects.all().delete()
        res_sarif_empty = self.client.get("/api/security/sarif/")
        self.assertEqual(res_sarif_empty.status_code, 404)

    # -------------------------------------------------------------
    # 3. apps/zkp_auth (crypto, models, tokens, views)
    # -------------------------------------------------------------
    def test_zkp_auth_models_and_str(self):
        # SovereignIdentity __str__
        self.assertIn("coverage_user", str(self.identity))

        # GitAccessToken __str__ and is_valid
        raw_tok = GitTokenService.generate_token_raw()
        tok = GitAccessToken.objects.create(
            user=self.user,
            name="Test Token",
            token_prefix=raw_tok[:12],
            token_hash=GitTokenService.hash_token(raw_tok),
            permissions="read",
            expires_at=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
        )
        self.assertIn("Test Token", str(tok))
        self.assertTrue(tok.is_valid())

        # Inactive token is_valid
        tok.is_active = False
        self.assertFalse(tok.is_valid())

        # Expired token is_valid
        tok.is_active = True
        tok.expires_at = timezone.now() - timezone.timedelta(days=1)
        self.assertFalse(tok.is_valid())

        # Test hash_to_int with bytes and arbitrary objects
        val_bytes = ZKPCrypto.hash_to_int(b"some_bytes", 12345, ["list_item"])
        self.assertIsInstance(val_bytes, int)

        # Test verify_proof with invalid subgroup public key
        invalid_pub_key = P - 1
        proof_sample = {"commitment_t": "0x123", "response_s": "0x456", "message": "msg"}
        self.assertFalse(ZKPCrypto.verify_proof(invalid_pub_key, proof_sample))

    def test_zkp_auth_tokens_and_views_branches(self):
        # Issue token for non-existent user
        res_tok = GitTokenService.issue_token_with_zkp(
            username="non_existent", challenge_nonce="nonce", commitment_t="0x123", response_s="0x456"
        )
        self.assertFalse(res_tok["success"])

        # Validate non-existent token format
        res_val1 = GitTokenService.validate_token("invalid_prefix_123")
        self.assertFalse(res_val1["valid"])

        # Validate valid prefix but non-existent token
        res_val2 = GitTokenService.validate_token("bnt_git_" + "0" * 40)
        self.assertFalse(res_val2["valid"])

        # ZKP Register View errors
        res_reg1 = self.client.post("/api/zkp/register/", {}, content_type="application/json")
        self.assertEqual(res_reg1.status_code, 400)

        res_reg2 = self.client.post(
            "/api/zkp/register/",
            {"username": self.user.username, "public_key_y": hex(self.y)},
            content_type="application/json",
        )
        self.assertEqual(res_reg2.status_code, 400)

        res_reg3 = self.client.post(
            "/api/zkp/register/", {"username": "new_user", "public_key_y": "not_hex"}, content_type="application/json"
        )
        self.assertEqual(res_reg3.status_code, 400)

        # ZKP Challenge View missing username
        res_chal = self.client.post("/api/zkp/challenge/", {}, content_type="application/json")
        self.assertEqual(res_chal.status_code, 400)

        # ZKP Verify View incomplete params
        res_ver1 = self.client.post("/api/zkp/verify/", {"username": "abc"}, content_type="application/json")
        self.assertEqual(res_ver1.status_code, 400)

        # ZKP Verify View non-existent challenge or user
        res_ver2 = self.client.post(
            "/api/zkp/verify/",
            {
                "username": "non_existent_usr",
                "challenge_nonce": "non_existent_nonce",
                "commitment_t": "0x123",
                "response_s": "0x456",
            },
            content_type="application/json",
        )
        self.assertEqual(res_ver2.status_code, 401)

        # GitTokenGenerateView missing params
        res_gen = self.client.post("/api/zkp/tokens/generate/", {}, content_type="application/json")
        self.assertEqual(res_gen.status_code, 400)

        # GitTokenValidateView missing token
        res_val_view = self.client.post("/api/zkp/tokens/validate/", {}, content_type="application/json")
        self.assertEqual(res_val_view.status_code, 400)

    # -------------------------------------------------------------
    # 4. finetuning/export_gguf (SOUV-04)
    # -------------------------------------------------------------
    def test_finetuning_export_gguf_tool(self):
        import os
        import tempfile

        from finetuning.export_gguf import export_to_gguf

        # Dry run execution
        res_dry = export_to_gguf(
            weights_dir="finetuning/lora_gemma_weights",
            output_path="finetuning/test_model.gguf",
            quantization="q4_k_m",
            dry_run=True,
        )
        self.assertEqual(res_dry, 0)

        # Actual file generation
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = f"{tmpdir}/output_model.gguf"
            res_actual = export_to_gguf(
                weights_dir=f"{tmpdir}/weights",
                output_path=out_path,
                quantization="q4_k_m",
                dry_run=False,
            )
            self.assertEqual(res_actual, 0)
            self.assertTrue(os.path.exists(out_path))
            with open(out_path, "rb") as f:
                header = f.read(4)
                self.assertEqual(header, b"GGUF")
