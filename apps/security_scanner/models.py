from django.db import models


class SecurityAuditReport(models.Model):
    repository_name = models.CharField(max_length=255, db_index=True)
    file_scanned = models.CharField(max_length=255, default="all")
    total_issues = models.IntegerField(default=0)
    critical_count = models.IntegerField(default=0)
    high_count = models.IntegerField(default=0)
    medium_count = models.IntegerField(default=0)
    sovereignty_score = models.IntegerField(default=100)
    status_rating = models.CharField(max_length=50, default="EXCELLENT")
    raw_findings = models.JSONField(default=list)
    scanned_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["scanned_at"], name="sec_scanned_idx"),
            models.Index(fields=["repository_name"], name="sec_repo_idx"),
        ]

    def __str__(self):
        return (
            f"Audit {self.repository_name} ({self.sovereignty_score}%) - {self.scanned_at.strftime('%Y-%m-%d %H:%M')}"
        )
