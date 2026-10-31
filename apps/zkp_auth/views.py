from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from .crypto import ZKPCrypto
from .models import SovereignIdentity, ZKPChallenge


class ZKPRegisterView(APIView):
    """
    Registers a new developer account using only their sovereign ZKP public key.
    The server NEVER receives or stores any password or private key.
    """
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email', f"{username}@bantudevlab.africa")
        public_key_y = request.data.get('public_key_y')
        country_code = request.data.get('country_code', 'AFR')

        if not username or not public_key_y:
            return Response(
                {'error': 'username et public_key_y sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': f"L'utilisateur {username} existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate that public_key_y is a valid integer hex
        try:
            y_int = int(public_key_y, 16)
        except ValueError:
            return Response({'error': 'Format de clé publique invalide (hex attendu)'}, status=status.HTTP_400_BAD_REQUEST)

        if not ZKPCrypto.validate_public_key(y_int):
            return Response(
                {'error': 'Clé publique invalide : n\'appartient pas au sous-groupe premier valide (Small Subgroup Protection).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, email=email)
        # Random unusable password because authentication uses ZKP
        user.set_unusable_password()
        user.save()

        identity = SovereignIdentity.objects.create(
            user=user,
            public_key_y=public_key_y,
            country_code=country_code,
            is_verified=True
        )

        return Response({
            'message': 'Identité souveraine enregistrée avec succès.',
            'username': user.username,
            'country_code': identity.country_code,
            'public_key_y': identity.public_key_y,
        }, status=status.HTTP_201_CREATED)


import secrets
from django.utils import timezone


class ZKPChallengeView(APIView):
    """
    Issues a cryptographically secure challenge nonce for the user to prove identity.
    Protects against user enumeration by returning a consistent response structure,
    status code (200 OK), and uniform timing whether the user exists or not.
    Throttled to 5 req/min.
    """
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'zkp'

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'username requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            challenge = ZKPChallenge.create_challenge(user=user)
            challenge_nonce = challenge.challenge_nonce
            expires_at = challenge.expires_at.isoformat()
        except User.DoesNotExist:
            # Mitigation for user enumeration: generate dummy challenge nonce and expiration with uniform format
            challenge_nonce = secrets.token_hex(32)
            expires_at = (timezone.now() + timezone.timedelta(seconds=300)).isoformat()

        return Response({
            'username': username,
            'challenge_nonce': challenge_nonce,
            'expires_at': expires_at,
        }, status=status.HTTP_200_OK)


class ZKPVerifyView(APIView):
    """
    Verifies the zero-knowledge proof against the active challenge nonce and user's public key.
    Throttled to 5 req/min.
    """
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'zkp'

    def post(self, request):
        username = request.data.get('username')
        challenge_nonce = request.data.get('challenge_nonce')
        commitment_t = request.data.get('commitment_t')
        response_s = request.data.get('response_s')

        if not all([username, challenge_nonce, commitment_t, response_s]):
            return Response({'error': 'Paramètres de preuve ZKP incomplets'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            identity = user.sovereign_identity
            challenge = ZKPChallenge.objects.get(user=user, challenge_nonce=challenge_nonce)
        except (User.DoesNotExist, SovereignIdentity.DoesNotExist, ZKPChallenge.DoesNotExist):
            return Response({'error': 'Identité ou challenge introuvable'}, status=status.HTTP_401_UNAUTHORIZED)

        if not challenge.is_valid():
            return Response({'error': 'Challenge expiré ou déjà utilisé'}, status=status.HTTP_401_UNAUTHORIZED)

        # Mark challenge as used to prevent replay attacks
        challenge.is_used = True
        challenge.save()

        # Zero-Knowledge Proof Verification
        y_int = int(identity.public_key_y, 16)
        proof = {
            'commitment_t': commitment_t,
            'response_s': response_s,
            'message': challenge_nonce,
        }

        is_valid = ZKPCrypto.verify_proof(public_y=y_int, proof=proof)
        if not is_valid:
            return Response({'error': 'Preuve ZKP invalide. Accès refusé.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Audit trail recording
        from apps.core.audit import AuditTrail
        AuditTrail.record_event(
            action_type='ZKP_AUTH',
            actor=user.username,
            details={'country_code': identity.country_code, 'status': 'SUCCESS'}
        )

        login(request, user)
        return Response({
            'success': True,
            'message': f'Authentification ZKP Zero-Trust réussie pour {user.username}',
            'user': {
                'id': user.id,
                'username': user.username,
                'country_code': identity.country_code,
            }
        }, status=status.HTTP_200_OK)


def zkp_login_page(request):
    """Page d'authentification souveraine ZKP"""
    return render(request, 'zkp_auth/login.html')


from .tokens import GitTokenService


class GitTokenGenerateView(APIView):
    """
    DEV-03: Generates a Git Access Token for CLI Git push/clone operations.
    Requires and validates a Zero-Knowledge Proof (ZKP).
    """
    def post(self, request):
        username = request.data.get('username')
        challenge_nonce = request.data.get('challenge_nonce')
        commitment_t = request.data.get('commitment_t')
        response_s = request.data.get('response_s')
        token_name = request.data.get('name', 'CLI Git Access Token')
        permissions = request.data.get('permissions', 'write')
        validity_days = int(request.data.get('validity_days', 30))

        if not all([username, challenge_nonce, commitment_t, response_s]):
            return Response(
                {'error': 'username, challenge_nonce, commitment_t et response_s sont requis pour prouver votre identité via ZKP.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = GitTokenService.issue_token_with_zkp(
            username=username,
            challenge_nonce=challenge_nonce,
            commitment_t=commitment_t,
            response_s=response_s,
            name=token_name,
            permissions=permissions,
            validity_days=validity_days
        )

        if not result.get('success'):
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)

        return Response(result, status=status.HTTP_201_CREATED)


class GitTokenValidateView(APIView):
    """
    DEV-03: Validates a Git Access Token supplied by Git CLI or Gitea over HTTPS.
    """
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'token requis'}, status=status.HTTP_400_BAD_REQUEST)

        result = GitTokenService.validate_token(token)
        if not result.get('valid'):
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)

        return Response(result, status=status.HTTP_200_OK)
