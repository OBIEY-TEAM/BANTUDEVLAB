from django.conf import settings


def forge_context(request):
    """Fournit les URLs et métadonnées de la Forge Git Souveraine aux templates."""
    gitea_external = getattr(settings, "GITEA_EXTERNAL_URL", "http://localhost:3002").rstrip("/")
    return {
        "GITEA_EXTERNAL_URL": gitea_external,
        "GITEA_LOGIN_URL": getattr(settings, "GITEA_LOGIN_URL", f"{gitea_external}/user/login"),
        "GITEA_API_URL": getattr(settings, "GITEA_API_URL", f"{gitea_external}/api/v1"),
        "GITLAB_URL": getattr(settings, "GITLAB_URL", "http://localhost:3001"),
    }
