"""
Tâches asynchrones et périodiques Celery pour l'application core (BantuDevLab).
"""

import logging

from celery import shared_task
from django.core.cache import cache

logger = logging.getLogger("bantudevlab.security")

FORGE_REPOS_CACHE_KEY = "bantudevlab_forge_repos_cache"


@shared_task(name="apps.core.tasks.sync_forge_repositories_cache")
def sync_forge_repositories_cache() -> int:
    """
    T-DEV-502 : Tâche Celery périodique rafraîchissant les dépôts Gitea CE
    dans le cache Valkey/Redis toutes les 30 secondes en tâche de fond.
    """
    try:
        from apps.gitea_client.client import GiteaClient

        repos = GiteaClient().list_repositories() or []

        cache.set(FORGE_REPOS_CACHE_KEY, repos, 60)
        logger.info("T-DEV-502 : Cache des dépôts synchronisé avec succès (%d dépôts).", len(repos))
        return len(repos)
    except Exception as exc:
        logger.warning("T-DEV-502 : Échec du rafraîchissement asynchrone des dépôts forge : %s", exc)
        return 0


@shared_task(name="apps.core.tasks.verify_audit_chain_nightly")
def verify_audit_chain_nightly() -> bool:
    """
    T-DEV-503 : Tâche Celery planifiée chaque nuit pour certifier la chaîne
    d'audit immuable SHA-256 sans saturer la mémoire du serveur.
    """
    try:
        from .audit import AuditTrail

        is_valid = AuditTrail.verify_chain_integrity()
        if is_valid:
            logger.info("T-DEV-503 : Certification nocturne réussie - Intégrité de la chaîne Malabo validée.")
        else:
            logger.critical(
                "T-DEV-503 : ALERTE CRITIQUE - Rupture d'intégrité détectée dans la chaîne d'audit Malabo !"
            )
        return is_valid
    except Exception as exc:
        logger.error("T-DEV-503 : Erreur lors de la vérification de la chaîne d'audit : %s", exc)
        return False


@shared_task(name="apps.core.tasks.cleanup_demo_repositories")
def cleanup_demo_repositories(max_age_hours: int = 24) -> int:
    """
    Nettoie automatiquement les dépôts de démonstration créés par cadev_evaluator
    au-delà de `max_age_hours` heures et invalide le cache associé.
    """
    try:
        from datetime import timedelta
        from django.utils import timezone
        from apps.gitea_client.models import SovereignRepository

        cutoff = timezone.now() - timedelta(hours=max_age_hours)
        deleted_count, _ = SovereignRepository.objects.filter(
            owner="cadev_evaluator", created_at__lt=cutoff
        ).delete()
        if deleted_count:
            cache.delete(FORGE_REPOS_CACHE_KEY)
            cache.delete("gitea_repos_list")
            logger.info("Nettoyage démo : %d dépôt(s) cadev_evaluator expiré(s) supprimé(s).", deleted_count)
        return deleted_count
    except Exception as exc:
        logger.warning("Nettoyage démo : échec de la purge automatique : %s", exc)
        return 0
