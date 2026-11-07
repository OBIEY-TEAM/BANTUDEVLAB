from django.conf import settings

from config.base_urls import (
    AI_URL,
    BASE_URL_1,
    BASE_URL_2,
    BASE_URL_3,
    FORGE_INTERNAL_URL,
    GITEA_WEB_URL,
)


def forge_context(request):
    """Fournit les URLs et métadonnées de la Forge Git Souveraine aux templates."""
    gitea_external = getattr(settings, "GITEA_EXTERNAL_URL", GITEA_WEB_URL).rstrip("/")
    gitlab_url = getattr(settings, "GITLAB_URL", BASE_URL_2).rstrip("/")
    return {
        "BASE_URL_1": getattr(settings, "BASE_URL_1", BASE_URL_1),
        "BASE_URL_2": getattr(settings, "BASE_URL_2", BASE_URL_2),
        "BASE_URL_3": getattr(settings, "BASE_URL_3", BASE_URL_3),
        "PORTAL_URL": getattr(settings, "BASE_URL_1", BASE_URL_1),
        "FORGE_URL": getattr(settings, "BASE_URL_2", BASE_URL_2),
        "API_URL": getattr(settings, "BASE_URL_3", BASE_URL_3),
        "GITEA_WEB_URL": getattr(settings, "GITEA_WEB_URL", GITEA_WEB_URL),
        "FORGE_INTERNAL_URL": getattr(settings, "FORGE_INTERNAL_URL", FORGE_INTERNAL_URL),
        "AI_URL": getattr(settings, "AI_URL", AI_URL),
        "GITEA_EXTERNAL_URL": gitea_external,
        "GITEA_LOGIN_URL": getattr(settings, "GITEA_LOGIN_URL", f"{gitea_external}/user/login"),
        "GITEA_API_URL": getattr(settings, "GITEA_API_URL", f"{gitea_external}/api/v1"),
        "GITLAB_URL": gitlab_url,
    }
