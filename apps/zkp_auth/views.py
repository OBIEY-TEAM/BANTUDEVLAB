from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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


class ZKPChallengeView(APIView):
    """
    Issues a cryptographically secure challenge nonce for the user to prove identity.
    """
    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'username requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur introuvable'}, status=status.HTTP_404_NOT_FOUND)

        challenge = ZKPChallenge.create_challenge(user=user)
        return Response({
            'username': user.username,
            'challenge_nonce': challenge.challenge_nonce,
            'expires_at': challenge.expires_at.isoformat(),
        }, status=status.HTTP_200_OK)


class ZKPVerifyView(APIView):
    """
    Verifies the zero-knowledge proof against the active challenge nonce and user's public key.
    """
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
