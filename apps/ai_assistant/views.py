import json
import logging
import re

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .gemma import GemmaAssistant
from .models import AIInteractionLog


class EventStreamRenderer(BaseRenderer):
    """Renderer DRF acceptant l'en-tête Accept: text/event-stream sans erreur HTTP 406."""

    media_type = "text/event-stream"
    format = "txt"
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, (bytes, str)):
            return data
        return json.dumps(data)


class WorkbenchDemoSessionAuthentication(SessionAuthentication):
    """Authentification session exemptant le mode démo interactif du Workbench des rejets CSRF."""

    def enforce_csrf(self, request):
        if (
            request.headers.get("X-Bantu-Workbench") == "interactive-demo"
            or "/dashboard" in request.headers.get("Referer", "")
        ):
            return
        return super().enforce_csrf(request)


class IsAuthenticatedOrWorkbenchDemo(BasePermission):
    """Autorise les utilisateurs authentifiés et le Workbench interactif de démonstration (/dashboard/)."""

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        if request.headers.get("X-Bantu-Workbench") == "interactive-demo":
            return True
        referer = request.headers.get("Referer", "")
        return "/dashboard" in referer

# T-DEV-505: Limite stricte du payload (256 Ko ou 15 000 caracteres)
MAX_CODE_CHARS = 15000
MAX_CODE_BYTES = 256 * 1024

IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def sanitize_pii_and_secrets(text: str) -> str:
    """
    T-DEV-505 & SEC-051: Nettoie les adresses IP, emails et cles d'API / secrets
    du code avant injection dans le prompt de gemma2:2b et journalisation.
    """
    from apps.security_scanner.engine import SecurityScannerEngine

    # Anonymisation des adresses IP et adresses email
    text = IP_PATTERN.sub("[IP_ANONYMISEE]", text)
    text = EMAIL_PATTERN.sub("[EMAIL_ANONYMISE]", text)

    # Masquage des cles d'API et secrets detectes par regex
    lines = []
    for line in text.splitlines():
        if any(pattern.search(line) for pattern, _ in SecurityScannerEngine.SECRET_PATTERNS):
            line = "[SECRET MASQUE]"
        lines.append(line)
    return "\n".join(lines)


def mask_secrets(text: str) -> str:
    """Compatibilite avec les anciens appels."""
    return sanitize_pii_and_secrets(text)


def validate_input(code_snippet, context):
    """Retourne un message d'erreur ou None si l'entree est valide."""
    if not isinstance(code_snippet, str) or not code_snippet.strip():
        return "code snippet requis"
    if len(code_snippet) > MAX_CODE_CHARS or len(code_snippet.encode("utf-8")) > MAX_CODE_BYTES:
        return f"code trop volumineux ({MAX_CODE_CHARS} caracteres ou 256 Ko maximum)"
    if not isinstance(context, str) or len(context) > 50:
        return "context invalide"
    return None


logger = logging.getLogger(__name__)


class GemmaCodeReviewView(APIView):
    """
    Submits code snippet to Gemma 2 2B for automated code review and security optimization.
    Supports Server-Sent Events (SSE) streaming (PERF-02) or standard JSON response.
    """

    authentication_classes = [WorkbenchDemoSessionAuthentication]
    permission_classes = [IsAuthenticatedOrWorkbenchDemo]
    renderer_classes = [JSONRenderer, EventStreamRenderer]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "ai"

    def get(self, request):
        """Allows SSE streaming via EventSource (GET /api/ai/review/?code=...&context=...)."""
        code_snippet = request.query_params.get("code")
        context = request.query_params.get("context", "review")
        error = validate_input(code_snippet, context)
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        sanitized_code = sanitize_pii_and_secrets(code_snippet)
        return self._stream_response(sanitized_code, context)

    def post(self, request):
        code_snippet = request.data.get("code")
        context = request.data.get("context", "review")
        stream = request.data.get("stream", None)
        accept_header = request.headers.get("Accept", "")

        error = validate_input(code_snippet, context)
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        sanitized_code = sanitize_pii_and_secrets(code_snippet)

        # SSE Stream requested either via param stream=True or Accept: text/event-stream
        is_sse = stream is True or "text/event-stream" in accept_header
        if is_sse:
            return self._stream_response(sanitized_code, context)

        assistant = GemmaAssistant()
        result = assistant.analyze_code(code_snippet=sanitized_code, context=context)

        # Log AI interaction
        AIInteractionLog.objects.create(
            query_context=context,
            prompt_snippet=sanitized_code[:500],
            ai_response=result.get("response", ""),
            model_used=result.get("model", "gemma2:2b"),
        )

        return Response(result, status=status.HTTP_200_OK)

    def _stream_response(self, code_snippet: str, context: str):
        assistant = GemmaAssistant()

        def event_stream():
            collected_chunks = []
            try:
                for chunk in assistant.stream_analyze_code(code_snippet=code_snippet, context=context):
                    collected_chunks.append(chunk)
                    yield f"data: {json.dumps({'token': chunk, 'done': False})}\n\n"
                full_response = "".join(collected_chunks)
                # Save log once streaming is done
                AIInteractionLog.objects.create(
                    query_context=context,
                    prompt_snippet=code_snippet[:500],
                    ai_response=full_response,
                    model_used=assistant.model_name,
                )
                yield f"data: {json.dumps({'token': '', 'done': True, 'full_response': full_response})}\n\n"
            except Exception:
                # SEC-043: ne jamais exposer le detail d'une exception interne au client.
                logger.exception("Erreur pendant le streaming Gemma")
                yield f"data: {json.dumps({'error': 'Erreur interne du service IA', 'done': True})}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response


