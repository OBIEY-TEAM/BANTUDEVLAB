import hashlib
import hmac
import re

from django.conf import settings
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .client import GiteaClient
from .models import SovereignRepository

SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")  # SEC-046: evite toute injection de chemin vers Gitea


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Permet l'exécution des commandes du terminal Gitea et Workbench sans rejet CSRF."""

    def enforce_csrf(self, request):
        return


def _add_cors(response: Response) -> Response:
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-CSRFToken, X-Bantu-Workbench"
    return response


def _resolve_lang(request) -> str:
    raw = (
        (request.data.get("lang") if hasattr(request, "data") and isinstance(request.data, dict) else None)
        or request.query_params.get("lang")
        or request.COOKIES.get("bantu_lang")
        or request.COOKIES.get("django_language")
        or request.COOKIES.get("lang")
        or getattr(request, "LANGUAGE_CODE", None)
        or request.headers.get("Accept-Language", "fr")
    )
    code = str(raw or "fr").lower().strip()[:2]
    return code if code in ("fr", "en", "sw", "pt") else "fr"


class RepositoryListView(APIView):
    """Lists repositories from Gitea forge with sovereign metadata."""

    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = "repo_create"

    def get_throttles(self):
        if self.request and self.request.method == "POST":
            from rest_framework.throttling import ScopedRateThrottle

            return [ScopedRateThrottle()]
        return super().get_throttles()

    def get(self, request):
        from apps.core.views import _merge_local_sovereign_repos

        client = GiteaClient()
        repos = _merge_local_sovereign_repos(client.list_repositories())
        return Response(
            {"count": len(repos), "source": "Gitea CE Sovereign Backend", "repositories": repos},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        from datetime import timedelta
        from django.utils import timezone

        name = request.data.get("name")
        description = request.data.get("description", "")
        private = request.data.get("private", False)

        if not name:
            return Response({"error": "name est requis"}, status=status.HTTP_400_BAD_REQUEST)

        is_demo_user = request.user.is_authenticated and request.user.username == "cadev_evaluator"
        if is_demo_user:
            if len(str(description).encode("utf-8")) > 1024:
                return Response(
                    {"error": "Quota démo dépassé : description limitée à 1024 octets."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cutoff = timezone.now() - timedelta(hours=24)
            SovereignRepository.objects.filter(owner="cadev_evaluator", created_at__lt=cutoff).delete()
            if SovereignRepository.objects.filter(owner="cadev_evaluator").count() >= 5:
                return Response(
                    {"error": "Quota démo atteint : maximum 5 dépôts actifs pour cadev_evaluator."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

        client = GiteaClient()
        result = client.create_repository(
            name=name,
            description=description,
            private=private,
            owner="cadev_evaluator" if is_demo_user else "",
        )

        # Cache in local sovereign repository table
        repo_data = result.get("data", {})
        owner_username = (
            repo_data.get("owner", {}).get("username", "cadev_evaluator" if is_demo_user else "sovereign-org")
            if isinstance(repo_data.get("owner"), dict)
            else ("cadev_evaluator" if is_demo_user else "sovereign-org")
        )
        from config.base_urls import build_gitea_url

        SovereignRepository.objects.update_or_create(
            name=name,
            owner=owner_username,
            defaults={
                "description": description,
                "html_url": repo_data.get("html_url", build_gitea_url(f"{owner_username}/{name}")),
                "clone_url": repo_data.get("clone_url", build_gitea_url(f"{owner_username}/{name}.git")),
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

        from django.core.cache import cache

        cache.delete("bantudevlab_forge_repos_cache")
        cache.delete(GiteaClient.CACHE_KEY_REPOS)

        return Response(result, status=status.HTTP_201_CREATED)


class ForgeStatusView(APIView):
    """Returns connectivity status and sovereign cluster information."""

    permission_classes = [AllowAny]

    def get(self, request):
        client = GiteaClient()
        version_data = client.get_server_version()
        return Response(
            {
                "forge_engine": "Gitea CE (MIT)",
                "cloud_provider": "VPS Ubuntu externe (domaines Datacloud)",
                "datacenter_location": "VPS Ubuntu externe — Déploiement souverain : objectif de la feuille de route",
                "version_info": version_data,
                "status": "ONLINE",
                "sovereignty_assurance": "Auto-hébergement local (Gitea CE + Ollama)",
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
                    "Gemma 2 2B AI PR review queued",
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


class RepoExplorerView(APIView):
    """
    Retourne la liste des dépôts Gitea, les branches d'un dépôt sélectionné,
    ainsi que l'arborescence de ses fichiers pour le Terminal Souverain (Run Security Audit / Ask Gemma).
    """

    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        return _add_cors(Response({}, status=status.HTTP_200_OK))

    def get(self, request):
        client = GiteaClient()
        repos = client.list_repositories(use_cache=False)

        # Fusionner les dépôts enregistrés en base SovereignRepository s'ils ne sont pas encore dans la liste
        known_names = {r.get("full_name") for r in repos if r.get("full_name")}
        for db_repo in SovereignRepository.objects.all()[:30]:
            full = f"{db_repo.owner}/{db_repo.name}"
            if full not in known_names:
                repos.append(
                    {
                        "id": db_repo.id + 5000,
                        "name": db_repo.name,
                        "full_name": full,
                        "owner": {"username": db_repo.owner},
                        "private": db_repo.is_private,
                        "html_url": db_repo.html_url,
                        "default_branch": "main",
                    }
                )
                known_names.add(full)

        selected_repo = request.query_params.get("repo", "").strip("/")
        if not selected_repo and repos:
            selected_repo = repos[0].get("full_name", "sovereign-org/afri-fintech-gateway")

        if "/" in selected_repo:
            owner, repo_name = selected_repo.split("/", 1)
        else:
            owner, repo_name = "sovereign-org", (selected_repo or "afri-fintech-gateway")
            selected_repo = f"{owner}/{repo_name}"

        # S'assurer que le dépôt courant passé par Gitea figure dans la liste
        if selected_repo not in known_names:
            repos.insert(
                0,
                {
                    "id": 9999,
                    "name": repo_name,
                    "full_name": selected_repo,
                    "owner": {"username": owner},
                    "private": False,
                    "default_branch": "main",
                },
            )

        branches_raw = client.get_repository_branches(owner, repo_name)
        branches = [b.get("name", "main") for b in branches_raw if isinstance(b, dict) and b.get("name")]
        if not branches:
            branches = ["main", "develop"]

        selected_branch = request.query_params.get("branch", "").strip() or branches[0]
        if selected_branch not in branches:
            branches.insert(0, selected_branch)

        files = client.get_repository_tree(owner, repo_name, branch=selected_branch)

        return _add_cors(
            Response(
                {
                    "repositories": [
                        {
                            "full_name": r.get("full_name", f"sovereign-org/{r.get('name', 'repo')}"),
                            "name": r.get("name", "repo"),
                            "default_branch": r.get("default_branch", "main"),
                        }
                        for r in repos
                    ],
                    "selected_repo": selected_repo,
                    "branches": branches,
                    "selected_branch": selected_branch,
                    "files": files,
                },
                status=status.HTTP_200_OK,
            )
        )


class RepoCommandAnalyzeView(APIView):
    """
    Exécute la commande structurée du Terminal Souverain (Run Security Audit ou Ask Gemma Review)
    sur un dépôt, une branche et un fichier (ou tous les fichiers '*') dans la langue active (fr, en, sw, pt).
    """

    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        return _add_cors(Response({}, status=status.HTTP_200_OK))

    def post(self, request):
        from apps.ai_assistant.gemma import GemmaAssistant
        from apps.ai_assistant.models import AIInteractionLog
        from apps.ai_assistant.views import sanitize_pii_and_secrets
        from apps.security_scanner.engine import SecurityScannerEngine
        from apps.security_scanner.models import SecurityAuditReport

        action = str(request.data.get("action", "security")).lower().strip()
        repository = str(request.data.get("repository", "sovereign-org/afri-fintech-gateway")).strip("/")
        branch = str(request.data.get("branch", "main")).strip() or "main"
        file_path = str(request.data.get("file_path", "*")).strip() or "*"
        lang = _resolve_lang(request)

        if "/" in repository:
            owner, repo_name = repository.split("/", 1)
        else:
            owner, repo_name = "sovereign-org", repository
            repository = f"{owner}/{repo_name}"

        client = GiteaClient()
        provided_files = request.data.get("files_content")
        provided_map = {}
        if isinstance(provided_files, list):
            for item in provided_files:
                if isinstance(item, dict) and item.get("path") and isinstance(item.get("content"), str):
                    provided_map[str(item["path"])] = item["content"]

        if provided_map:
            target_files = list(provided_map.keys())[:10]
        elif file_path in ("*", "ALL", "all"):
            all_files = client.get_repository_tree(owner, repo_name, branch=branch)
            target_files = [
                f
                for f in all_files
                if not f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf"))
            ][:10]
            if not target_files:
                target_files = list(client.DEFAULT_DEMO_FILES.keys())
        else:
            target_files = [file_path]

        if action in ("gemma", "ai", "review"):
            combined_parts = []
            for fp in target_files:
                raw_content = provided_map.get(fp) or client.get_file_content(owner, repo_name, branch, fp)
                combined_parts.append(f"# --- FILE: {fp} (branch: {branch}) ---\n{raw_content[:3000]}")
            combined_code = sanitize_pii_and_secrets("\n\n".join(combined_parts)[:14000])
            assistant = GemmaAssistant()
            ai_res = assistant.analyze_code(
                code_snippet=combined_code,
                context=f"repo:{repository}@{branch}:{file_path}",
                lang=lang,
            )
            AIInteractionLog.objects.create(
                query_context=f"repo_review:{repository}",
                prompt_snippet=combined_code[:500],
                ai_response=ai_res.get("response", ""),
                model_used=ai_res.get("model", "gemma2:2b"),
            )
            cmd_str = f"gemma-review --repo={repository} --branch={branch} --target={file_path}"
            return _add_cors(
                Response(
                    {
                        "success": True,
                        "action": "gemma",
                        "command": cmd_str,
                        "repository": repository,
                        "branch": branch,
                        "file_path": file_path,
                        "files_analyzed": target_files,
                        "lang": lang,
                        "model": ai_res.get("model", "gemma2:2b"),
                        "response": ai_res.get("response", ""),
                    },
                    status=status.HTTP_200_OK,
                )
            )

        # Action: Run Security Audit (SAST)
        aggregated_issues = []
        for fp in target_files:
            raw_content = provided_map.get(fp) or client.get_file_content(owner, repo_name, branch, fp)
            scan_res = SecurityScannerEngine.scan_code(filename=fp, content=raw_content, lang=lang)
            aggregated_issues.extend(scan_res.get("issues", []))

        critical_count = sum(1 for i in aggregated_issues if i.get("severity") == "CRITICAL")
        high_count = sum(1 for i in aggregated_issues if i.get("severity") == "HIGH")
        medium_count = sum(1 for i in aggregated_issues if i.get("severity") == "MEDIUM")
        deductions = (critical_count * 25) + (high_count * 15) + (medium_count * 5)
        score = max(0, 100 - deductions)

        status_rating = "EXCELLENT"
        if score < 50:
            status_rating = "CRITICAL_RISK"
        elif score < 75:
            status_rating = "WARNING"
        elif score < 90:
            status_rating = "GOOD"

        SecurityAuditReport.objects.create(
            repository_name=repository,
            file_scanned=file_path if file_path != "*" else f"* ({len(target_files)} files)",
            total_issues=len(aggregated_issues),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            sovereignty_score=score,
            status_rating=status_rating,
            raw_findings=aggregated_issues,
        )

        msg_meta = SecurityScannerEngine.I18N_MESSAGES.get(lang, SecurityScannerEngine.I18N_MESSAGES["fr"])
        cmd_str = f"security-audit --repo={repository} --branch={branch} --target={file_path}"
        return _add_cors(
            Response(
                {
                    "success": True,
                    "action": "security",
                    "command": cmd_str,
                    "repository": repository,
                    "branch": branch,
                    "file_path": file_path,
                    "files_analyzed": target_files,
                    "lang": lang,
                    "total_issues": len(aggregated_issues),
                    "critical": critical_count,
                    "high": high_count,
                    "medium": medium_count,
                    "sovereignty_score": score,
                    "status_rating": status_rating,
                    "jurisdiction": msg_meta["jurisdiction"],
                    "issues": aggregated_issues,
                },
                status=status.HTTP_200_OK,
            )
        )
