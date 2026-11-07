from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from config.base_urls import BASE_URL_2, GITEA_WEB_URL


class DynamicGiteaRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        gitea_url = getattr(settings, "GITEA_LOGIN_URL", f"{GITEA_WEB_URL}/user/login")
        return gitea_url or BASE_URL_2


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # I18N-01: Switch langue
    path("admin/", admin.site.urls),
    # Redirections dynamiques vers Gitea Native
    path("gitea/", DynamicGiteaRedirectView.as_view(), name="redirect_gitea"),
    path("switch-gitea/", DynamicGiteaRedirectView.as_view(), name="switch_gitea"),
    path("basculer-gitea/", DynamicGiteaRedirectView.as_view(), name="basculer_gitea"),
    path("", include("apps.core.urls")),
    path("api/zkp/", include("apps.zkp_auth.urls")),
    path("api/forge/", include("apps.gitea_client.urls")),
    path("api/gitlab/", include("apps.gitlab_client.urls")),
    path("api/security/", include("apps.security_scanner.urls")),
    path("api/ai/", include("apps.ai_assistant.urls")),
    # DEV-04: Documentation OpenAPI & Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Servir les fichiers statiques en dev ou testing
if settings.DEBUG or getattr(settings, "TESTING", False):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
