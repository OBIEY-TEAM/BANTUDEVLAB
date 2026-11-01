from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("healthz", views.healthz_view, name="healthz"),
    path("readyz", views.readyz_view, name="readyz"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("metrics/", views.metrics_view, name="metrics"),
    path("sovereignty-metrics/", views.metrics_view, name="sovereignty_metrics"),
    path("api/organizations/", views.SovereignOrganizationListCreateView.as_view(), name="organizations"),
]
