import json

from django.test import Client, TestCase

from apps.zkp_auth.crypto import ZKPCrypto


class ApiViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_core_home_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_core_dashboard_view(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_zkp_full_auth_flow(self):
        # 1. Register with ZKP public key
        x, y = ZKPCrypto.generate_keypair()
        reg_resp = self.client.post(
            "/api/zkp/register/",
            data=json.dumps({"username": "aminata", "public_key_y": hex(y), "country_code": "SEN"}),
            content_type="application/json",
        )
        self.assertEqual(reg_resp.status_code, 201)

        # 2. Request challenge nonce
        chal_resp = self.client.post(
            "/api/zkp/challenge/", data=json.dumps({"username": "aminata"}), content_type="application/json"
        )
        self.assertEqual(chal_resp.status_code, 200)
        challenge_nonce = chal_resp.json()["challenge_nonce"]

        # 3. Generate and verify proof
        proof = ZKPCrypto.generate_proof(secret_x=x, public_y=y, message=challenge_nonce)
        verify_resp = self.client.post(
            "/api/zkp/verify/",
            data=json.dumps(
                {
                    "username": "aminata",
                    "challenge_nonce": challenge_nonce,
                    "commitment_t": proof["commitment_t"],
                    "response_s": proof["response_s"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(verify_resp.status_code, 200)
        self.assertTrue(verify_resp.json()["success"])

    def test_security_scan_api(self):
        resp = self.client.post(
            "/api/security/scan/",
            data=json.dumps({"content": "password = 'hardcoded_cleartext_secret'\n", "filename": "auth.py"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("sovereignty_score", resp.json())

    def test_ai_review_api(self):
        resp = self.client.post(
            "/api/ai/review/", data=json.dumps({"code": "def run(): pass"}), content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["success"])

    def test_forge_status_api(self):
        resp = self.client.get("/api/forge/status/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("forge_engine", resp.json())
