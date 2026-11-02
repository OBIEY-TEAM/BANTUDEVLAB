from django.conf import settings


def forge_context(request):
    """Fournit les URLs et métadonnées de la Forge Git Souveraine aux templates."""
    return {
        "GITEA_EXTERNAL_URL": getattr(settings, "GITEA_EXTERNAL_URL", "http://localhost:3001"),
        "GITEA_API_URL": getattr(settings, "GITEA_API_URL", "http://localhost:3001/api/v1"),
        "GITLAB_URL": getattr(settings, "GITLAB_URL", "http://localhost:3001"),
    }
