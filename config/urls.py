from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('api/zkp/', include('apps.zkp_auth.urls')),
    path('api/forge/', include('apps.gitea_client.urls')),
    path('api/security/', include('apps.security_scanner.urls')),
    path('api/ai/', include('apps.ai_assistant.urls')),
]
