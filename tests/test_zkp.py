from django.contrib.auth.models import User
from django.test import Client, TestCase

from apps.zkp_auth.crypto import G, P, Q, ZKPCrypto
from apps.zkp_auth.models import SovereignIdentity


class ZKPCryptoTestCase(TestCase):
    def test_keypair_generation(self):
        """Vérifie la génération de la paire de clés (x, y)"""
        x, y = ZKPCrypto.generate_keypair()
        self.assertGreater(x, 0)
        self.assertLess(x, Q)
        self.assertEqual(pow(G, x, P), y)

    def test_deterministic_keypair_generation(self):
        """Vérifie que la graine souveraine dérive la même paire de clés"""
        x1, y1 = ZKPCrypto.generate_keypair(secret_seed="sovereign_africa_seed")
        x2, y2 = ZKPCrypto.generate_keypair(secret_seed="sovereign_africa_seed")
        self.assertEqual(x1, x2)
        self.assertEqual(y1, y2)

    def test_valid_zkp_proof_verification(self):
        """Vérifie qu'une preuve légitime est acceptée sans divulgation du secret"""
        x, y = ZKPCrypto.generate_keypair()
        message = "bantudevlab-nonce-challenge-xyz"
        proof = ZKPCrypto.generate_proof(secret_x=x, public_y=y, message=message)

        is_valid = ZKPCrypto.verify_proof(public_y=y, proof=proof)
        self.assertTrue(is_valid)

    def test_invalid_zkp_proof_rejected(self):
        """Vérifie qu'une preuve altérée ou fausse est rejetée"""
        x, y = ZKPCrypto.generate_keypair()
        message = "legitimate-challenge"
        proof = ZKPCrypto.generate_proof(secret_x=x, public_y=y, message=message)

        # Alter response
        altered_proof = proof.copy()
        altered_proof["response_s"] = hex(int(proof["response_s"], 16) + 1)
        self.assertFalse(ZKPCrypto.verify_proof(public_y=y, proof=altered_proof))

        # Alter message (challenge replay attempt)
        replay_proof = proof.copy()
        replay_proof["message"] = "fraudulent-challenge"
        self.assertFalse(ZKPCrypto.verify_proof(public_y=y, proof=replay_proof))


class ZKPOIDCIntegrationTestCase(TestCase):
    """T-ADM-702 : Verifie l'exposition OIDC Discovery et les reclamations SSO/equipes."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="sovereign_dev", email="dev@bantudevlab.africa")
        SovereignIdentity.objects.create(
            user=self.user,
            public_key_y="1234abcd",
            country_code="CIV",
        )

    def test_oidc_discovery_endpoint(self):
        response = self.client.get("/.well-known/openid-configuration")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("issuer", data)
        self.assertIn("userinfo_endpoint", data)
        self.assertIn("authorization_endpoint", data)
        self.assertIn("groups", data["scopes_supported"])

    def test_oidc_userinfo_claims(self):
        response = self.client.get(f"/api/zkp/userinfo/?username={self.user.username}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sub"], str(self.user.id))
        self.assertEqual(data["preferred_username"], self.user.username)
        self.assertIn("groups", data)
        self.assertTrue(len(data["groups"]) > 0)
