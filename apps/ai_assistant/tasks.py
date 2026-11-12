from celery import shared_task

from .gemma import GemmaAssistant
from .models import AIInteractionLog


@shared_task(name="apps.ai_assistant.tasks.async_analyze_code")
def async_analyze_code(code_snippet: str, context: str = "review") -> dict:
    """
    Tâche Celery asynchrone pour exécuter des appels d'inférence à Gemma 2 2B
    hors du cycle de requête HTTP de Django.
    """
    assistant = GemmaAssistant()
    result = assistant.analyze_code(code_snippet=code_snippet, context=context)

    # Journalisation de l'interaction IA
    log = AIInteractionLog.objects.create(
        query_context=context,
        prompt_snippet=code_snippet[:500],
        ai_response=result.get("response", ""),
        model_used=result.get("model", "gemma2:2b"),
    )
    result["log_id"] = log.id
    return result


@shared_task(name="apps.ai_assistant.tasks.async_pr_review_bot")
def async_pr_review_bot(repo_name: str, pr_index: int, diff_content: str, title: str = "") -> dict:
    """
    T-PR-801 : Tache Celery pour l'execution autonome de revue de PR via Gemma 2 2B.
    """
    assistant = GemmaAssistant()
    review_res = assistant.generate_pr_summary(diff_content=diff_content, pr_title=title)

    verdict = "APPROVED"
    if "eval(" in diff_content or "exec(" in diff_content:
        verdict = "REQUEST_CHANGES"
    elif "password" in diff_content.lower() or "secret" in diff_content.lower():
        verdict = "COMMENT"

    comment_body = (
        f"### Revue Automatique BantuDevLab Copilot (Gemma 2 2B)\n\n"
        f"**Verdict** : `{verdict}`\n\n"
        f"{review_res.get('summary', '')}\n\n"
        f"---\n*Revue effectuee de facon souveraine en local*"
    )

    log = AIInteractionLog.objects.create(
        query_context=f"pr_review:{repo_name}#{pr_index}",
        prompt_snippet=diff_content[:500],
        ai_response=comment_body,
        model_used="gemma2:2b (PR Review Bot)",
    )

    return {
        "success": True,
        "repo": repo_name,
        "pr_index": pr_index,
        "verdict": verdict,
        "review_comment": comment_body,
        "log_id": log.id,
    }
