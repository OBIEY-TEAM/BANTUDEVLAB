from django.conf import settings
from django.http import HttpResponse

GITEA_TO_DJANGO_LANG = {
    "fr-FR": "fr",
    "en-US": "en",
    "sw-KE": "sw",
    "pt-PT": "pt",
    "fr": "fr",
    "en": "en",
    "sw": "sw",
    "pt": "pt",
}

DJANGO_TO_GITEA_LANG = {
    "fr": "fr-FR",
    "en": "en-US",
    "sw": "sw-KE",
    "pt": "pt-PT",
}


class SecurityHeadersMiddleware:
    """
    Middleware injecting hardened HTTP security headers, Content-Security-Policy (CSP),
    and CORS headers for forge interoperability.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Handle CORS preflight OPTIONS requests for API endpoints
        if request.method == "OPTIONS" and request.path.startswith("/api/"):
            response = HttpResponse(status=200)
            origin = request.headers.get("Origin", "*")
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = (
                "Authorization, Content-Type, X-CSRFToken, X-Requested-With, Accept, Origin, User-Agent"
            )
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Max-Age"] = "86400"
            return response

        response = self.get_response(request)

        # Inject Content-Security-Policy
        csp = getattr(settings, "CSP_POLICY", "default-src 'self'; frame-ancestors 'none';")
        response["Content-Security-Policy"] = csp

        # Additional standard security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Inject CORS headers for API endpoints
        if request.path.startswith("/api/"):
            origin = request.headers.get("Origin", "*")
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = (
                "Authorization, Content-Type, X-CSRFToken, X-Requested-With, Accept, Origin, User-Agent"
            )
            response["Access-Control-Allow-Credentials"] = "true"

        return response


class EcosystemI18nMiddleware:
    """
    Middleware assurant la synchronisation universelle et transparente
    de langue entre BantuDevLab, Gitea et GitLab Forge.
    Supporte le parametre URL ?lang=, les cookies 'django_language',
    'bantu_lang' et le cookie Gitea 'lang'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.utils import translation

        target_lang = None

        # 1. Priorite : parametre POST ou GET 'language' / 'lang'
        explicit_lang = request.POST.get("language") or request.GET.get("language") or request.GET.get("lang")
        if explicit_lang and explicit_lang in GITEA_TO_DJANGO_LANG:
            target_lang = GITEA_TO_DJANGO_LANG[explicit_lang]

        # 2. Priorite : cookie bantudevlab explicite
        if not target_lang:
            bantu_cookie = request.COOKIES.get("bantu_lang")
            if bantu_cookie and bantu_cookie in GITEA_TO_DJANGO_LANG:
                target_lang = GITEA_TO_DJANGO_LANG[bantu_cookie]

        # 3. Priorite : cookie gitea
        if not target_lang:
            gitea_cookie = request.COOKIES.get("lang")
            if gitea_cookie and gitea_cookie in GITEA_TO_DJANGO_LANG:
                target_lang = GITEA_TO_DJANGO_LANG[gitea_cookie]

        # 4. Priorite : cookie standard django
        if not target_lang:
            django_cookie = request.COOKIES.get(getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language"))
            if django_cookie and django_cookie in GITEA_TO_DJANGO_LANG:
                target_lang = GITEA_TO_DJANGO_LANG[django_cookie]

        if target_lang:
            translation.activate(target_lang)
            request.LANGUAGE_CODE = target_lang

        response = self.get_response(request)

        # Synchroniser tous les cookies de langue dans la reponse HTTP
        resp_lang = None
        if hasattr(response, "cookies") and response.cookies.get("django_language"):
            resp_lang = response.cookies["django_language"].value
        elif hasattr(response, "cookies") and response.cookies.get("bantu_lang"):
            resp_lang = response.cookies["bantu_lang"].value

        active_lang = resp_lang or getattr(request, "LANGUAGE_CODE", None) or translation.get_language() or "fr"
        active_short = GITEA_TO_DJANGO_LANG.get(active_lang, "fr")
        active_gitea = DJANGO_TO_GITEA_LANG.get(active_short, "fr-FR")

        response.set_cookie(
            getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language"),
            active_short,
            max_age=31536000,
            path="/",
            samesite="Lax",
        )
        response.set_cookie("bantu_lang", active_short, max_age=31536000, path="/", samesite="Lax")
        response.set_cookie("lang", active_gitea, max_age=31536000, path="/", samesite="Lax")

        return response
