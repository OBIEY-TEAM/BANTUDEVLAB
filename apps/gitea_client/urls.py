from django.urls import path

from . import views

app_name = "gitea_client"

urlpatterns = [
    path("repositories/", views.RepositoryListView.as_view(), name="repositories"),
    path("status/", views.ForgeStatusView.as_view(), name="forge_status"),
    path("webhook/", views.GiteaWebhookReceiverView.as_view(), name="gitea_webhook"),
    path("sync/", views.GiteaSyncView.as_view(), name="gitea_sync"),
]
