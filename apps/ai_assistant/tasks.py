from celery import shared_task
from .gemma import GemmaAssistant
from .models import AIInteractionLog


@shared_task(name='apps.ai_assistant.tasks.async_analyze_code')
def async_analyze_code(code_snippet: str, context: str = 'review') -> dict:
    """
    Tâche Celery asynchrone pour exécuter des appels d'inférence à Gemma 5B
    hors du cycle de requête HTTP de Django.
    """
    assistant = GemmaAssistant()
    result = assistant.analyze_code(code_snippet=code_snippet, context=context)

    # Journalisation de l'interaction IA
    log = AIInteractionLog.objects.create(
        query_context=context,
        prompt_snippet=code_snippet[:500],
        ai_response=result.get('response', ''),
        model_used=result.get('model', 'gemma:5b')
    )
    result['log_id'] = log.id
    return result
