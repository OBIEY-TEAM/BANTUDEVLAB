from django.conf import settings


class SecurityHeadersMiddleware:
    """
    Middleware injecting hardened HTTP security headers, including Content-Security-Policy (CSP).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Inject Content-Security-Policy
        csp = getattr(settings, "CSP_POLICY", "default-src 'self'; frame-ancestors 'none';")
        response["Content-Security-Policy"] = csp

        # Additional standard security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
