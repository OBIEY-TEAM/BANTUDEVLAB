import os
import sys
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

try:
    from dotenv import load_dotenv

    load_dotenv()
except (ImportError, ModuleNotFoundError):
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

TESTING = (
    any(cmd in sys.argv for cmd in ("test", "pytest", "check", "makemigrations", "migrate")) or "pytest" in sys.modules
)

# SEC-011: DEBUG desactive par defaut (opt-in explicite pour le developpement).
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

# SEC-010: aucun secret par defaut en production.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG or TESTING:
        SECRET_KEY = "insecure-dev-only-key-do-not-use-in-production"  # nosec B105
    else:
        raise ImproperlyConfigured("DJANGO_SECRET_KEY doit etre defini (voir .env.example).")

# (DEBUG est defini plus haut)

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "apps.core",
    "apps.zkp_auth",
    "apps.gitea_client",
    "apps.gitlab_client",
    "apps.security_scanner",
    "apps.ai_assistant",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "apps.core.middleware.SecurityHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # I18N-01
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": ["apps.core.templatetags.icons"],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.forge_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database configuration: support PostgreSQL with SQLite fallback
DB_ENGINE = os.environ.get("DB_ENGINE", "sqlite")
if DB_ENGINE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "bantudevlab"),
            "USER": os.environ.get("POSTGRES_USER", "bantudevlab_admin"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "db"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
    ("sw", "Kiswahili"),
    ("pt", "Português"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "1000/day",
        "zkp": "5/minute",
        "scanner": "10/minute",
        "zkp_register": "10/hour",
        "ai": "20/minute",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "BantuDevLab Sovereign Forge API",
    "DESCRIPTION": "Documentation interactive OpenAPI 3.0 des endpoints de la forge logicielle souveraine panafricaine (ZKP, Forge, Scanner de securite et Assistant IA Gemma 2 2B).",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}

# Security Hardening: En-têtes HTTP & Cookies (SEC-05)
SECURE_BROWSER_XSS_FILTER = False  # obsolete (supprime en Django 5.x) : la CSP prend le relais
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Cookies Hardening
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax" if (DEBUG or TESTING) else "Strict")
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = os.environ.get("CSRF_COOKIE_SAMESITE", "Lax" if (DEBUG or TESTING) else "Strict")

# SEC-041: durcissement transport en production (HTTPS strict, HSTS, cookies Secure).
if not (DEBUG or TESTING):
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1", "yes")
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o]
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # SEC-043: corps de requete limite a 1 Mo

# Content Security Policy (CSP)
CSP_POLICY = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; frame-ancestors 'none';"

# Gitea / Forge Sovereign Integration
GITEA_API_URL = os.environ.get("GITEA_API_URL", "http://localhost:3002/api/v1")
GITEA_ADMIN_TOKEN = os.environ.get("GITEA_ADMIN_TOKEN", "")
GITEA_EXTERNAL_URL = os.environ.get("GITEA_EXTERNAL_URL", "http://localhost:3002")
GITEA_LOGIN_URL = os.environ.get("GITEA_LOGIN_URL", "http://localhost:3002/user/login")
GITEA_WEBHOOK_SECRET = os.environ.get(
    "GITEA_WEBHOOK_SECRET", "bantu_dev_webhook_secret_key_2026" if (DEBUG or TESTING) else ""
)

# GitLab Sovereign Enterprise Integration
GITLAB_URL = os.environ.get("GITLAB_URL", "http://localhost:3001")
GITLAB_PRIVATE_TOKEN = os.environ.get("GITLAB_PRIVATE_TOKEN", "")
GITLAB_WEBHOOK_SECRET = os.environ.get("GITLAB_WEBHOOK_SECRET", "bantu_gitlab_webhook_secret_2026")

# Gemma 2 2B Sovereign Assistant Configuration
GEMMA_API_URL = os.environ.get("GEMMA_API_URL", "http://localhost:11434/api/generate")
GEMMA_MODEL_NAME = os.environ.get("GEMMA_MODEL_NAME", "gemma2:2b")
GEMMA_EMBEDDINGS_URL = os.environ.get("GEMMA_EMBEDDINGS_URL", "http://localhost:11434/api/embeddings")

# Celery / Redis Task Queue Configuration (PERF-01)
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", REDIS_URL)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Celery Beat Periodic Tasks (T-DEV-502, T-DEV-503, T-DEV-504)
CELERY_BEAT_SCHEDULE = {
    "sync-forge-repositories-cache-every-30s": {
        "task": "apps.core.tasks.sync_forge_repositories_cache",
        "schedule": 30.0,
    },
    "verify-audit-chain-nightly": {
        "task": "apps.core.tasks.verify_audit_chain_nightly",
        "schedule": 86400.0,
    },
    "purge-expired-zkp-challenges-every-15m": {
        "task": "apps.zkp_auth.tasks.purge_expired_zkp_challenges",
        "schedule": 900.0,
    },
}


# Distributed Caching Layer (PERF-04)
def _get_cache_configuration():
    redis_url = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
    import sys

    if "test" in sys.argv or os.environ.get("REDIS_CACHE_ENABLED", "").lower() in ("false", "0"):
        return {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "bantudevlab-cache",
                "TIMEOUT": 60,
            }
        }
    try:
        import redis

        client = redis.Redis.from_url(redis_url, socket_connect_timeout=0.2)
        client.ping()
        return {
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": redis_url,
                "TIMEOUT": 60,
            }
        }
    except Exception:
        return {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "bantudevlab-cache",
                "TIMEOUT": 60,
            }
        }


CACHES = _get_cache_configuration()