class GemmaStatusView(APIView):
    """Returns local Gemma 2 2B AI model state and sovereign configuration."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "model": "Gemma 2 2B (African Sovereign Code Assistant)",
                "precision": "4-bit / 8-bit QLoRA Finetuned",
                "host_environment": "Systalink Sovereign Cloud Cluster",
                "offline_mode_capable": True,
                "status": "READY",
            },
            status=status.HTTP_200_OK,
        )


class CopilotExplainView(APIView):
    """
    T-COP-701 : Point d'acces Copilot pour expliquer un fragment de code ou fichier.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")
        language = request.data.get("language", "")
        if not code or not isinstance(code, str):
            return Response({"error": "Parametre 'code' requis"}, status=status.HTTP_400_BAD_REQUEST)
        if len(code) > MAX_CODE_CHARS:
            return Response(
                {"error": f"Code trop volumineux ({MAX_CODE_CHARS} caracteres max)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sanitized_code = sanitize_pii_and_secrets(code)
        assistant = GemmaAssistant()
        result = assistant.explain_code(code_snippet=sanitized_code, language=language)
        return Response(result, status=status.HTTP_200_OK)


class CopilotCompleteView(APIView):
    """
    T-COP-701 : Point d'acces Copilot pour l'autocompletion de code.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")
        language = request.data.get("language", "")
        if not code or not isinstance(code, str):
            return Response({"error": "Parametre 'code' requis"}, status=status.HTTP_400_BAD_REQUEST)
        if len(code) > MAX_CODE_CHARS:
            return Response(
                {"error": f"Code trop volumineux ({MAX_CODE_CHARS} caracteres max)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sanitized_code = sanitize_pii_and_secrets(code)
        assistant = GemmaAssistant()
        result = assistant.complete_code(prefix_code=sanitized_code, language=language)
        return Response(result, status=status.HTTP_200_OK)


class CopilotPRSummaryView(APIView):
    """
    T-COP-701 : Point d'acces Copilot pour la synthese de Pull Request.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        diff = request.data.get("diff")
        title = request.data.get("title", "")
        if not diff or not isinstance(diff, str):
            return Response({"error": "Parametre 'diff' requis"}, status=status.HTTP_400_BAD_REQUEST)

        sanitized_diff = sanitize_pii_and_secrets(diff)
        assistant = GemmaAssistant()
        result = assistant.generate_pr_summary(diff_content=sanitized_diff, pr_title=title)
        return Response(result, status=status.HTTP_200_OK)


class CopilotPRReviewBotView(APIView):
    """
    T-PR-801 : Declenchement de la revue automatique d'une Pull Request par le bot Copilot souverain.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        from .tasks import async_pr_review_bot

        repo_name = request.data.get("repo_name", "bantudevlab/forge")
        pr_index = request.data.get("pr_index", 1)
        diff_content = request.data.get("diff", "")
        title = request.data.get("title", "")

        # Support payload webhook GitHub / Gitea
        if not diff_content and "pull_request" in request.data:
            pr_data = request.data.get("pull_request", {})
            title = pr_data.get("title", "")
            diff_content = pr_data.get("body", "") or f"+ Pull Request #{pr_data.get('number', 1)}"
            pr_index = pr_data.get("number", 1)
            repo_data = request.data.get("repository", {})
            repo_name = repo_data.get("full_name", repo_name)

        if not diff_content:
            return Response({"error": "Parametre 'diff' requis"}, status=status.HTTP_400_BAD_REQUEST)

        sanitized_diff = sanitize_pii_and_secrets(diff_content)
        result = async_pr_review_bot(
            repo_name=repo_name,
            pr_index=pr_index,
            diff_content=sanitized_diff,
            title=title,
        )
        return Response(result, status=status.HTTP_200_OK)


class CopilotExportView(APIView):
    """
    T-FIN-2601 : Point d'acces Copilot pour l'exportation et persistance de session de discussion.
    Supporte les formats Markdown (.md) et JSON (.json).
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        messages = request.data.get("messages", [])
        export_format = request.data.get("format", "markdown").lower()

        if not isinstance(messages, list):
            return Response({"error": "Parametre 'messages' doit etre une liste"}, status=status.HTTP_400_BAD_REQUEST)

        if export_format == "json":
            return Response({"messages": messages, "format": "json"}, status=status.HTTP_200_OK)

        # Markdown format
        lines = [
            "# Session d'Assistance Copilote Souverain (BantuDevLab)",
            "",
            "> Genere automatiquement par BantuDevLab Sovereign Copilot.",
            "",
            "---",
            "",
        ]

        for idx, msg in enumerate(messages, 1):
            role = msg.get("role", "user").capitalize()
            content = sanitize_pii_and_secrets(str(msg.get("content", "")))
            lines.append(f"### {idx}. {role}")
            lines.append("")
            lines.append(content)
            lines.append("")

        markdown_doc = "\n".join(lines).strip()
        return Response(
            {
                "format": "markdown",
                "content": markdown_doc,
                "total_messages": len(messages),
            },
            status=status.HTTP_200_OK,
        )


class CopilotReviewView(APIView):
    """
    Point d'acces Copilot public pour l'audit de securite interactif depuis l'interface forge.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")
        context = request.data.get("context", "security")
        if not code or not isinstance(code, str):
            return Response({"error": "Parametre 'code' requis"}, status=status.HTTP_400_BAD_REQUEST)

        sanitized_code = sanitize_pii_and_secrets(code)
        assistant = GemmaAssistant()
        result = assistant.analyze_code(code_snippet=sanitized_code, context=context)
        return Response(result, status=status.HTTP_200_OK)
