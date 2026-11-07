"""
Tests pour la centralisation des URLs souveraines (BASE_URL_1, BASE_URL_2, BASE_URL_3)
et des services associés (Gitea, Forge interne, IA Gemma).
"""

from django.test import RequestFactory, TestCase

from apps.core.context_processors import forge_context
from config.base_urls import (
    AI_URL,
    BASE_URL_1,
    BASE_URL_2,
    BASE_URL_3,
    FORGE_INTERNAL_URL,
    GITEA_WEB_URL,
    build_ai_url,
    build_api_url,
    build_forge_url,
    build_git_url,
    build_gitea_url,
    build_portal_url,
    get_base_domains,
    get_base_urls,
)


class BaseURLsTestCase(TestCase):
    def test_default_base_urls(self):
        """Vérifie que les URLs souveraines par défaut correspondent aux spécifications."""
        self.assertEqual(BASE_URL_1, "https://cybersocle.site")
        self.assertEqual(BASE_URL_2, "https://git.cybersocle.site")
        self.assertEqual(BASE_URL_3, "https://api.cybersocle.site")
        self.assertEqual(GITEA_WEB_URL, "https://gitea.cybersocle.site")
        self.assertEqual(FORGE_INTERNAL_URL, "https://forge.cybersocle.site")
        self.assertEqual(AI_URL, "https://ai.cybersocle.site")

    def test_url_builders(self):
        """Vérifie les fonctions de construction dynamique d'URLs."""
        self.assertEqual(build_portal_url(), "https://cybersocle.site")
        self.assertEqual(build_portal_url("/dashboard/"), "https://cybersocle.site/dashboard/")
        self.assertEqual(build_portal_url("metrics/"), "https://cybersocle.site/metrics/")

        self.assertEqual(build_git_url("/user/login"), "https://git.cybersocle.site/user/login")
        self.assertEqual(build_api_url("/v1/health"), "https://api.cybersocle.site/v1/health")
        self.assertEqual(build_gitea_url("/user/login"), "https://gitea.cybersocle.site/user/login")
        self.assertEqual(build_forge_url("/health"), "https://forge.cybersocle.site/health")
        self.assertEqual(build_ai_url("/api/generate"), "https://ai.cybersocle.site/api/generate")

    def test_get_base_domains(self):
        """Vérifie l'extraction des noms d'hôtes sans ports ni protocoles."""
        domains = get_base_domains()
        self.assertIn("cybersocle.site", domains)
        self.assertIn("git.cybersocle.site", domains)
        self.assertIn("api.cybersocle.site", domains)
        self.assertIn("gitea.cybersocle.site", domains)
        self.assertIn("forge.cybersocle.site", domains)
        self.assertIn("ai.cybersocle.site", domains)

    def test_get_base_urls_dict(self):
        urls = get_base_urls()
        self.assertEqual(urls["BASE_URL_1"], "https://cybersocle.site")
        self.assertEqual(urls["BASE_URL_2"], "https://git.cybersocle.site")
        self.assertEqual(urls["BASE_URL_3"], "https://api.cybersocle.site")
        self.assertEqual(urls["GITEA_WEB_URL"], "https://gitea.cybersocle.site")
        self.assertEqual(urls["FORGE_INTERNAL_URL"], "https://forge.cybersocle.site")
        self.assertEqual(urls["AI_URL"], "https://ai.cybersocle.site")

    def test_context_processor(self):
        """Vérifie que forge_context fournit les variables d'URL aux templates."""
        rf = RequestFactory()
        req = rf.get("/")
        ctx = forge_context(req)
        self.assertIn("BASE_URL_1", ctx)
        self.assertIn("BASE_URL_2", ctx)
        self.assertIn("BASE_URL_3", ctx)
        self.assertIn("GITEA_WEB_URL", ctx)
        self.assertIn("FORGE_INTERNAL_URL", ctx)
        self.assertIn("AI_URL", ctx)
        self.assertIn("GITEA_LOGIN_URL", ctx)
        self.assertIn("GITLAB_URL", ctx)
        self.assertNotIn("localhost:3002", ctx["GITEA_LOGIN_URL"])
