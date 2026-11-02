"""Tests de durcissement securite (phase 1 du backlog : T-020 a T-051)."""

import json

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.zkp_auth.crypto import ZKPCrypto
from apps.zkp_auth.models import SovereignIdentity, ZKPChallenge

PROTECTED = [
    ("get", "/api/organizations/"),
    ("post", "/api/security/scan/"),
    ("get", "/api/security/audits/"),
    ("get", "/api/security/sarif/"),
    ("post", "/api/ai/review/"),
    ("get", "/api/forge/repositories/"),
    ("get", "/api/forge/sync/"),
]


def make_identity(username="alice"):
    x, y = ZKPCrypto.generate_keypair(f"seed-{username}")
    user = User.objects.create_user(username=username)
    SovereignIdentity.objects.create(user=user, public_key_y=hex(y), country_code="CIV", is_verified=True)
    return user, x, y


class AnonymousAccessTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_protected_routes_reject_anonymous(self):
        for method, url in PROTECTED:
            with self.subTest(url=url):
                resp = (
                    getattr(self.client, method)(url, {}, format="json") if method == "post" else self.client.get(url)
                )
                self.assertIn(resp.status_code, (401, 403))

    def test_public_routes_remain_open(self):
        self.assertEqual(self.client.get("/api/ai/status/").status_code, 200)
        self.assertEqual(self.client.get("/api/forge/status/").status_code, 200)

    def test_basic_auth_is_disabled(self):
        import base64

        User.objects.create_user(username="bob", password="Str0ng-pass-123")
        token = base64.b64encode(b"bob:Str0ng-pass-123").decode()
        resp = self.client.get("/api/security/audits/", HTTP_AUTHORIZATION=f"Basic {token}")
        self.assertIn(resp.status_code, (401, 403))

    def test_org_creation_requires_admin(self):
        user = User.objects.create_user(username="plain")
        self.client.force_authenticate(user)
        resp = self.client.post("/api/organizations/", {"name": "X", "slug": "x"}, format="json")
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(self.client.get("/api/organizations/").status_code, 200)


class ChallengeConsumptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, self.x, self.y = make_identity()

    def _proof(self, nonce):
        return ZKPCrypto.generate_proof(self.x, self.y, nonce)

    def test_token_issuance_consumes_challenge_and_blocks_replay(self):
        chal = ZKPChallenge.create_challenge(self.user)
        proof = self._proof(chal.challenge_nonce)
        body = {
            "username": "alice",
            "challenge_nonce": chal.challenge_nonce,
            "commitment_t": proof["commitment_t"],
            "response_s": proof["response_s"],
        }
        first = self.client.post("/api/zkp/tokens/generate/", body, format="json")
        self.assertEqual(first.status_code, 201)
        replay = self.client.post("/api/zkp/tokens/generate/", body, format="json")
        self.assertEqual(replay.status_code, 401)

    def test_token_issuance_rejects_unknown_nonce(self):
        proof = self._proof("nonce-jamais-emis")
        body = {
            "username": "alice",
            "challenge_nonce": "nonce-jamais-emis",
            "commitment_t": proof["commitment_t"],
            "response_s": proof["response_s"],
        }
        self.assertEqual(self.client.post("/api/zkp/tokens/generate/", body, format="json").status_code, 401)

    def test_token_parameters_are_validated(self):
        chal = ZKPChallenge.create_challenge(self.user)
        proof = self._proof(chal.challenge_nonce)
        base = {
            "username": "alice",
            "challenge_nonce": chal.challenge_nonce,
            "commitment_t": proof["commitment_t"],
            "response_s": proof["response_s"],
        }
        for extra in ({"permissions": "root"}, {"validity_days": 99999}, {"validity_days": "abc"}, {"name": "n" * 101}):
            with self.subTest(extra=extra):
                resp = self.client.post("/api/zkp/tokens/generate/", {**base, **extra}, format="json")
                self.assertEqual(resp.status_code, 400)

    def test_verify_rejects_oversized_or_non_string_params(self):
        for body in (
            {"username": "alice", "challenge_nonce": "a", "commitment_t": "f" * 5000, "response_s": "1"},
            {"username": "alice", "challenge_nonce": "a", "commitment_t": 5, "response_s": "1"},
        ):
            resp = self.client.post("/api/zkp/verify/", body, format="json")
            self.assertEqual(resp.status_code, 400)

    def test_verify_challenge_cannot_be_used_twice(self):
        chal = ZKPChallenge.create_challenge(self.user)
        proof = self._proof(chal.challenge_nonce)
        body = {
            "username": "alice",
            "challenge_nonce": chal.challenge_nonce,
            "commitment_t": proof["commitment_t"],
            "response_s": proof["response_s"],
        }
        self.assertEqual(self.client.post("/api/zkp/verify/", body, format="json").status_code, 200)
        self.assertEqual(self.client.post("/api/zkp/verify/", body, format="json").status_code, 401)


class RegistrationValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        _, self.y = ZKPCrypto.generate_keypair("reg-seed")

    def test_invalid_username_rejected(self):
        for name in ("ab", "bad name", "x" * 40, "<script>", 123):
            with self.subTest(name=name):
                resp = self.client.post(
                    "/api/zkp/register/", {"username": name, "public_key_y": hex(self.y)}, format="json"
                )
                self.assertEqual(resp.status_code, 400)

    def test_invalid_country_rejected(self):
        resp = self.client.post(
            "/api/zkp/register/",
            {"username": "carol", "public_key_y": hex(self.y), "country_code": "ci"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_oversized_public_key_rejected(self):
        resp = self.client.post("/api/zkp/register/", {"username": "dave", "public_key_y": "f" * 5000}, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_valid_registration_still_works(self):
        resp = self.client.post(
            "/api/zkp/register/",
            {"username": "erin_01", "public_key_y": hex(self.y), "country_code": "SEN"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)


class AIHardeningTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(User.objects.create_user(username="dev"))

    def test_oversized_code_rejected(self):
        resp = self.client.post("/api/ai/review/", {"code": "a" * 20001}, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_secrets_masked_in_interaction_log(self):
        from apps.ai_assistant.models import AIInteractionLog

        self.client.post("/api/ai/review/", {"code": "api_key = 'ghp_secret_token_123456789012345678'"}, format="json")
        log = AIInteractionLog.objects.latest("id")
        self.assertNotIn("ghp_secret", log.prompt_snippet)

    def test_stream_error_does_not_leak_details(self):
        from unittest import mock

        with mock.patch("apps.ai_assistant.views.GemmaAssistant") as assistant:
            assistant.return_value.stream_analyze_code.side_effect = RuntimeError("secret-internal-path")
            resp = self.client.post("/api/ai/review/", {"code": "x = 1", "stream": True}, format="json")
            content = b"".join(resp.streaming_content).decode()
        self.assertNotIn("secret-internal-path", content)
        self.assertIn("Erreur interne", content)


class WebhookTests(TestCase):
    @override_settings(GITEA_WEBHOOK_SECRET="")
    def test_webhook_disabled_without_secret(self):
        resp = APIClient().post(
            "/api/forge/webhook/", json.dumps({}), content_type="application/json", HTTP_X_GITEA_SIGNATURE="abc"
        )
        self.assertEqual(resp.status_code, 503)


class SettingsHardeningTests(TestCase):
    def test_security_defaults(self):
        from django.conf import settings

        perms = settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]
        self.assertEqual(perms, ["rest_framework.permissions.IsAuthenticated"])
        self.assertNotIn("*", settings.ALLOWED_HOSTS)
        self.assertNotIn(
            "rest_framework.authentication.BasicAuthentication",
            settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"],
        )
    def test_cyclonedx_sbom_generation_and_schema(self):
        """T-SBM-1101 & T-SBM-1103 : Verification du format CycloneDX v1.5 et Package URLs."""
        import tempfile
        from pathlib import Path
        from scripts.generate_sovereign_sbom import generate_cyclonedx_sbom

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            sample_req = tmp_path / "requirements.txt"
            sample_req.write_text("django==5.2.18\ndjangorestframework==3.15.2\n", encoding="utf-8")
            out_file = tmp_path / "bom.cyclonedx.json"

            sbom = generate_cyclonedx_sbom(tmp_path, out_file)
            self.assertEqual(sbom["bomFormat"], "CycloneDX")
            self.assertEqual(sbom["specVersion"], "1.5")
            self.assertGreaterEqual(len(sbom["components"]), 2)
            self.assertEqual(sbom["components"][0]["name"], "django")
            self.assertIn("pkg:pypi/django@5.2.18", sbom["components"][0]["purl"])

