"""
QA-02: Fuzzing & Tests de Résilience Cryptographique ZKP pour BANTUDEVLAB.
Développe une suite complète de tests cryptographiques aléatoires (fuzzing) injectant :
- Des valeurs non conformes (scalaires négatifs, hors limites, corruptions de format),
- Des clés publiques dégradées (petits sous-groupes, y in {0, 1, P-1, P, P+1}, ordre composite),
- Des nonces expirés, rejoués ou corrompus,
- Des messages et challenges altérés prouvant l'inviolabilité mathématique de l'implémentation.
"""

import random
import secrets
import string

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

from apps.zkp_auth.crypto import G, P, Q, ZKPCrypto
from apps.zkp_auth.models import SovereignIdentity, ZKPChallenge
from apps.zkp_auth.tokens import GitTokenService


class ZKPFuzzingResilienceTestCase(TestCase):
    """Suite de fuzzing et tests de résilience cryptographique de l'implémentation ZKP."""

    def setUp(self):
        from django.core.cache import cache

        cache.clear()
        self.client = Client()
        self.username = "fuzz_user"
        self.secret_x, self.public_y = ZKPCrypto.generate_keypair("sovereign_fuzz_seed_123")
        self.user = User.objects.create_user(username=self.username, email="fuzz@bantudevlab.africa")
        self.user.set_unusable_password()
        self.user.save()
        self.identity = SovereignIdentity.objects.create(
            user=self.user, public_key_y=hex(self.public_y), country_code="CIV", is_verified=True
        )

    # -------------------------------------------------------------
    # 1. FUZZING DES CLÉS PUBLIQUES (Petits sous-groupes & Dégénérées)
    # -------------------------------------------------------------
    def test_fuzz_degraded_and_invalid_public_keys(self):
        """Injecte des clés publiques dégénérées, nulles, hors groupe ou vulnérables."""
        invalid_keys = [
            0,
            1,
            -1,
            -self.public_y,
            P - 1,  # Éléments d'ordre 2
            P,
            P + 1,
            P + 100,
            2**2048,
            "not_an_int",
            None,
            3.14159,
            [],
            {},
        ]

        # Éléments non résidus quadratiques (y^Q mod P != 1)
        # G n'est pas un résidu d'ordre Q si c'est un non-résidu mod P
        for candidate in [3, 5, 7, 11, 13]:
            if pow(candidate, Q, P) != 1:
                invalid_keys.append(candidate)

        for bad_y in invalid_keys:
            with self.subTest(bad_y=bad_y):
                self.assertFalse(
                    ZKPCrypto.validate_public_key(bad_y),
                    f"La clé publique dégradée {bad_y} n'aurait pas dû être validée !",
                )

    def test_fuzz_random_scalar_injection_in_public_key_validation(self):
        """Fuzzing aléatoire de scalaires dans la validation de clé publique."""
        for _ in range(50):
            # Génère de grands nombres arbitraires hors du sous-groupe premier
            bit_length = random.choice([64, 128, 256, 512, 1024, 2048, 2050])
            rand_scalar = secrets.randbits(bit_length)

            # Si rand_scalar n'est pas dans le sous-groupe q, la validation doit échouer
            is_valid = ZKPCrypto.validate_public_key(rand_scalar)
            if not (1 < rand_scalar < P - 1) or pow(rand_scalar, Q, P) != 1:
                self.assertFalse(is_valid, f"Le scalaire aléatoire {rand_scalar} ne devait pas être accepté.")

    # -------------------------------------------------------------
    # 2. FUZZING DES PREUVES FIAT-SHAMIR (t, s) ET CHALLENGES
    # -------------------------------------------------------------
    def test_fuzz_tampered_commitments_and_responses(self):
        """Injecte des variations pseudo-aléatoires sur (t, s) pour prouver le rejet."""
        message = "nonce_cryptographique_valide_42"
        valid_proof = ZKPCrypto.generate_proof(self.secret_x, self.public_y, message)
        t_int = int(valid_proof["commitment_t"], 16)
        s_int = int(valid_proof["response_s"], 16)

        # Vérifie d'abord que la preuve de départ est valide
        self.assertTrue(ZKPCrypto.verify_proof(self.public_y, valid_proof))

        # Altérations de s
        s_fuzz_cases = [
            (s_int + 1) % Q,
            (s_int - 1) % Q,
            0 if s_int != 0 else 1,
            s_int ^ 0x01,
            s_int ^ 0xFF,
            s_int + Q,  # s >= Q (hors domaine)
            -1,  # négatif
            -s_int,
        ]

        for tampered_s in s_fuzz_cases:
            tampered_proof = {
                "commitment_t": hex(t_int),
                "response_s": hex(tampered_s) if tampered_s >= 0 else str(tampered_s),
                "message": message,
            }
            self.assertFalse(
                ZKPCrypto.verify_proof(self.public_y, tampered_proof),
                f"La preuve avec s altéré ({tampered_s}) n'a pas été rejetée !",
            )

        # Altérations de t
        t_fuzz_cases = [
            (t_int + 1) % P,
            (t_int - 1) % P,
            (t_int * G) % P,
            0,  # t < 1
            1,
            P,  # t >= P
            P + 1,
            -t_int,
        ]

        for tampered_t in t_fuzz_cases:
            tampered_proof = {
                "commitment_t": hex(tampered_t) if tampered_t >= 0 else str(tampered_t),
                "response_s": hex(s_int),
                "message": message,
            }
            self.assertFalse(
                ZKPCrypto.verify_proof(self.public_y, tampered_proof),
                f"La preuve avec t altéré ({tampered_t}) n'a pas été rejetée !",
            )

    def test_fuzz_tampered_messages_and_nonces(self):
        """Altère le message / nonce dans le protocole Fiat-Shamir."""
        message = "sovereign_tx_challenge_nonce_12345"
        proof = ZKPCrypto.generate_proof(self.secret_x, self.public_y, message)

        for _ in range(30):
            # Génère des mutations aléatoires du message
            mutation_type = random.choice(["flip_char", "append", "prepend", "empty", "random_str"])
            if mutation_type == "flip_char":
                pos = random.randint(0, len(message) - 1)
                corrupted_char = chr((ord(message[pos]) + random.randint(1, 10)) % 126)
                mutated_message = message[:pos] + corrupted_char + message[pos + 1 :]
            elif mutation_type == "append":
                mutated_message = message + "x"
            elif mutation_type == "prepend":
                mutated_message = "0" + message
            elif mutation_type == "empty":
                mutated_message = ""
            else:
                mutated_message = "".join(random.choices(string.ascii_letters + string.digits, k=32))

            if mutated_message != message:
                corrupted_proof = {
                    "commitment_t": proof["commitment_t"],
                    "response_s": proof["response_s"],
                    "message": mutated_message,
                }
                self.assertFalse(
                    ZKPCrypto.verify_proof(self.public_y, corrupted_proof),
                    f"Le message altéré '{mutated_message}' a été validé à tort !",
                )

    def test_fuzz_corrupted_payload_structures(self):
        """Injecte des structures de preuve non conformes et types imprévus."""
        malformed_proofs = [
            {},
            {"commitment_t": "0x123"},
            {"response_s": "0x456"},
            {"commitment_t": "invalid_hex", "response_s": "0x123", "message": "msg"},
            {"commitment_t": "0x123", "response_s": "invalid_hex", "message": "msg"},
            {"commitment_t": None, "response_s": "0x123", "message": "msg"},
            {"commitment_t": "0x123", "response_s": None, "message": "msg"},
            {"commitment_t": 12345, "response_s": 67890, "message": "msg"},
            {"commitment_t": "", "response_s": "", "message": ""},
        ]

        for bad_proof in malformed_proofs:
            self.assertFalse(ZKPCrypto.verify_proof(self.public_y, bad_proof))

    # -------------------------------------------------------------
    # 3. RÉSILIENCE API REST & ATTAQUES PAR REJEU / EXPIRATION
    # -------------------------------------------------------------
    def test_resilience_expired_and_reused_challenges(self):
        """Prouve le rejet immédiat des challenges expirés ou rejoués."""
        challenge = ZKPChallenge.create_challenge(user=self.user)
        proof = ZKPCrypto.generate_proof(self.secret_x, self.public_y, challenge.challenge_nonce)

        # 1er usage : succès
        res1 = self.client.post(
            "/api/zkp/verify/",
            {
                "username": self.username,
                "challenge_nonce": challenge.challenge_nonce,
                "commitment_t": proof["commitment_t"],
                "response_s": proof["response_s"],
            },
            content_type="application/json",
        )
        self.assertEqual(res1.status_code, 200)

        # 2e usage : Rejeu immédiat -> DOIT ÉCHOUER (is_used = True)
        res2 = self.client.post(
            "/api/zkp/verify/",
            {
                "username": self.username,
                "challenge_nonce": challenge.challenge_nonce,
                "commitment_t": proof["commitment_t"],
                "response_s": proof["response_s"],
            },
            content_type="application/json",
        )
        self.assertEqual(res2.status_code, 401)
        self.assertIn("expiré ou déjà utilisé", res2.json().get("error", ""))

        # Challenge expiré artificiellement dans le passé
        expired_challenge = ZKPChallenge.create_challenge(user=self.user)
        expired_challenge.expires_at = timezone.now() - timezone.timedelta(seconds=10)
        expired_challenge.save()

        proof_exp = ZKPCrypto.generate_proof(self.secret_x, self.public_y, expired_challenge.challenge_nonce)
        res3 = self.client.post(
            "/api/zkp/verify/",
            {
                "username": self.username,
                "challenge_nonce": expired_challenge.challenge_nonce,
                "commitment_t": proof_exp["commitment_t"],
                "response_s": proof_exp["response_s"],
            },
            content_type="application/json",
        )
        self.assertEqual(res3.status_code, 401)

    def test_fuzz_oversized_hex_payload_dos_protection(self):
        """T-SEC-202 & T-TST-502: Teste le rejet immédiat des hexadécimaux géants anti-DoS."""
        oversized_hex = "a" * 2000
        proof_dos = {"commitment_t": oversized_hex, "response_s": "0x123", "message": "dos_test"}
        self.assertFalse(ZKPCrypto.verify_proof(self.public_y, proof_dos))

    def test_resilience_git_token_issuance_fuzzing(self):
        """Teste la résilience du service d'émission de token Git face à de faux paramètres."""
        challenge = ZKPChallenge.create_challenge(user=self.user)
        valid_proof = ZKPCrypto.generate_proof(self.secret_x, self.public_y, challenge.challenge_nonce)

        # Preuve altérée
        bad_token_res = GitTokenService.issue_token_with_zkp(
            username=self.username,
            challenge_nonce=challenge.challenge_nonce,
            commitment_t=valid_proof["commitment_t"],
            response_s=hex((int(valid_proof["response_s"], 16) + 1) % Q),
        )
        self.assertFalse(bad_token_res["success"])
        self.assertIn("Preuve ZKP invalide", bad_token_res["error"])

        # Token émis avec une preuve valide
        good_token_res = GitTokenService.issue_token_with_zkp(
            username=self.username,
            challenge_nonce=challenge.challenge_nonce,
            commitment_t=valid_proof["commitment_t"],
            response_s=valid_proof["response_s"],
        )
        self.assertTrue(good_token_res["success"])
        token = good_token_res["token"]

        # Fuzzing de validation du token : altération de bits
        for _ in range(10):
            corrupted_token = list(token)
            idx = random.randint(len(GitTokenService.TOKEN_PREFIX), len(token) - 1)
            corrupted_token[idx] = "0" if corrupted_token[idx] != "0" else "1"
            corrupted_token_str = "".join(corrupted_token)

            val_res = GitTokenService.validate_token(corrupted_token_str)
            self.assertFalse(val_res["valid"])
