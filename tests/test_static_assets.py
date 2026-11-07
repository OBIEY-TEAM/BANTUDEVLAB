"""Tests automatisés pour la vérification du chargement des fichiers statiques et CSS."""

import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from rest_framework.test import APIClient


class StaticFilesLoadingTestCase(SimpleTestCase):
    """Vérifie que les fichiers statiques cruciaux (CSS, JS, images, polices) sont servis correctement."""

    def setUp(self):
        self.client = APIClient()
        self.base_dir = Path(__file__).resolve().parent.parent

    def test_css_loading_debug_false(self):
        """Vérifie que /static/css/style.css retourne HTTP 200 et text/css même avec DEBUG=False."""
        with override_settings(DEBUG=False):
            resp = self.client.get("/static/css/style.css")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("text/css", resp.headers.get("Content-Type", ""))
            self.assertTrue(len(resp.getvalue()) > 0)

    def test_javascript_loading(self):
        """Vérifie que /static/js/bantu-ecosystem-sync.js retourne HTTP 200 et application/javascript ou text/javascript."""
        with override_settings(DEBUG=False):
            resp = self.client.get("/static/js/bantu-ecosystem-sync.js")
            self.assertEqual(resp.status_code, 200)
            content_type = resp.headers.get("Content-Type", "")
            self.assertTrue(
                "javascript" in content_type,
                f"Content-Type inattendu pour le fichier JS : {content_type}",
            )

    def test_codemirror_vendor_assets_loading(self):
        """Vérifie que les bibliothèques tierces (CodeMirror CSS et JS) sont accessibles via /static/."""
        vendor_assets = [
            "/static/vendor/codemirror/codemirror.min.css",
            "/static/vendor/codemirror/theme/material-darker.min.css",
            "/static/vendor/codemirror/codemirror.min.js",
            "/static/vendor/codemirror/mode/python/python.min.js",
            "/static/vendor/codemirror/addon/edit/closebrackets.min.js",
        ]
        with override_settings(DEBUG=False):
            for asset_url in vendor_assets:
                resp = self.client.get(asset_url)
                self.assertEqual(
                    resp.status_code,
                    200,
                    f"Impossible de charger l'asset statique : {asset_url} (HTTP {resp.status_code})",
                )

    def test_images_and_favicons_loading(self):
        """Vérifie que le logo et les favicons sont accessibles et retournent HTTP 200."""
        assets = [
            "/static/img/logo.svg",
            "/static/img/favicon.svg",
            "/static/img/logo.png",
            "/static/img/favicon.png",
            "/static/img/favicon.ico",
        ]
        with override_settings(DEBUG=False):
            for asset_url in assets:
                resp = self.client.get(asset_url)
                self.assertEqual(
                    resp.status_code,
                    200,
                    f"Asset image manquant ou inaccessible : {asset_url}",
                )

    def test_templates_static_references_exist_on_disk(self):
        """Scanne tous les gabarits HTML pour s'assurer que chaque {% static 'path' %} existe sur disque."""
        templates_dir = self.base_dir / "templates"
        static_dir = self.base_dir / "static"
        static_tag_regex = re.compile(r"""\{%\s*static\s+['"]([^'"]+)['"]\s*%\}""")

        for html_file in templates_dir.rglob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            matches = static_tag_regex.findall(content)
            for asset_rel_path in matches:
                target_path = static_dir / asset_rel_path
                self.assertTrue(
                    target_path.exists(),
                    f"Référence statique cassée dans {html_file.name}: {asset_rel_path} n'existe pas dans {static_dir}",
                )

    def test_static_exempt_from_ssl_redirect(self):
        """Vérifie que la configuration SECURE_REDIRECT_EXEMPT inclut bien les routes statiques."""
        exempts = getattr(settings, "SECURE_REDIRECT_EXEMPT", [])
        has_static_exempt = any(re.match(pattern, "static/css/style.css") for pattern in exempts)
        self.assertTrue(
            has_static_exempt,
            "Les fichiers statiques doivent être exemptés de SECURE_SSL_REDIRECT pour éviter les boucles ou blocages HTTP.",
        )
