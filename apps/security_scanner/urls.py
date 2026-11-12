from django.urls import path

from . import views

app_name = "security_scanner"

urlpatterns = [
    path("scan/", views.ScanCodeView.as_view(), name="scan_code"),
    path("audits/", views.SecurityAuditHistoryView.as_view(), name="audit_history"),
    path("sarif/", views.SecuritySarifExportView.as_view(), name="sarif_export_latest"),
    path("audits/<int:report_id>/sarif/", views.SecuritySarifExportView.as_view(), name="sarif_export_report"),
    path("gitlab-sast/", views.SecurityGitLabSastExportView.as_view(), name="gitlab_sast_latest"),
    path(
        "audits/<int:report_id>/gitlab-sast/", views.SecurityGitLabSastExportView.as_view(), name="gitlab_sast_report"
    ),
]
