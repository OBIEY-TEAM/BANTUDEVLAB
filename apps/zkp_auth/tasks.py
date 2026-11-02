"""
Tâches Celery pour l'authentification Zero-Knowledge Proof (ZKP).
"""

import logging

from celery import shared_task

from .models import ZKPChallenge

logger = logging.getLogger("bantudevlab.security")


@shared_task(name="apps.zkp_auth.tasks.purge_expired_zkp_challenges")
def purge_expired_zkp_challenges(max_age_minutes: int = 10) -> int:
    """
    T-DEV-504 : Purge automatique périodique des challenges ZKP expirés.
    Planifié toutes les 15 minutes via Celery Beat pour prévenir l'accumulation de nonces (anti-DoS).
    """
    try:
        count = ZKPChallenge.purge_expired_challenges(max_age_minutes=max_age_minutes)
        logger.info("T-DEV-504 : %d challenge(s) ZKP expire(s) purge(s) avec succes.", count)
        return count
    except Exception as exc:
        logger.error("T-DEV-504 : Erreur lors de la purge des challenges ZKP : %s", exc)
        return 0
