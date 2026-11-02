import secrets

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class SovereignIdentity(models.Model):
    """
    Zero-Trust sovereign identity linked to a user.
    Stores the public key (y) without ever storing the private key (x) or password.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sovereign_identity")
    public_key_y = models.TextField(help_text="Public Key (y = g^x mod p) in hex format")
    country_code = models.CharField(max_length=3, default="CIV", help_text="African Sovereign Member State (ISO-3)")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SovereignIdentity({self.user.username} - {self.country_code})"


class ZKPChallenge(models.Model):
    """
    Session/nonce challenge issued for zero-trust interactive/non-interactive authentication.
    Prevents replay attacks.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="zkp_challenges")
    challenge_nonce = models.CharField(max_length=128, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["challenge_nonce"], name="zkp_nonce_idx"),
            models.Index(fields=["expires_at"], name="zkp_expires_idx"),
        ]

    @classmethod
    def create_challenge(cls, user, validity_seconds=300):
        nonce = secrets.token_hex(32)
        expires_at = timezone.now() + timezone.timedelta(seconds=validity_seconds)
        return cls.objects.create(user=user, challenge_nonce=nonce, expires_at=expires_at)

    @classmethod
    def purge_expired_challenges(cls, max_age_minutes: int = 10) -> int:
        """
        T-DEV-504 : Supprime les challenges ZKP expiress depuis plus de max_age_minutes.
        Empeche l'accumulation de nonces orphelins (protection anti-DoS).
        """
        cutoff = timezone.now() - timezone.timedelta(minutes=max_age_minutes)
        deleted_count, _ = cls.objects.filter(expires_at__lt=cutoff).delete()
        return deleted_count

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at


class GitAccessToken(models.Model):
    """
    DEV-03: Git Access Token model validated via ZKP.
    Enables developers to clone and push code to Gitea over HTTPS without standard passwords.
    Stores the SHA-256 hash of the token for security.
    """

    PERMISSION_CHOICES = [
        ("read", "Lecture seule (Clone / Pull)"),
        ("write", "Lecture / Écriture (Clone / Pull / Push)"),
        ("admin", "Administration complète"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="git_access_tokens")
    name = models.CharField(max_length=100, default="CLI Git Access Token")
    token_prefix = models.CharField(max_length=16, help_text="First 8 characters for token identification")
    token_hash = models.CharField(max_length=64, unique=True, db_index=True, help_text="SHA-256 hash of the raw token")
    permissions = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default="write")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["token_hash"], name="git_tok_hash_idx"),
        ]

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True

    def __str__(self):
        return f"GitAccessToken({self.user.username} - {self.name} [{self.token_prefix}...])"
