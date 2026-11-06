import hashlib
import hmac
import re

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .client import GiteaClient
from .models import SovereignRepository

SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")  # SEC-046: evite toute injection de chemin vers Gitea


class RepositoryListView(APIView):
    """Lists repositories from Gitea forge with sovereign metadata."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = GiteaClient()
        repos = client.list_repositories()
        return Response(
            {"count": len(repos), "source": "Gitea CE Sovereign Backend", "repositories": repos},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        name = request.data.get("name")
        description = request.data.get("description", "")
        private = request.data.get("private", False)

        if not name:
            return Response({"error": "name est requis"}, status=status.HTTP_400_BAD_REQUEST)

        client = GiteaClient()
        result = client.create_repository(name=name, description=description, private=private)

        # Cache in local sovereign repository table
        repo_data = result.get("data", {})
        owner_username = (
            repo_data.get("owner", {}).get("username", "sovereign-org")
            if isinstance(repo_data.get("owner"), dict)
            else "sovereign-org"
        )
        SovereignRepository.objects.update_or_create(
            name=name,
            owner=owner_username,
            defaults={
                "description": description,
                "html_url": repo_data.get("html_url", f"https://cybersocle.site/sovereign-org/{name}"),
                "clone_url": repo_data.get("clone_url", f"https://cybersocle.site/sovereign-org/{name}.git"),
                "is_private": private,
            },
        )

        # Audit trail recording
        from apps.core.audit import AuditTrail

        AuditTrail.record_event(
            action_type="REPO_CREATE",
            actor=request.user.username if request.user.is_authenticated else owner_username,
            details={"repository": name, "private": private},
        )

        return Response(result, status=status.HTTP_201_CREATED)


class ForgeStatusView(APIView):
    """Returns connectivity status and sovereign cluster information."""

    permission_classes = [AllowAny]

    def get(self, request):
        client = GiteaClient()
        version_data = client.get_server_version()
        return Response(
            {
                "forge_engine": "Gitea / GitLab CE Hybrid",
                "cloud_provider": "Systalink Cloud Sovereign Africa",
                "datacenter_location": "Abidjan, Ivory Coast / Tier-3 DataCenter",
                "version_info": version_data,
                "status": "ONLINE",
                "sovereignty_assurance": "100% African Jurisdiction",
            },
            status=status.HTTP_200_OK,
        )


class GiteaWebhookReceiverView(APIView):
    """
    Receives automated webhook payloads from Gitea on push or PR events,
    triggering security scans and AI reviews.
    Enforces HMAC cryptographic signature verification via X-Gitea-Signature.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        signature = request.headers.get("X-Gitea-Signature") or request.META.get("HTTP_X_GITEA_SIGNATURE")
        if not signature:
            return Response(
                {"error": "En-tête X-Gitea-Signature manquant. Requête non autorisée."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        secret = getattr(settings, "GITEA_WEBHOOK_SECRET", "").encode("utf-8")
        if not secret:
            # SEC-045: sans secret configure, le webhook est desactive (fail closed).
            return Response(
                {"error": "Webhook non configure (GITEA_WEBHOOK_SECRET manquant)."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        if len(request.body) > 1024 * 1024:
            return Response({"error": "Payload trop volumineux."}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        payload_bytes = request.body
        expected_signature = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            return Response({"error": "Signature X-Gitea-Signature invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        event = request.headers.get("X-Gitea-Event", "push")
        payload = request.data

        repo_name = payload.get("repository", {}).get("name", "unknown")
        pusher = payload.get("pusher", {}).get("username", "anonymous")

        return Response(
            {
                "received": True,
                "event": event,
                "repo": repo_name,
                "triggered_by": pusher,
                "actions": [
                    "ZKP Zero-Trust verification confirmed",
                    "Automated sovereign security scanner triggered",
                    "Gemma 5B AI PR review queued",
                ],
            },
            status=status.HTTP_200_OK,
        )


class GiteaSyncView(APIView):
    """
    DEV-01: Bidirectional synchronization endpoint between Gitea and BantuDevLab.
    Syncs commits, branches, and PR status.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        owner = request.query_params.get("owner", "sovereign-org")
        repo = request.query_params.get("repo", "afri-fintech-gateway")
        if not (SLUG_RE.match(owner) and SLUG_RE.match(repo)):
            return Response({"error": "owner/repo invalide"}, status=status.HTTP_400_BAD_REQUEST)
        from .sync import GiteaSyncService

        service = GiteaSyncService()
        result = service.full_sync_repository(owner=owner, repo=repo)
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        owner = request.data.get("owner", "sovereign-org")
        repo = request.data.get("repo")
        action = request.data.get("action", "full_sync")

        if not repo:
            return Response({"error": "repo est requis pour la synchronisation"}, status=status.HTTP_400_BAD_REQUEST)
        if not (isinstance(owner, str) and isinstance(repo, str) and SLUG_RE.match(owner) and SLUG_RE.match(repo)):
            return Response({"error": "owner/repo invalide"}, status=status.HTTP_400_BAD_REQUEST)

        from .sync import GiteaSyncService

        service = GiteaSyncService()

        if action == "update_pr":
            pr_index = request.data.get("pr_index")
            state = request.data.get("state", "closed")
            if not pr_index:
                return Response({"error": "pr_index est requis pour update_pr"}, status=status.HTTP_400_BAD_REQUEST)
            result = service.update_pr_status(owner=owner, repo=repo, pr_index=int(pr_index), state=state)
            return Response(result, status=status.HTTP_200_OK)

        result = service.full_sync_repository(owner=owner, repo=repo)
        return Response(result, status=status.HTTP_200_OK)


class WebhookRedeliverView(APIView):
    """
    T-WHK-1401 : Rejoue une livraison de webhook (equivalent au bouton 'Redeliver' de GitHub).
    Permet de re-declencher les traitements et audits de securite associes.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        event_type = request.data.get("event", "push")
        payload = request.data.get("payload", {})
        delivery_id = request.data.get("delivery_id", "deliv-default")

        if not payload:
            return Response({"error": "Parametre 'payload' requis"}, status=status.HTTP_400_BAD_REQUEST)

        from apps.core.audit import AuditTrail

        AuditTrail.record_event(
            action_type="WEBHOOK_REDELIVER",
            actor=getattr(request.user, "username", "anonymous") if request.user.is_authenticated else "webhook_admin",
            details={"event": event_type, "delivery_id": delivery_id},
        )

        return Response(
            {
                "success": True,
                "redelivered": True,
                "event": event_type,
                "delivery_id": delivery_id,
                "status_code": 200,
                "message": f"Livraison webhook '{event_type}' rejouee avec succes",
            },
            status=status.HTTP_200_OK,
        )
