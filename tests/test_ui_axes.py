"""
Tests for Axe 4: Design System, Interface Graphique & UX Moderne (UI/UX).
Validates UI-01 to UI-05:
- UI-01: Web Code Editor (CodeMirror) on dashboard workbench.
- UI-02: Modern Visual Dashboard & Vulnerability Cards, Circular Gauge for Sovereignty.
- UI-03: Interactive ZKP Wizard, BIP-39 mnemonic generator, key strength meter, protected key download.
- UI-04: Global Toast Notification System in base template and CSS.
- UI-05: Panafrican Sovereign Nodes Interactive Map & Telemetry.
"""

from django.test import Client, TestCase
from django.urls import reverse


class Axe4UITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ui04_toast_notification_system_in_base(self):
        """UI-04: Vérifie la présence du conteneur Toast et du système de notification dans base.html."""
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")

        # Conteneur Toast
        self.assertIn('id="toastContainer"', content)
        self.assertIn('class="toast-container"', content)
        # Helper global window.showToast
        self.assertIn("window.showToast", content)
        self.assertIn("toast-item toast-", content)

    def test_ui01_and_ui02_dashboard_code_editor_and_visualizations(self):
        """UI-01 & UI-02: Vérifie la présence de CodeMirror et des composants graphiques (jauge, cartes)."""
        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")

        # UI-01: Code Editor & Workbench
        self.assertIn("codemirror", content.lower())
        self.assertIn('id="codeEditorMount"', content)
        self.assertIn('id="scanCodeInput"', content)
        self.assertIn("workbench_security_audit.py", content)
        self.assertIn("initCodeEditor", content)

        # UI-02: Visual Dashboard, Circular Gauge & Vulnerability Cards
        self.assertIn("sovereignty-gauge-card", content)
        self.assertIn('id="gaugeProgressCircle"', content)
        self.assertIn('id="gaugeScoreText"', content)
        self.assertIn('id="vulnerabilitiesContainer"', content)
        self.assertIn("vulnerability-card", content)
        self.assertIn("pillCriticalCount", content)
        self.assertIn("renderVulnerabilityCards", content)

    def test_ui03_zkp_interactive_wizard_and_identity_manager(self):
        """UI-03: Vérifie l'assistant ZKP interactif (BIP-39, jauge de force, téléchargement de clé)."""
        resp = self.client.get(reverse("zkp_auth:zkp_login_page"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")

        # Wizard Navigation & Steps
        self.assertIn("zkp-wizard-card", content)
        self.assertIn("zkp-steps-nav", content)
        self.assertIn("wizardStep1", content)
        self.assertIn("wizardStep2", content)
        self.assertIn("wizardStep3", content)

        # BIP-39 Mnemonic & Cryptographic Strength
        self.assertIn("BIP-39", content)
        self.assertIn('id="mnemonicWordsGrid"', content)
        self.assertIn("generateNewMnemonic", content)
        self.assertIn('id="strengthBar"', content)
        self.assertIn("updateCryptoStrengthMeter", content)

        # Sovereign Key Download
        self.assertIn("downloadSovereignKeyFile", content)
        self.assertIn(".json", content)

    def test_ui05_panafrican_metrics_map_and_nodes(self):
        """UI-05: Vérifie la cartographie interactive des nœuds souverains africains."""
        resp = self.client.get(reverse("sovereignty_metrics"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode("utf-8")

        # Map Wrapper & SVG
        self.assertIn("africa-map-wrapper", content)
        self.assertIn("map-svg-container", content)

        # 5 Nœuds Souverains Africains
        for node in ["Abidjan", "Dakar", "Lagos", "Kigali", "Nairobi"]:
            self.assertIn(node, content)

        # Cartes et Télémétrie de Latence
        self.assertIn("node-cards-grid", content)
        self.assertIn('id="card-abidjan"', content)
        self.assertIn('id="card-dakar"', content)
        self.assertIn('id="card-lagos"', content)
        self.assertIn('id="card-kigali"', content)
        self.assertIn('id="card-nairobi"', content)
        self.assertIn('id="nodeDetailsBanner"', content)
        self.assertIn("simulatePingAllNodes", content)

    def test_style_css_contains_axe4_classes(self):
        """Vérifie que static/css/style.css contient les classes CSS des composants de l'Axe 4."""
        import os

        from django.conf import settings

        css_path = os.path.join(settings.BASE_DIR, "static", "css", "style.css")
        self.assertTrue(os.path.exists(css_path))
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # UI-04 Toast
        self.assertIn(".toast-container", css_content)
        self.assertIn(".toast-item", css_content)

        # UI-01 & UI-02 Editor & Visualisations
        self.assertIn(".editor-container", css_content)
        self.assertIn(".circular-gauge-wrapper", css_content)
        self.assertIn(".vulnerability-card", css_content)
        self.assertIn(".badge-critical", css_content)

        # UI-03 ZKP Wizard
        self.assertIn(".zkp-wizard-card", css_content)
        self.assertIn(".mnemonic-grid", css_content)
        self.assertIn(".strength-meter-bar", css_content)

        # UI-05 Map
        self.assertIn(".africa-map-wrapper", css_content)
        self.assertIn(".map-node-pulse", css_content)
        self.assertIn(".node-cards-grid", css_content)
