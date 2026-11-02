import re
import secrets

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .crypto import ZKPCrypto
from .models import SovereignIdentity, ZKPChallenge
from .tokens import GitTokenService

USERNAME_RE = re.compile(r"^[A-Za-z0-9._-]{3,32}$")
COUNTRY_RE = re.compile(r"^[A-Z]{3}$")
MAX_HEX_LEN = 1024  # une valeur de 2048 bits = 512 caracteres hex


def _valid_proof_params(username, challenge_nonce, commitment_t, response_s) -> bool:
    """SEC-031: tous les parametres sont presents, de type str et de taille bornee."""
    params = (username, challenge_nonce, commitment_t, response_s)
    if not all(params):
        return False
    return (
        all(isinstance(p, str) for p in params)
        and len(username) <= 150
        and all(len(p) <= MAX_HEX_LEN for p in params[1:])
    )


class ZKPRegisterView(APIView):
    """
    Registers a new developer account using only their sovereign ZKP public key.
    The server NEVER receives or stores any password or private key.
    """

    permission_classes = [AllowAny]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "zkp_register"

    def post(self, request):
        username = request.data.get("username")
        if username is not None and (not isinstance(username, str) or not USERNAME_RE.match(username)):
            return Response(
                {"error": "username invalide (3-32 caracteres : lettres, chiffres, '.', '_', '-')"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        email = request.data.get("email", f"{username}@bantudevlab.africa")
        public_key_y = request.data.get("public_key_y")
        country_code = request.data.get("country_code", "AFR")

        if not isinstance(country_code, str) or not COUNTRY_RE.match(country_code):
            return Response({"error": "country_code invalide (ISO-3 attendu)"}, status=status.HTTP_400_BAD_REQUEST)

        if not username or not public_key_y:
            return Response({"error": "username et public_key_y sont requis"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": f"L'utilisateur {username} existe déjà."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that public_key_y is a valid integer hex
        try:
            if not isinstance(public_key_y, str) or len(public_key_y) > MAX_HEX_LEN:
                raise ValueError("public_key_y trop long")
            y_int = int(public_key_y, 16)
        except (ValueError, TypeError):
            return Response(
                {"error": "Format de clé publique invalide (hex attendu)"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not ZKPCrypto.validate_public_key(y_int):
            return Response(
                {
                    "error": "Clé publique invalide : n'appartient pas au sous-groupe premier valide (Small Subgroup Protection)."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, email=email)
        # Random unusable password because authentication uses ZKP
        user.set_unusable_password()
        user.save()

        identity = SovereignIdentity.objects.create(
            user=user, public_key_y=public_key_y, country_code=country_code, is_verified=True
        )

        return Response(
            {
                "message": "Identité souveraine enregistrée avec succès.",
                "username": user.username,
                "country_code": identity.country_code,
                "public_key_y": identity.public_key_y,
            },
            status=status.HTTP_201_CREATED,
        )


class ZKPChallengeView(APIView):
    """
    Issues a cryptographically secure challenge nonce for the user to prove identity.
    Protects against user enumeration by returning a consistent response structure,
    status code (200 OK), and uniform timing whether the user exists or not.
    Throttled to 5 req/min.
    """

    permission_classes = [AllowAny]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "zkp"

    def post(self, request):
        username = request.data.get("username")
        if not username:
            return Response({"error": "username requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            challenge = ZKPChallenge.create_challenge(user=user)
            challenge_nonce = challenge.challenge_nonce
            expires_at = challenge.expires_at.isoformat()
        except User.DoesNotExist:
            # Mitigation for user enumeration: generate dummy challenge nonce and expiration with uniform format
            challenge_nonce = secrets.token_hex(32)
            expires_at = (timezone.now() + timezone.timedelta(seconds=300)).isoformat()

        return Response(
            {
                "username": username,
                "challenge_nonce": challenge_nonce,
                "expires_at": expires_at,
            },
            status=status.HTTP_200_OK,
        )


class ZKPVerifyView(APIView):
    """
    Verifies the zero-knowledge proof against the active challenge nonce and user's public key.
    Throttled to 5 req/min.
    """

    permission_classes = [AllowAny]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "zkp"

    def post(self, request):
        username = request.data.get("username")
        challenge_nonce = request.data.get("challenge_nonce")
        commitment_t = request.data.get("commitment_t")
        response_s = request.data.get("response_s")

        if not _valid_proof_params(username, challenge_nonce, commitment_t, response_s):
            return Response({"error": "Paramètres de preuve ZKP incomplets"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            identity = user.sovereign_identity
            challenge = ZKPChallenge.objects.get(user=user, challenge_nonce=challenge_nonce)
        except (User.DoesNotExist, SovereignIdentity.DoesNotExist, ZKPChallenge.DoesNotExist):
            return Response({"error": "Identité ou challenge introuvable"}, status=status.HTTP_401_UNAUTHORIZED)

        if not challenge.is_valid():
            return Response({"error": "Challenge expiré ou déjà utilisé"}, status=status.HTTP_401_UNAUTHORIZED)

        # SEC-030: consommation atomique du defi (anti-rejeu, meme en concurrence).
        consumed = ZKPChallenge.objects.filter(pk=challenge.pk, is_used=False).update(is_used=True)
        if not consumed:
            return Response({"error": "Challenge expiré ou déjà utilisé"}, status=status.HTTP_401_UNAUTHORIZED)

        # Zero-Knowledge Proof Verification
        y_int = int(identity.public_key_y, 16)
        proof = {
            "commitment_t": commitment_t,
            "response_s": response_s,
            "message": challenge_nonce,
        }

        is_valid = ZKPCrypto.verify_proof(public_y=y_int, proof=proof)
        if not is_valid:
            return Response({"error": "Preuve ZKP invalide. Accès refusé."}, status=status.HTTP_401_UNAUTHORIZED)

        # Audit trail recording
        from apps.core.audit import AuditTrail

        AuditTrail.record_event(
            action_type="ZKP_AUTH",
            actor=user.username,
            details={"country_code": identity.country_code, "status": "SUCCESS"},
        )

        login(request, user)
        return Response(
            {
                "success": True,
                "message": f"Authentification ZKP Zero-Trust réussie pour {user.username}",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "country_code": identity.country_code,
                },
            },
            status=status.HTTP_200_OK,
        )


def zkp_login_page(request):
    """Page d'authentification souveraine ZKP"""
    return render(request, "zkp_auth/login.html")


class GitTokenGenerateView(APIView):
    """
    DEV-03: Generates a Git Access Token for CLI Git push/clone operations.
    Requires and validates a Zero-Knowledge Proof (ZKP).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        challenge_nonce = request.data.get("challenge_nonce")
        commitment_t = request.data.get("commitment_t")
        response_s = request.data.get("response_s")
        token_name = request.data.get("name", "CLI Git Access Token")
        permissions = request.data.get("permissions", "write")
        if permissions not in ("read", "write", "admin"):
            return Response(
                {"error": "permissions doit valoir read, write ou admin"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            validity_days = int(request.data.get("validity_days", 30))
        except (TypeError, ValueError):
            return Response({"error": "validity_days doit etre un entier"}, status=status.HTTP_400_BAD_REQUEST)
        if not 1 <= validity_days <= 365:
            return Response({"error": "validity_days doit etre entre 1 et 365"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(token_name, str) or len(token_name) > 100:
            return Response({"error": "name invalide (100 caracteres max)"}, status=status.HTTP_400_BAD_REQUEST)

        if not all([username, challenge_nonce, commitment_t, response_s]):
            return Response(
                {
                    "error": "username, challenge_nonce, commitment_t et response_s sont requis pour prouver votre identité via ZKP."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = GitTokenService.issue_token_with_zkp(
            username=username,
            challenge_nonce=challenge_nonce,
            commitment_t=commitment_t,
            response_s=response_s,
            name=token_name,
            permissions=permissions,
            validity_days=validity_days,
        )

        if not result.get("success"):
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)

        return Response(result, status=status.HTTP_201_CREATED)


class ZKPUserInfoView(APIView):
    """
    T-GIT-301: Endpoint UserInfo pour la stratégie OmniAuth GitLab BantuZKP
    (gitlab/lib/gitlab/auth/bantu_zkp.rb). Permet le single sign-on et le
    provisionnement automatique d'utilisateurs souverains sans mot de passe.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get("username")
        if not username and request.user.is_authenticated:
            username = request.user.username

        if not username:
            return Response({"error": "Paramètre username manquant"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            identity = getattr(user, "sovereign_identity", None)
            country_code = identity.country_code if identity else "CIV"
            public_key_y = identity.public_key_y if identity else ""
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "user_id": user.id,
                "username": user.username,
                "email": user.email or f"{user.username}@bantudevlab.africa",
                "country_code": country_code,
                "public_key_y": public_key_y,
                "sovereignty_level": "Tier-1 Continental",
                "groups": ["Sovereign African Developers", "Bantu Forge Members"],
            },
            status=status.HTTP_200_OK,
        )


class GitTokenValidateView(APIView):
    """
    DEV-03: Validates a Git Access Token supplied by Git CLI or Gitea over HTTPS.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "token requis"}, status=status.HTTP_400_BAD_REQUEST)

        result = GitTokenService.validate_token(token)
        if not result.get("valid"):
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)

        return Response(result, status=status.HTTP_200_OK)
