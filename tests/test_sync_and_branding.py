from django.test import TestCase, Client
from django.utils.translation import activate, gettext as _
from pathlib import Path
from PIL import Image

class SyncAndBrandingTestCase(TestCase):
    """
    Tests de validation de la nouvelle charte graphique, logo cyber et synchronisation linguistique.
    """

    def setUp(self):
        self.client = Client()

    def test_new_logo_files_exist_and_valid(self):
        """Verifie que les fichiers du nouveau logo existent et sont valides."""
        logo_png = Path("static/img/logo.png")
        self.assertTrue(logo_png.exists())
        with Image.open(logo_png) as img:
            self.assertEqual(img.size, (512, 512))

        logo_svg = Path("static/img/logo.svg")
        self.assertTrue(logo_svg.exists())
        content = logo_svg.read_text(encoding="utf-8")
        self.assertIn("<svg", content)
        self.assertIn("data:image/png;base64,", content)

        gitea_logo_svg = Path("custom/public/assets/img/logo.svg")
        self.assertTrue(gitea_logo_svg.exists())

    def test_language_catalogs_activation(self):
        """Verifie que les catalogues de langues souveraines se chargent sans erreur."""
        expected = {
            "fr": "Tableau de Bord Souverain BANTUDEVLAB",
            "en": "BANTUDEVLAB Sovereign Dashboard",
            "sw": "Dashibodi Huru ya BANTUDEVLAB",
            "pt": "Painel de Controle Soberano BANTUDEVLAB",
        }
        for lang_code, exp_title in expected.items():
            activate(lang_code)
            translated = _("Tableau de Bord Souverain BANTUDEVLAB")
            self.assertEqual(translated, exp_title)

    def test_home_page_rendering_in_multiple_languages(self):
        """Verifie que la page d'accueil repond en 200 et reflete la langue active."""
        for lang_code in ["fr", "en", "sw", "pt"]:
            response = self.client.get("/", HTTP_ACCEPT_LANGUAGE=lang_code, HTTP_HOST="127.0.0.1")
            self.assertEqual(response.status_code, 200)

    def test_theme_and_lang_cookies_in_base_template(self):
        """Verifie la presence des mecanismes de synchronisation dans le template de base."""
        base_html = Path("templates/base.html").read_text(encoding="utf-8")
        self.assertIn("GITEA_LANG_MAP", base_html)
        self.assertIn("syncGiteaLinks", base_html)
        self.assertIn("bantu_theme", base_html)
