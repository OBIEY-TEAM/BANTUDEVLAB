"""
QA-01: Tests End-to-End Complets avec Playwright pour BANTUDEVLAB.
Rédige une suite complète de tests de bout en bout simulant le parcours utilisateur réel :
1. Accès à la page d'authentification souveraine (/api/zkp/login-ui/).
2. Génération de clé ZKP dans le navigateur (BIP-39, dérivation Schnorr locale).
3. Téléchargement ou enregistrement de l'identité Zero-Trust sans mot de passe.
4. Authentification Zero-Trust (défi challenge Fiat-Shamir résolu localement).
5. Soumission de code dans le Workbench (/dashboard/).
6. Exécution du scanner SAST et vérification du score de souveraineté dans l'interface.
"""

import os
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright


class PlaywrightE2ETestCase(StaticLiveServerTestCase):
    """Suite de tests E2E Playwright pour le parcours utilisateur complet."""

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        try:
            cls.playwright = sync_playwright().start()
            cls.browser = cls.playwright.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )
        except Exception as e:
            super().tearDownClass()
            raise unittest.SkipTest(f"Playwright chromium browser indisponible: {e}")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "browser") and cls.browser:
            cls.browser.close()
        if hasattr(cls, "playwright") and cls.playwright:
            cls.playwright.stop()
        super().tearDownClass()

    def setUp(self):
        from django.core.cache import cache

        cache.clear()
        self.context = self.browser.new_context(viewport={"width": 1280, "height": 800})
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_complete_e2e_user_journey(self):
        """
        Simule le parcours utilisateur complet :
        Génération mnémonique ZKP -> Inscription -> Authentification ZKP -> Workbench -> Scan Souveraineté
        """
        # 1. Accès à la page de connexion ZKP
        login_url = f"{self.live_server_url}/api/zkp/login-ui/"
        self.page.goto(login_url)
        self.page.wait_for_selector(".zkp-wizard-card")
        self.assertIn("Connexion Zero-Trust", self.page.locator("h2").inner_text())

        # 2. Étape 1 : Renseignement du nom d'utilisateur
        username_input = self.page.locator("#zkpUsername")
        username_input.fill("amadou_dev")
        self.page.locator("button:has-text('Suivant')").click()

        # 3. Étape 2 : Génération de clé mnémonique BIP-39
        self.page.wait_for_selector("#mnemonicWordsGrid")
        # Vérifie qu'exactement 12 puces de mots mnémoniques sont affichées
        mnemonic_chips = self.page.locator(".mnemonic-word-chip")
        self.assertEqual(mnemonic_chips.count(), 12)

        # Vérifie que le secret dérivé et la jauge de force sont remplis
        secret_val = self.page.locator("#zkpSecret").input_value()
        self.assertTrue(len(secret_val) > 10)
        self.assertIn("Inviolable", self.page.locator("#strengthText").inner_text())

        # Enregistrement de l'identité sur le serveur
        self.page.locator("button:has-text('Enregistrer Identité')").click()
        # Attendre le message de succès dans les logs
        self.page.wait_for_selector("#zkpLog")
        self.page.wait_for_function(
            "() => document.getElementById('zkpLog').innerText.includes('Enregistrement ZKP réussi')"
        )

        # 4. Étape 3 : Authentification Zero-Trust (Résolution Fiat-Shamir)
        self.page.locator("button:has-text('Passer à la Connexion')").click()
        self.page.wait_for_selector("#wizardStep3")
        self.page.locator("button:has-text('Prouver mon Identité')").click()

        # Attendre le message de confirmation de connexion ZKP
        self.page.wait_for_function(
            "() => document.getElementById('zkpLog').innerText.includes('Vérification Zero-Knowledge réussie')"
        )

        # 5. Navigation vers le Workbench Souverain sur le Dashboard
        dashboard_url = f"{self.live_server_url}/dashboard/"
        self.page.goto(dashboard_url)
        self.page.wait_for_selector(".editor-container")
        self.assertIn("Workbench Souverain & Audit SAST", self.page.locator("body").inner_text())

        # 6. Soumission de code dans le Workbench
        test_source_code = """
import os
import requests

api_key = "ghp_123456789012345678901234567890123456"

def sovereign_function(query):
    eval(query)
    requests.post("https://foreign-analytics.tracking.com/data")
    return True
"""
        # Injection dans l'éditeur (CodeMirror ou fallback textarea)
        self.page.evaluate(
            """(code) => {
            if (window.editorInstance) {
                window.editorInstance.setValue(code);
            } else {
                document.getElementById('scanCodeInput').value = code;
            }
        }""",
            test_source_code,
        )

        # Lancer le scan SAST
        self.page.locator("button:has-text('Lancer l\\'Audit de Sécurité')").click()

        # 7. Vérification de la jauge et des résultats de souveraineté
        self.page.wait_for_selector("#visualScanContainer", state="visible")
        self.page.wait_for_selector(".sovereignty-gauge-card")

        # Vérifier que le score est affiché et calculé
        score_text = self.page.locator("#gaugeScoreText").inner_text()
        self.assertTrue(score_text.endswith("%"))

        # Vérifier la présence des compteurs de sévérité
        pill_crit = self.page.locator("#pillCriticalCount").inner_text()
        self.assertTrue(int(pill_crit) >= 0)

        # Vérifier la présence d'au moins une carte de vulnérabilité
        vuln_cards = self.page.locator(".vulnerability-card")
        self.assertTrue(vuln_cards.count() >= 1)

    def test_zero_cdn_offline_isolation(self):
        """
        T-QA-503 : Vérifie que le tableau de bord et CodeMirror se chargent parfaitement
        sans aucune requête réseau sortant vers l'extérieur du serveur local.
        """
        external_requests = []

        def handle_request(request):
            url = request.url
            if not url.startswith(self.live_server_url) and not url.startswith("data:"):
                external_requests.append(url)

        self.page.on("request", handle_request)
        self.page.goto(f"{self.live_server_url}/dashboard/")
        self.page.wait_for_selector(".editor-container")
        self.page.wait_for_function("() => window.CodeMirror !== undefined")

        # Vérification qu'aucune requête externe / CDN n'a été émise
        self.assertEqual(len(external_requests), 0, f"Requêtes CDN détectées : {external_requests}")
