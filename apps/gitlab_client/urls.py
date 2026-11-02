from django.urls import path
from apps.gitlab_client.views import gitlab_webhook_receiver

app_name = "gitlab_client"

urlpatterns = [
    path("webhook/", gitlab_webhook_receiver, name="gitlab_webhook"),
]
