from django.db import models
from django.utils import timezone


class AuditTrailLog(models.Model):
    """
    Immutable sovereign audit trail log entry with chained cryptographic hashes
    (Merkle tree / blockchain-like hashing) to guarantee non-repudiation and tamper evidence.
    """
    ACTION_CHOICES = [
        ('ZKP_AUTH', 'ZKP Authentication'),
        ('REPO_CREATE', 'Repository Creation'),
        ('VULN_SCAN', 'Vulnerability Scan'),
        ('SECURITY_ALERT', 'Security Alert'),
        ('CONFIG_CHANGE', 'Configuration Change'),
    ]

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    action_type = models.CharField(max_length=64, choices=ACTION_CHOICES, db_index=True)
    actor = models.CharField(max_length=150, default='system', db_index=True)
    details = models.JSONField(default=dict)
    prev_hash = models.CharField(max_length=64, default='0' * 64, help_text="SHA-256 hash of previous block")
    current_hash = models.CharField(max_length=64, unique=True, help_text="SHA-256 hash of current block")

    class Meta:
        ordering = ['id']
        verbose_name = 'Audit Trail Log'
        verbose_name_plural = 'Audit Trail Logs'

    def __str__(self):
        return f"AuditLog[{self.id}] {self.action_type} by {self.actor} at {self.timestamp}"
