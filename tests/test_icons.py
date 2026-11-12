"""Tests des icones SVG et de l'absence d'emojis (T-080 a T-085)."""

import importlib.util
from pathlib import Path

from django.template import Context, Template
from django.test import TestCase
from rest_framework.test import APIClient

ROOT = Path(__file__).resolve().parent.parent


def _load_checker():
    spec = importlib.util.spec_from_file_location("check_no_emoji", ROOT / "scripts" / "check_no_emoji.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IconTagTests(TestCase):
    def render(self, source):
        return Template(source).render(Context())

    def test_icon_renders_decorative_svg(self):
        html = self.render('{% icon "shield" size=24 %}')
        self.assertIn("<svg", html)
        self.assertIn('width="24"', html)
        self.assertIn('aria-hidden="true"', html)
        self.assertIn("currentColor", html)

    def test_icon_with_title_is_accessible(self):
        html = self.render('{% icon "star" title="Favoris" %}')
        self.assertIn('role="img"', html)
        self.assertIn('aria-label="Favoris"', html)

    def test_title_is_escaped(self):
        html = self.render('{% icon "star" title="<script>x</script>" %}')
        self.assertNotIn("<script>", html)

    def test_unknown_icon_renders_nothing(self):
        self.assertEqual(self.render('{% icon "inexistante" %}'), "")

    def test_all_flags_render(self):
        for code in ("CIV", "SEN", "NGA", "KEN", "RWA"):
            with self.subTest(code=code):
                self.assertIn("<svg", self.render('{% flag "' + code + '" %}'))
        self.assertEqual(self.render('{% flag "XXX" %}'), "")


class NoEmojiTests(TestCase):
    def test_checker_flags_emojis(self):
        checker = _load_checker()
        sample = ROOT / "tests" / "_emoji_sample.tmp.md"
        sample.write_text("Bonjour \U0001f680", encoding="utf-8")
        try:
            found = checker.find_emojis([sample])
        finally:
            sample.unlink()
        self.assertEqual(len(found), 1)

    def test_project_has_no_emoji(self):
        checker = _load_checker()
        self.assertEqual(checker.find_emojis(checker.iter_files()), [])

    def test_rendered_pages_contain_svg_icons_and_no_emoji(self):
        checker = _load_checker()
        client = APIClient()
        for url in ("/", "/metrics/", "/api/zkp/login-ui/"):
            with self.subTest(url=url):
                resp = client.get(url)
                self.assertEqual(resp.status_code, 200)
                content = resp.content.decode("utf-8")
                self.assertIn("<svg", content)
                self.assertIsNone(checker.EMOJI.search(content))
