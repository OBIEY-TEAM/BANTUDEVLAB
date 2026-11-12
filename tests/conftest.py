"""Configuration pytest commune.

Depuis SEC-020, l'API exige l'authentification par defaut. Les anciens tests qui
utilisent `django.test.Client` sont donc executes avec un administrateur
connecte ; les tests d'acces anonyme utilisent explicitement
`rest_framework.test.APIClient` (sous-classe, jamais auto-authentifie).
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture(autouse=True)
def _authenticated_default_client(monkeypatch):
    original_request = Client.request

    def request(self, **kwargs):
        if type(self) is Client and not getattr(self, "_auto_logged", False):
            self._auto_logged = True
            user, _ = User.objects.get_or_create(
                username="__test_admin__", defaults={"is_staff": True, "is_superuser": True}
            )
            self.force_login(user)
        return original_request(self, **kwargs)

    monkeypatch.setattr(Client, "request", request)


@pytest.fixture(autouse=True)
def _clear_cache():
    """Isole les tests : throttling DRF, circuit breaker Gitea et caches vivent dans le cache."""
    from django.core.cache import cache

    try:
        cache.clear()
    except Exception:
        pass
    yield
    try:
        cache.clear()
    except Exception:
        pass
