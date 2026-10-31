"""
Zero-Knowledge Proof (ZKP) Cryptographic Engine for BANTUDEVLAB.
Implements the Schnorr / Sigma Identification Protocol using the Fiat-Shamir Heuristic
for Non-Interactive Zero-Knowledge Proofs (NIZKP).

Protocol overview:
1. Public Parameters:
   - p: Large safe prime modulus
   - q: Prime order subgroup (or (p-1)//2)
   - g: Generator of the multiplicative group
2. Key Generation:
   - Prover secret key: x in [1, q-1]
   - Public key: y = (g^x) mod p
3. Non-Interactive Proof (Fiat-Shamir):
   - Prover picks random ephemeral nonce: v in [1, q-1]
   - Commitment: t = (g^v) mod p
   - Challenge: c = H(g || y || t || message) mod q
   - Response: s = (v - c * x) mod q
   - Proof: (t, s)
4. Verification:
   - Check if t in [1, p-1]
   - Compute c = H(g || y || t || message) mod q
   - Verify: (g^s * y^c) mod p == t
   If equal, the prover demonstrated knowledge of secret x without disclosing x.
"""

import hashlib
import secrets
from typing import Tuple, Dict, Any

# Standard 2048-bit MODP Group (RFC 3526 Group 14) parameters for robust security
# Or RFC 5114 1024-bit / standard prime for ultra fast verification during tests
# Here we define a standard well-defined cryptographic prime and generator.
P_HEX = (
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF"
)

P = int(P_HEX, 16)
# Group generator
G = 2
# Subgroup prime order q = (p - 1) // 2
Q = (P - 1) // 2


class ZKPCrypto:
    """Zero-Knowledge Proof implementation based on Schnorr protocol."""

    @staticmethod
    def hash_to_int(*args: Any) -> int:
        """Computes SHA-256 hash of concatenated inputs and returns integer mod Q."""
        hasher = hashlib.sha256()
        for item in args:
            if isinstance(item, int):
                hasher.update(str(item).encode('utf-8'))
            elif isinstance(item, str):
                hasher.update(item.encode('utf-8'))
            elif isinstance(item, bytes):
                hasher.update(item)
            else:
                hasher.update(str(item).encode('utf-8'))
        digest = hasher.hexdigest()
        return int(digest, 16) % Q

    @classmethod
    def generate_keypair(cls, secret_seed: str = None) -> Tuple[int, int]:
        """
        Generates a keypair (x, y).
        x: Private sovereign secret (known ONLY to the user/prover)
        y: Public sovereign identity key = g^x mod p
        """
        if secret_seed:
            # Deterministic derivation from a sovereign seed/passphrase
            x = (cls.hash_to_int("bantudevlab_seed", secret_seed) % (Q - 2)) + 1
        else:
            x = secrets.randbelow(Q - 2) + 1

        y = pow(G, x, P)
        return x, y

    @classmethod
    def generate_proof(cls, secret_x: int, public_y: int, message: str) -> Dict[str, str]:
        """
        Generates a Non-Interactive Zero-Knowledge Proof (NIZKP) of knowledge of secret_x.
        Returns:
            commitment (t), response (s), and message.
        """
        # Random ephemeral nonce
        v = secrets.randbelow(Q - 2) + 1
        # Commitment
        t = pow(G, v, P)
        # Challenge via Fiat-Shamir heuristic
        c = cls.hash_to_int(G, public_y, t, message)
        # Response: s = (v - c * x) mod Q
        s = (v - (c * secret_x)) % Q

        return {
            "commitment_t": hex(t),
            "response_s": hex(s),
            "message": message,
        }

    @classmethod
    def verify_proof(cls, public_y: int, proof: Dict[str, str]) -> bool:
        """
        Verifies the Zero-Knowledge Proof without knowing secret_x.
        Validates:
            t == (g^s * y^c) mod p
        """
        try:
            t = int(proof["commitment_t"], 16)
            s = int(proof["response_s"], 16)
            message = proof.get("message", "")
        except (KeyError, ValueError, TypeError):
            return False

        if not (1 <= t < P):
            return False

        if not (0 <= s < Q):
            return False

        # Reconstruct challenge
        c = cls.hash_to_int(G, public_y, t, message)

        # Verification check: (g^s * y^c) mod p
        lhs = (pow(G, s, P) * pow(public_y, c, P)) % P
        return lhs == t
