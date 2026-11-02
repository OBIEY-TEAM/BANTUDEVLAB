"""Initialisation des tests pour BantuDevLab.

Depuis SEC-020, l'API exige l'authentification par défaut.
Afin d'assurer la cohérence stricte entre `pytest` et `manage.py test`,
`django.test.Client.request` auto-authentifie un utilisateur administrateur
pour les tests classiques utilisant `Client`, tandis que les tests testant
l'accès anonyme ou un utilisateur spécifique utilisent explicitement
`rest_framework.test.APIClient` (sous-classe de Client).
"""

from django.contrib.auth.models import User
from django.test import Client

_orig_client_request = Client.request


def _patched_client_request(self, **kwargs):
    if type(self) is Client and not getattr(self, "_auto_logged", False):
        self._auto_logged = True
        try:
            user, _ = User.objects.get_or_create(
                username="__test_admin__", defaults={"is_staff": True, "is_superuser": True}
            )
            self.force_login(user)
        except Exception:
            pass
    return _orig_client_request(self, **kwargs)


Client.request = _patched_client_request
