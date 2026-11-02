from django.urls import path

from . import views

app_name = "ai_assistant"

urlpatterns = [
    path("review/", views.GemmaCodeReviewView.as_view(), name="gemma_review"),
    path("status/", views.GemmaStatusView.as_view(), name="gemma_status"),
    path("copilot/explain/", views.CopilotExplainView.as_view(), name="copilot_explain"),
    path("copilot/complete/", views.CopilotCompleteView.as_view(), name="copilot_complete"),
    path("copilot/pr-summary/", views.CopilotPRSummaryView.as_view(), name="copilot_pr_summary"),
]
