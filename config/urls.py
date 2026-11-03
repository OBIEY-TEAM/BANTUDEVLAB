from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

try:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

    has_spectacular = True
except (ImportError, ModuleNotFoundError):
    has_spectacular = False

from apps.zkp_auth.views import ZKPOpenIDConfigurationView

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # I18N-01: Switch langue
    path("admin/", admin.site.urls),
    # Point de decouverte OIDC racine
    path(".well-known/openid-configuration", ZKPOpenIDConfigurationView.as_view(), name="root_openid_configuration"),
    # Redirections directes vers Gitea Native (3002)
    path(
        "gitea/", RedirectView.as_view(url="http://localhost:3002/user/login", permanent=False), name="redirect_gitea"
    ),
    path(
        "switch-gitea/",
        RedirectView.as_view(url="http://localhost:3002/user/login", permanent=False),
        name="switch_gitea",
    ),
    path(
        "basculer-gitea/",
        RedirectView.as_view(url="http://localhost:3002/user/login", permanent=False),
        name="basculer_gitea",
    ),
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
