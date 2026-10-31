import secrets
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SovereignIdentity(models.Model):
    """
    Zero-Trust sovereign identity linked to a user.
    Stores the public key (y) without ever storing the private key (x) or password.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sovereign_identity')
    public_key_y = models.TextField(help_text="Public Key (y = g^x mod p) in hex format")
    country_code = models.CharField(max_length=3, default='CIV', help_text="African Sovereign Member State (ISO-3)")
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zkp_challenges')
    challenge_nonce = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @classmethod
    def create_challenge(cls, user, validity_seconds=300):
        nonce = secrets.token_hex(32)
        expires_at = timezone.now() + timezone.timedelta(seconds=validity_seconds)
        return cls.objects.create(user=user, challenge_nonce=nonce, expires_at=expires_at)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
