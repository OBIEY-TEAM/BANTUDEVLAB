import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'bantudevlab-sovereign-secret-key-insecure-dev-only-2025')

DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'apps.core',
    'apps.zkp_auth',
    'apps.gitea_client',
    'apps.security_scanner',
    'apps.ai_assistant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'apps.core.middleware.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database configuration: support PostgreSQL with SQLite fallback
DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite')
if DB_ENGINE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'bantudevlab'),
            'USER': os.environ.get('POSTGRES_USER', 'bantudevlab_admin'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'sovereign_pass_2025'),
            'HOST': os.environ.get('POSTGRES_HOST', 'db'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'zkp': '5/minute',
        'scanner': '10/minute',
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'BantuDevLab Sovereign Forge API',
    'DESCRIPTION': 'Documentation interactive OpenAPI 3.0 des endpoints de la forge logicielle souveraine panafricaine (ZKP, Forge, Scanner de sécurité et Assistant IA Gemma 5B).',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# Security Hardening: En-têtes HTTP & Cookies (SEC-05)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Cookies Hardening
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Content Security Policy (CSP)
CSP_POLICY = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data:; font-src 'self' https://cdnjs.cloudflare.com; frame-ancestors 'none';"

# Gitea / Forge Sovereign Integration
GITEA_API_URL = os.environ.get('GITEA_API_URL', 'http://localhost:3000/api/v1')
GITEA_ADMIN_TOKEN = os.environ.get('GITEA_ADMIN_TOKEN', '')
GITEA_EXTERNAL_URL = os.environ.get('GITEA_EXTERNAL_URL', 'http://localhost:3000')
GITEA_WEBHOOK_SECRET = os.environ.get('GITEA_WEBHOOK_SECRET', 'sovereign_webhook_secret_key_2025')

# Gemma 5B Sovereign Assistant Configuration
GEMMA_API_URL = os.environ.get('GEMMA_API_URL', 'http://localhost:11434/api/generate')
GEMMA_MODEL_NAME = os.environ.get('GEMMA_MODEL_NAME', 'gemma:5b')
GEMMA_EMBEDDINGS_URL = os.environ.get('GEMMA_EMBEDDINGS_URL', 'http://localhost:11434/api/embeddings')

# Celery / Redis Task Queue Configuration (PERF-01)
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', REDIS_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Distributed Caching Layer (PERF-04)
def _get_cache_configuration():
    redis_url = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
    import sys
    if 'test' in sys.argv or os.environ.get('REDIS_CACHE_ENABLED', '').lower() in ('false', '0'):
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'bantudevlab-cache',
                'TIMEOUT': 60,
            }
        }
    try:
        import redis
        client = redis.Redis.from_url(redis_url, socket_connect_timeout=0.2)
        client.ping()
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': redis_url,
                'TIMEOUT': 60,
            }
        }
    except Exception:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'bantudevlab-cache',
                'TIMEOUT': 60,
            }
        }

CACHES = _get_cache_configuration()
