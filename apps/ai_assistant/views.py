import json
import logging
import re

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .gemma import GemmaAssistant
from .models import AIInteractionLog

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

    permission_classes = [IsAuthenticated]
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
