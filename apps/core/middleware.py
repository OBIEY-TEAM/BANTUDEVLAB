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
    Supporte les requetes POST de selection de langue, le parametre URL ?lang=,
    les cookies 'django_language', 'bantu_lang' et le cookie Gitea 'lang'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.utils import translation

        target_lang = None

        # 0. Priorite absolue : POST explicite du formulaire set_language
        post_lang = request.POST.get("language")
        if post_lang and post_lang in GITEA_TO_DJANGO_LANG:
            target_lang = GITEA_TO_DJANGO_LANG[post_lang]

        # 1. Priorite : parametre d'URL ?lang=
        if not target_lang:
            param_lang = request.GET.get("lang")
            if param_lang and param_lang in GITEA_TO_DJANGO_LANG:
                target_lang = GITEA_TO_DJANGO_LANG[param_lang]

        # 2. Priorite : cookie standard django
        if not target_lang:
            django_cookie = request.COOKIES.get(getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language"))
            if django_cookie and django_cookie in GITEA_TO_DJANGO_LANG:
                target_lang = GITEA_TO_DJANGO_LANG[django_cookie]

        # 3. Priorite : cookie bantudevlab explicite
        if not target_lang:
            bantu_cookie = request.COOKIES.get("bantu_lang")
            if bantu_cookie and bantu_cookie in GITEA_TO_DJANGO_LANG:
                target_lang = GITEA_TO_DJANGO_LANG[bantu_cookie]

        # 4. Priorite : cookie gitea
        if not target_lang:
            gitea_cookie = request.COOKIES.get("lang")
            if gitea_cookie and gitea_cookie in GITEA_TO_DJANGO_LANG:
                target_lang = GITEA_TO_DJANGO_LANG[gitea_cookie]

        if target_lang:
            translation.activate(target_lang)
            request.LANGUAGE_CODE = target_lang

        response = self.get_response(request)

        # Respecter d'abord la langue choisie dans la reponse (ex: vue set_language)
        lang_cookie_name = getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language")
        resp_lang = response.cookies.get(lang_cookie_name)
        if resp_lang and resp_lang.value in GITEA_TO_DJANGO_LANG:
            active_short = GITEA_TO_DJANGO_LANG[resp_lang.value]
        else:
            active_lang = getattr(request, "LANGUAGE_CODE", None) or translation.get_language() or "fr"
            active_short = GITEA_TO_DJANGO_LANG.get(active_lang, "fr")

        active_gitea = DJANGO_TO_GITEA_LANG.get(active_short, "fr-FR")

        # Synchroniser tous les cookies de l'ecosysteme dans la reponse HTTP
        response.set_cookie(
            lang_cookie_name,
            active_short,
            max_age=31536000,
            path="/",
            samesite="Lax",
        )
        response.set_cookie("bantu_lang", active_short, max_age=31536000, path="/", samesite="Lax")
        response.set_cookie("lang", active_gitea, max_age=31536000, path="/", samesite="Lax")

        return response
