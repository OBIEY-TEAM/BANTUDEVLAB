"""
Git CLI Access Token Generator and Validator via ZKP (DEV-03).
Enables sovereign developers to authenticate Git operations (clone, push, pull)
over HTTPS without standard passwords.
Tokens are verified cryptographically via Zero-Knowledge Proofs.
"""

import hashlib
import secrets
from typing import Any, Dict

from django.contrib.auth.models import User
from django.utils import timezone

from .crypto import ZKPCrypto
from .models import GitAccessToken, SovereignIdentity


class GitTokenService:
    """Service to issue and validate Git access tokens backed by ZKP proofs."""

    TOKEN_PREFIX = "bnt_git_"

    @classmethod
    def generate_token_raw(cls) -> str:
        """Generates a secure random Git token with sovereign prefix."""
        random_part = secrets.token_hex(20)
        return f"{cls.TOKEN_PREFIX}{random_part}"

    @classmethod
    def hash_token(cls, raw_token: str) -> str:
        """Computes SHA-256 hash of a raw token."""
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @classmethod
    def issue_token_with_zkp(
        cls,
        username: str,
        challenge_nonce: str,
        commitment_t: str,
        response_s: str,
        name: str = "CLI Git Access Token",
        permissions: str = "write",
        validity_days: int = 30,
    ) -> Dict[str, Any]:
        """
        Validates ZKP proof for the user and generates a new Git access token.
        """
        try:
            user = User.objects.get(username=username)
            identity = user.sovereign_identity
        except (User.DoesNotExist, SovereignIdentity.DoesNotExist):
            return {"success": False, "error": "Identité souveraine introuvable"}

        # Verify ZKP proof
        y_int = int(identity.public_key_y, 16)
        proof = {
            "commitment_t": commitment_t,
            "response_s": response_s,
            "message": challenge_nonce,
        }

        if not ZKPCrypto.verify_proof(public_y=y_int, proof=proof):
            return {"success": False, "error": "Preuve ZKP invalide. Génération de token refusée."}

        raw_token = cls.generate_token_raw()
        token_hash = cls.hash_token(raw_token)
        prefix = raw_token[:12]
        expires_at = timezone.now() + timezone.timedelta(days=validity_days)

        token_record = GitAccessToken.objects.create(
            user=user,
            name=name,
            token_prefix=prefix,
            token_hash=token_hash,
            permissions=permissions,
            expires_at=expires_at,
            is_active=True,
        )

        return {
            "success": True,
            "token": raw_token,
            "token_id": token_record.id,
            "name": token_record.name,
            "permissions": token_record.permissions,
            "expires_at": expires_at.isoformat(),
            "username": user.username,
            "instructions": f"Utilisez ce token comme mot de passe pour git clone / git push : https://{user.username}:{raw_token}@forge.bantudevlab.africa/...",
        }

    @classmethod
    def validate_token(cls, raw_token: str) -> Dict[str, Any]:
        """
        Validates a Git CLI token provided during HTTPS Git clone/push.
        """
        if not raw_token or not raw_token.startswith(cls.TOKEN_PREFIX):
            return {"valid": False, "error": "Format de token invalide"}

        token_hash = cls.hash_token(raw_token)
        try:
            token_obj = GitAccessToken.objects.select_related("user").get(token_hash=token_hash)
        except GitAccessToken.DoesNotExist:
            return {"valid": False, "error": "Token inexistant ou révoqué"}

        if not token_obj.is_valid():
            return {"valid": False, "error": "Token expiré ou inactif"}

        token_obj.last_used_at = timezone.now()
        token_obj.save(update_fields=["last_used_at"])

        return {
            "valid": True,
            "username": token_obj.user.username,
            "permissions": token_obj.permissions,
            "token_id": token_obj.id,
            "expires_at": token_obj.expires_at.isoformat() if token_obj.expires_at else None,
        }
