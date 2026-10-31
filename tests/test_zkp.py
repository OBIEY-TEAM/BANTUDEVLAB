from django.test import TestCase
from apps.zkp_auth.crypto import ZKPCrypto, P, G, Q

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
