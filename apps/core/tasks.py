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
    T-DEV-502 : Tâche Celery périodique rafraîchissant les dépôts GitLab et Gitea
    dans le cache Redis toutes les 30 secondes en tâche de fond.
    """
    try:
        from apps.gitea_client.client import GiteaClient
        from apps.gitlab_client.client import GitLabClient

        gitlab_repos = GitLabClient().list_repositories()
        gitea_repos = GiteaClient().list_repositories()
        repos = gitlab_repos or gitea_repos or []

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
