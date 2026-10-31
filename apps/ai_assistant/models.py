from django.db import models


class AIInteractionLog(models.Model):
    query_context = models.CharField(max_length=100, default="code_review")
    prompt_snippet = models.TextField()
    ai_response = models.TextField()
    model_used = models.CharField(max_length=100, default="gemma:5b")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AIInteraction {self.query_context} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
