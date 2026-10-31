from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .gemma import GemmaAssistant
from .models import AIInteractionLog

class GemmaCodeReviewView(APIView):
    """
    Submits code snippet to Gemma 5B for automated code review and security optimization.
    """
    def post(self, request):
        code_snippet = request.data.get('code')
        context = request.data.get('context', 'review')

        if not code_snippet:
            return Response({'error': 'code snippet requis'}, status=status.HTTP_400_BAD_REQUEST)

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
