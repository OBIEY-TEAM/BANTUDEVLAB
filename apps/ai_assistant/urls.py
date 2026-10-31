from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('review/', views.GemmaCodeReviewView.as_view(), name='gemma_review'),
    path('status/', views.GemmaStatusView.as_view(), name='gemma_status'),
]
