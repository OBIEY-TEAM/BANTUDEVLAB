from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

try:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

    has_spectacular = True
except (ImportError, ModuleNotFoundError):
    has_spectacular = False

from apps.zkp_auth.views import ZKPOpenIDConfigurationView
from config.base_urls import BASE_URL_2, GITEA_WEB_URL


class DynamicGiteaRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        gitea_url = getattr(settings, "GITEA_LOGIN_URL", f"{GITEA_WEB_URL}/user/login")
        return gitea_url or BASE_URL_2


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # I18N-01: Switch langue
    path("admin/", admin.site.urls),
    # Point de decouverte OIDC racine
    path(".well-known/openid-configuration", ZKPOpenIDConfigurationView.as_view(), name="root_openid_configuration"),
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
]

if has_spectacular:
    # DEV-04: Documentation OpenAPI & Swagger UI
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]

# Servir les fichiers statiques : fallback robuste avec django.views.static.serve
# permettant le chargement direct du CSS et des assets statiques dans tous les environnements
static_doc_root = (
    settings.STATIC_ROOT
    if (getattr(settings, "STATIC_ROOT", None) and getattr(settings, "STATIC_ROOT").exists())
    else settings.STATICFILES_DIRS[0]
)

urlpatterns += [
    re_path(
        r"^%s(?P<path>.*)$" % settings.STATIC_URL.lstrip("/"),
        serve,
        {"document_root": static_doc_root},
        name="static_serve",
    ),
]
