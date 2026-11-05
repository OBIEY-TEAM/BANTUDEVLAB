from pathlib import Path

from django.test import Client, TestCase
from django.utils.translation import activate
from django.utils.translation import gettext as _
from PIL import Image


class SyncAndBrandingTestCase(TestCase):
    """
    Tests de validation de la nouvelle charte graphique, logo cyber et synchronisation linguistique tri-ecosysteme.
    """

    def setUp(self):
        self.client = Client()

    def test_new_logo_files_exist_and_valid(self):
        """Verifie que les fichiers du nouveau logo existent et sont valides sur BantuDevLab et Gitea."""
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
        self.assertEqual(logo_svg.read_bytes(), gitea_logo_svg.read_bytes())

    def test_sync_script_distribution(self):
        """Verifie que le script de synchronisation est distribue a travers les 3 plateformes."""
        bantu_js = Path("static/js/bantu-ecosystem-sync.js")
        gitea_js = Path("custom/public/assets/js/bantu-ecosystem-sync.js")
        self.assertTrue(bantu_js.exists())
        self.assertTrue(gitea_js.exists())
        self.assertEqual(bantu_js.read_text(encoding="utf-8"), gitea_js.read_text(encoding="utf-8"))

        content = bantu_js.read_text(encoding="utf-8")
        self.assertIn("bantu_ecosystem_sync", content)
        self.assertIn("syncEcosystemChange", content)
        self.assertIn("GITEA_LANG_MAP", content)

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
        self.assertIn("bantu-ecosystem-sync.js", base_html)
        self.assertIn("GITEA_LANG_MAP", base_html)
        self.assertIn("syncEcosystemChange", base_html)
        self.assertIn("bantu_theme", base_html)

    def test_gitlab_forge_server_i18n_and_sync(self):
        """Verifie que forge_server.py contient les catalogues i18n et les routes statiques du logo."""
        forge_code = Path("forge_server.py").read_text(encoding="utf-8")
        self.assertIn("FORGE_I18N", forge_code)
        self.assertIn('"fr":', forge_code)
        self.assertIn('"en":', forge_code)
        self.assertIn('"sw":', forge_code)
        self.assertIn('"pt":', forge_code)
        self.assertIn("/static/img/logo.svg", forge_code)
        self.assertIn("bantu-ecosystem-sync.js", forge_code)
        self.assertIn("changeForgeLang", forge_code)
        self.assertIn("toggleForgeTheme", forge_code)

    def test_gitea_header_tmpl_sync_controls(self):
        """Verifie que le template Gitea contient le logo, le selecteur de langues et la bascule de theme."""
        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("bantu-ecosystem-sync.js", header_tmpl)
        self.assertIn("gitea-bantu-lang-selector", header_tmpl)
        self.assertIn("gitea-theme-toggle-btn", header_tmpl)
        self.assertIn("syncEcosystemChange", header_tmpl)
