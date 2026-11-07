from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("health", views.healthz_view, name="health"),
    path("healthz", views.healthz_view, name="healthz"),
    path("readyz", views.readyz_view, name="readyz"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("metrics/", views.metrics_view, name="metrics"),
    path("sovereignty-metrics/", views.metrics_view, name="sovereignty_metrics"),
    path("faq/", views.faq_view, name="faq"),
    path("api/organizations/", views.SovereignOrganizationListCreateView.as_view(), name="organizations"),
]
