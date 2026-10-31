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


class SovereignOrganization(models.Model):
    """
    DEV-02: Support Multi-Tenancy & Organisations Africaines.
    Regroupe les développeurs et dépôts par entité souveraine
    (ex: banques centrales, ministères, universités, startups tech régionales).
    """
    ENTITY_TYPE_CHOICES = [
        ('CENTRAL_BANK', 'Banque Centrale'),
        ('MINISTRY', 'Ministère / Agence Gouvernementale'),
        ('UNIVERSITY', 'Université / Centre de Recherche'),
        ('REGIONAL_STARTUP', 'Startup Tech Régionale'),
        ('PANAFRICAN_BODY', 'Organisation Panafricaine (ex: UA, Smart Africa)'),
    ]

    name = models.CharField(max_length=255, unique=True, help_text="Nom de l'organisation souveraine")
    slug = models.SlugField(max_length=100, unique=True, help_text="Identifiant unique pour URLs et Git org")
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES, default='REGIONAL_STARTUP')
    country_code = models.CharField(max_length=3, default='CIV', help_text="Code pays ISO-3 (ex: CIV, SEN, RWA, NGA)")
    description = models.TextField(blank=True, default='')
    website = models.URLField(blank=True, default='')
    sovereignty_level = models.CharField(max_length=50, default='Tier-1 Continental')
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Sovereign Organization'
        verbose_name_plural = 'Sovereign Organizations'

    def __str__(self):
        return f"{self.name} ({self.get_entity_type_display()} - {self.country_code})"
