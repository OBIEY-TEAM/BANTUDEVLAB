import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import StreamingHttpResponse
from .gemma import GemmaAssistant
from .models import AIInteractionLog

class GemmaCodeReviewView(APIView):
    """
    Submits code snippet to Gemma 5B for automated code review and security optimization.
    Supports Server-Sent Events (SSE) streaming (PERF-02) or standard JSON response.
    """
    def get(self, request):
        """Allows SSE streaming via EventSource (GET /api/ai/review/?code=...&context=...)."""
        code_snippet = request.query_params.get('code')
        context = request.query_params.get('context', 'review')
        if not code_snippet:
            return Response({'error': 'code snippet requis'}, status=status.HTTP_400_BAD_REQUEST)
        return self._stream_response(code_snippet, context)

    def post(self, request):
        code_snippet = request.data.get('code')
        context = request.data.get('context', 'review')
        stream = request.data.get('stream', None)
        accept_header = request.headers.get('Accept', '')

        if not code_snippet:
            return Response({'error': 'code snippet requis'}, status=status.HTTP_400_BAD_REQUEST)

        # SSE Stream requested either via param stream=True or Accept: text/event-stream
        is_sse = stream is True or 'text/event-stream' in accept_header
        if is_sse:
            return self._stream_response(code_snippet, context)

        assistant = GemmaAssistant()
        result = assistant.analyze_code(code_snippet=code_snippet, context=context)

        # Log AI interaction
        AIInteractionLog.objects.create(
            query_context=context,
            prompt_snippet=code_snippet[:500],
            ai_response=result.get('response', ''),
            model_used=result.get('model', 'gemma:5b')
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
                    model_used=assistant.model_name
                )
                yield f"data: {json.dumps({'token': '', 'done': True, 'full_response': full_response})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response


class GemmaStatusView(APIView):
    """Returns local Gemma 5B AI model state and sovereign configuration."""
    def get(self, request):
        return Response({
            "model": "Gemma 5B (African Sovereign Code Assistant)",
            "precision": "4-bit / 8-bit QLoRA Finetuned",
            "host_environment": "Systalink Sovereign Cloud Cluster",
            "offline_mode_capable": True,
            "status": "READY"
        }, status=status.HTTP_200_OK)
