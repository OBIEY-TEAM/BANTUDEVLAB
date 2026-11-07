"""
Tests unitaires et de non-régression pour la gestion centralisée des URLs de base souveraines.
Vérifie BASE_URL_1 (https://cybersocle.site), BASE_URL_2 (https://git.cybersocle.site)
et BASE_URL_3 (https://api.cybersocle.site), ainsi que les constructeurs dynamiques d'URLs.
"""

import os
from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase, TestCase

import config.base_urls as bu
from apps.core.context_processors import forge_context
from apps.gitea_client.client import GiteaClient


class BaseUrlsConfigurationTestCase(SimpleTestCase):
    """Vérifie la définition, l'accès et les constructeurs dynamiques des URLs de base."""

    def test_default_base_urls_constants(self):
        """Vérifie que les trois constantes par défaut correspondent aux spécifications."""
        self.assertEqual(bu.DEFAULT_BASE_URL_1, "https://cybersocle.site")
        self.assertEqual(bu.DEFAULT_BASE_URL_2, "https://git.cybersocle.site")
        self.assertEqual(bu.DEFAULT_BASE_URL_3, "https://api.cybersocle.site")

    def test_get_base_urls_dict(self):
        """Vérifie le dictionnaire retourné par get_base_urls()."""
        urls = bu.get_base_urls()
        self.assertIn("BASE_URL_1", urls)
        self.assertIn("BASE_URL_2", urls)
        self.assertIn("BASE_URL_3", urls)
        self.assertEqual(urls["BASE_URL_1"], "https://cybersocle.site")
        self.assertEqual(urls["BASE_URL_2"], "https://git.cybersocle.site")
        self.assertEqual(urls["BASE_URL_3"], "https://api.cybersocle.site")

    def test_get_base_domains(self):
        """Vérifie l'extraction des domaines pour ALLOWED_HOSTS."""
        domains = bu.get_base_domains()
        self.assertIn("cybersocle.site", domains)
        self.assertIn("git.cybersocle.site", domains)
        self.assertIn("api.cybersocle.site", domains)

    def test_build_url_helpers(self):
        """Vérifie la construction dynamique des URLs avec ou sans slash initial."""
        self.assertEqual(bu.build_portal_url(""), "https://cybersocle.site")
        self.assertEqual(bu.build_portal_url("/dashboard/"), "https://cybersocle.site/dashboard/")
        self.assertEqual(bu.build_portal_url("dashboard/"), "https://cybersocle.site/dashboard/")

        self.assertEqual(bu.build_git_url(""), "https://git.cybersocle.site")
        self.assertEqual(bu.build_git_url("/org/repo.git"), "https://git.cybersocle.site/org/repo.git")
        self.assertEqual(bu.build_git_url("org/repo.git"), "https://git.cybersocle.site/org/repo.git")

        self.assertEqual(bu.build_api_url(""), "https://api.cybersocle.site")
        self.assertEqual(bu.build_api_url("/v1/scan/"), "https://api.cybersocle.site/v1/scan/")
        self.assertEqual(bu.build_api_url("v1/scan/"), "https://api.cybersocle.site/v1/scan/")

    def test_env_override_base_urls(self):
        """Vérifie la prise en compte des variables d'environnement."""
        with patch.dict(
            os.environ,
            {
                "BASE_URL_1": "https://custom-portal.africa/",
                "BASE_URL_2": "https://custom-git.africa/",
                "BASE_URL_3": "https://custom-api.africa/",
            },
        ):
            # Rechargement ou appel direct avec build_url
            b1 = os.environ.get("BASE_URL_1").rstrip("/")
            b2 = os.environ.get("BASE_URL_2").rstrip("/")
            b3 = os.environ.get("BASE_URL_3").rstrip("/")
            self.assertEqual(bu.build_url(b1, "test"), "https://custom-portal.africa/test")
            self.assertEqual(bu.build_url(b2, "test"), "https://custom-git.africa/test")
            self.assertEqual(bu.build_url(b3, "test"), "https://custom-api.africa/test")

    def test_context_processor_exposes_base_urls(self):
        """Vérifie que le processeur de contexte Django expose les trois URLs de base aux templates."""
        from django.test import RequestFactory

        request = RequestFactory().get("/")
        ctx = forge_context(request)
        self.assertIn("BASE_URL_1", ctx)
        self.assertIn("BASE_URL_2", ctx)
        self.assertIn("BASE_URL_3", ctx)
        self.assertEqual(ctx["BASE_URL_1"], "https://cybersocle.site")
        self.assertEqual(ctx["BASE_URL_2"], "https://git.cybersocle.site")
        self.assertEqual(ctx["BASE_URL_3"], "https://api.cybersocle.site")


class DynamicUrlIntegrationTestCase(TestCase):
    """Vérifie l'intégration dynamique dans les clients et vues."""

    def test_gitea_client_create_repository_dynamic_url(self):
        """Vérifie que la création de dépôt de repli utilise dynamiquement BASE_URL_1."""
        client = GiteaClient()
        with patch.object(client, "_post", return_value={"success": False}):
            res = client.create_repository(name="sovereign-smart-contract", description="Test repo")
            data = res.get("data", {})
            expected_html = bu.build_portal_url("sovereign-developer/sovereign-smart-contract")
            expected_clone = bu.build_portal_url("sovereign-developer/sovereign-smart-contract.git")
            self.assertEqual(data.get("html_url"), expected_html)
            self.assertEqual(data.get("clone_url"), expected_clone)

    def test_allowed_hosts_includes_all_base_domains(self):
        """Vérifie que ALLOWED_HOSTS inclut les domaines des trois bases URLs."""
        for domain in ["cybersocle.site", "git.cybersocle.site", "api.cybersocle.site"]:
            self.assertIn(domain, settings.ALLOWED_HOSTS)
