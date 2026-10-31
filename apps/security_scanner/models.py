from django.db import models

class SecurityAuditReport(models.Model):
    repository_name = models.CharField(max_length=255)
    file_scanned = models.CharField(max_length=255, default='all')
    total_issues = models.IntegerField(default=0)
    critical_count = models.IntegerField(default=0)
    high_count = models.IntegerField(default=0)
    medium_count = models.IntegerField(default=0)
    sovereignty_score = models.IntegerField(default=100)
    status_rating = models.CharField(max_length=50, default='EXCELLENT')
    raw_findings = models.JSONField(default=list)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit {self.repository_name} ({self.sovereignty_score}%) - {self.scanned_at.strftime('%Y-%m-%d %H:%M')}"
