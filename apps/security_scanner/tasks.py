from celery import shared_task

from .engine import SecurityScannerEngine
from .models import SecurityAuditReport


@shared_task(name="apps.security_scanner.tasks.async_scan_code")
def async_scan_code(
    filename: str, content: str, repository_name: str = "sovereign-repo", actor: str = "anonymous-scanner"
) -> dict:
    """
    Tâche Celery asynchrone pour exécuter des scans de sécurité volumineux
    hors du cycle de requête HTTP de Django.
    """
    result = SecurityScannerEngine.scan_code(filename=filename, content=content)

    # Sauvegarde du rapport d'audit persistant
    report = SecurityAuditReport.objects.create(
        repository_name=repository_name,
        file_scanned=filename,
        total_issues=result["total_issues"],
        critical_count=result["critical"],
        high_count=result["high"],
        medium_count=result["medium"],
        sovereignty_score=result["sovereignty_score"],
        status_rating=result["status_rating"],
        raw_findings=result["issues"],
    )

    # Enregistrement dans l'audit trail
    from apps.core.audit import AuditTrail

    AuditTrail.record_event(
        action_type="VULN_SCAN",
        actor=actor,
        details={
            "repository": repository_name,
            "file_scanned": filename,
            "total_issues": result["total_issues"],
            "critical_count": result["critical"],
            "sovereignty_score": result["sovereignty_score"],
            "async_task": True,
        },
    )

    result["report_id"] = report.id
    return result
