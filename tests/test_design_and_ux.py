"""Tests automatisés du Design System, Navigation, UX et Internationalisation (develop-design.md)."""

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.zkp_auth.models import SovereignIdentity


class DesignAndNavigationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # DES-01 & DES-02: Thème Clair / Sombre
    def test_des01_and_des02_theme_toggle_and_anti_fouc(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")

        # Anti-FOUC script
        self.assertIn("bantu_theme", content)
        self.assertIn("data-theme", content)

        # Theme toggle button
        self.assertIn('id="themeToggleBtn"', content)
        self.assertIn('id="themeIcon"', content)

        # CSS support
        with open("static/css/style.css", "r", encoding="utf-8") as f:
            css = f.read()
        self.assertIn('[data-theme="light"]', css)
        self.assertIn(".theme-switch-btn", css)

    # NAV-01 & NAV-02: Navigation Responsive & Liens Actifs
    def test_nav01_and_nav02_responsive_navbar_and_drawer(self):
        resp = self.client.get(reverse("home"))
        content = resp.content.decode("utf-8")

        # Hamburger toggle button
        self.assertIn('id="mobileMenuBtn"', content)
        self.assertIn('class="navbar-toggle"', content)

        # Drawer panel & overlay
        self.assertIn('id="navDrawer"', content)
        self.assertIn('id="drawerOverlay"', content)
        self.assertIn('class="nav-drawer"', content)

        # Active page detection
        self.assertIn('aria-current="page"', content)

    # NAV-03: Session Utilisateur et Badge ZKP
    def test_nav03_user_profile_session_display(self):
        # Anonymous state
        anon_resp = self.client.get(reverse("home"))
        self.assertIn("Connexion Zero-Trust", anon_resp.content.decode("utf-8"))

        # Authenticated state
        user = User.objects.create_user(username="kouame_sovereign")
        SovereignIdentity.objects.create(user=user, public_key_y="12345", country_code="CIV", is_verified=True)
        self.client.force_login(user)

        auth_resp = self.client.get(reverse("home"))
        auth_content = auth_resp.content.decode("utf-8")
        self.assertIn("user-session-badge", auth_content)
        self.assertIn("kouame_sovereign", auth_content)

    # NAV-04: Fil d'Ariane (Breadcrumbs)
    def test_nav04_breadcrumbs_on_subpages(self):
        for route_name, page_label in [
            ("dashboard", "Tableau de Bord"),
            ("sovereignty_metrics", "Souverainet"),
            ("zkp_auth:zkp_login_page", "Zero-Trust"),
        ]:
            with self.subTest(route=route_name):
                resp = self.client.get(reverse(route_name))
                self.assertEqual(resp.status_code, 200)
                content = resp.content.decode("utf-8")
                self.assertIn('class="breadcrumbs"', content)
                self.assertIn('class="breadcrumbs-current"', content)
                self.assertIn(page_label, content)

    # NAV-05: Indicateur de Lien Externe Forge Git
    def test_nav05_external_forge_git_link(self):
        resp = self.client.get(reverse("home"))
        content = resp.content.decode("utf-8")
        self.assertIn('target="_blank"', content)
        self.assertIn('rel="noopener noreferrer"', content)
        self.assertIn("external-link", content)

    # I18N-01 & I18N-02: Internationalisation & Sélecteur de Langue
    def test_i18n01_and_i18n02_language_selector_and_middleware(self):
        # Middleware checks
        self.assertIn("django.middleware.locale.LocaleMiddleware", settings.MIDDLEWARE)
        self.assertTrue(hasattr(settings, "LANGUAGES"))
        self.assertGreaterEqual(len(settings.LANGUAGES), 4)

        # UI Selector
        resp = self.client.get(reverse("home"))
        content = resp.content.decode("utf-8")
        self.assertIn('id="langMenuBtn"', content)
        self.assertIn('id="langMenu"', content)
        self.assertIn('action="/i18n/setlang/"', content)

    # UI-01: Bouton de Copie Mnémonique (Feedback "Copié !")
    def test_ui01_copy_mnemonic_button(self):
        resp = self.client.get(reverse("zkp_auth:zkp_login_page"))
        content = resp.content.decode("utf-8")
        self.assertIn('id="copyMnemonicBtn"', content)
        self.assertIn("copyMnemonicPhrase", content)

    # UI-02: Sélecteur de Langage Code Workbench
    def test_ui02_code_editor_language_selector(self):
        resp = self.client.get(reverse("dashboard"))
        content = resp.content.decode("utf-8")
        self.assertIn('id="editorLangSelect"', content)
        self.assertIn('value="python"', content)
        self.assertIn('value="javascript"', content)
        self.assertIn('value="yaml"', content)
        self.assertIn('value="dockerfile"', content)

    # UI-03: Accessibilité Clavier Carte SVG des Nœuds
    def test_ui03_svg_map_keyboard_accessibility(self):
        resp = self.client.get(reverse("sovereignty_metrics"))
        content = resp.content.decode("utf-8")
        self.assertIn('tabindex="0"', content)
        self.assertIn('role="button"', content)
        self.assertIn("onkeydown=", content)

    def test_t_rea_1301_and_1302_reactions_and_shortcodes(self):
        """T-REA-1301 & T-REA-1302 : Verification des reactions Primer et polyfill de shortcodes."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-reaction-btn", css_light)
        self.assertIn(".gh-reaction-tag", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-reaction-btn", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-REA-1302", header_tmpl)
        self.assertIn("shortcodeMap", header_tmpl)
        self.assertIn(":rocket:", header_tmpl)
