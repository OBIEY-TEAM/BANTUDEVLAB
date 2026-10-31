from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('api/zkp/', include('apps.zkp_auth.urls')),
    path('api/forge/', include('apps.gitea_client.urls')),
    path('api/security/', include('apps.security_scanner.urls')),
    path('api/ai/', include('apps.ai_assistant.urls')),
    # DEV-04: Documentation OpenAPI & Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
