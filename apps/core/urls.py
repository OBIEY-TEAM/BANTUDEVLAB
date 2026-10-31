from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('metrics/', views.metrics_view, name='metrics'),
    path('sovereignty-metrics/', views.metrics_view, name='sovereignty_metrics'),
]
