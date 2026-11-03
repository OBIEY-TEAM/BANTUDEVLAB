from django.conf import settings
from django.http import HttpResponse


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
