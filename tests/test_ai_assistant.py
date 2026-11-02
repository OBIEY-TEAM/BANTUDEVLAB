from django.test import TestCase

from apps.ai_assistant.gemma import GemmaAssistant
from apps.ai_assistant.tasks import async_analyze_code
from apps.ai_assistant.views import MAX_CODE_CHARS, sanitize_pii_and_secrets, validate_input


class GemmaAssistantTestCase(TestCase):
    def test_gemma_fallback_analysis_clean_code(self):
        assistant = GemmaAssistant()
        self.assertEqual(assistant.model_name, "gemma2:2b")
        code = "def sovereign_hash(data):\n    return hashlib.sha256(data).hexdigest()\n"
        result = assistant.analyze_code(code_snippet=code, context="unit_test")
        self.assertTrue(result["success"])
        self.assertIn("response", result)
        self.assertIn("BantuDevLab AI", result["response"])
        self.assertIn("Gemma 2 2B", result["response"])

    def test_gemma_fallback_analysis_eval_danger(self):
        assistant = GemmaAssistant()
        dangerous_code = "eval(user_untrusted_input)\n"
        result = assistant.analyze_code(code_snippet=dangerous_code, context="security_review")
        self.assertTrue(result["success"])
        self.assertIn("eval", result["response"])
        self.assertIn("[CRITIQUE]", result["response"])

    def test_gemma2_prompt_instruct_format(self):
        """T-AI-501 : Format officiel Gemma 2 (<start_of_turn>user / model)."""
        assistant = GemmaAssistant()
        prompt = assistant._build_prompt("print('hello')", "test_context")
        self.assertTrue(prompt.startswith("<start_of_turn>user\n"))
        self.assertIn("<end_of_turn>\n<start_of_turn>model\n", prompt)
        self.assertIn("BANTU-AI", prompt)
        self.assertIn("print('hello')", prompt)

    def test_pii_and_secret_sanitization(self):
        """T-DEV-505 : Anonymisation des IP, emails et masquage des secrets."""
        raw_code = (
            "ip = '192.168.1.100'\n"
            "email = 'contact@african-sovereignty.org'\n"
            "api_key = 'ghp_123456789012345678901234567890123456'\n"
        )
        cleaned = sanitize_pii_and_secrets(raw_code)
        self.assertNotIn("192.168.1.100", cleaned)
        self.assertIn("[IP_ANONYMISEE]", cleaned)
        self.assertNotIn("contact@african-sovereignty.org", cleaned)
        self.assertIn("[EMAIL_ANONYMISE]", cleaned)
        self.assertNotIn("ghp_123456789012345678901234567890123456", cleaned)
        self.assertIn("[SECRET MASQUE]", cleaned)

    def test_payload_size_validation(self):
        """T-DEV-505 : Rejet du code dépassant 15 000 caractères."""
        oversized = "a" * (MAX_CODE_CHARS + 10)
        err = validate_input(oversized, "review")
        self.assertIsNotNone(err)
        self.assertIn("trop volumineux", err)

        valid_code = "def valid(): return True"
        self.assertIsNone(validate_input(valid_code, "review"))

    def test_async_analyze_code_celery_task(self):
        """T-DEV-501 : Exécution de la tâche Celery async_analyze_code."""
        result = async_analyze_code("print('sovereign')", context="celery_test")
        self.assertTrue(result["success"])
        self.assertIn("log_id", result)
        self.assertEqual(result["model"], "gemma2:2b (Sovereign Engine)")

    def test_gemma_streaming_early_abort_safety(self):
        """T-AI-503 : Gestion de l'interruption prématurée du flux SSE."""
        assistant = GemmaAssistant()
        generator = assistant.stream_analyze_code("print('stream')")
        first_token = next(generator)
        self.assertTrue(len(first_token) > 0)
        generator.close()  # Interruption anticipée par le client

    def test_copilot_explain_endpoint(self):
        """T-COP-701 : Test du point d'accès Copilot Explain."""
        from django.test import Client

        client = Client()
        res = client.post(
            "/api/ai/copilot/explain/",
            data={"code": "def hello():\n    return 'world'\n", "language": "python"},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIn("explanation", data)

    def test_copilot_complete_endpoint(self):
        """T-COP-701 : Test du point d'accès Copilot Complete."""
        from django.test import Client

        client = Client()
        res = client.post(
            "/api/ai/copilot/complete/",
            data={"code": "def calculate_hash(data):", "language": "python"},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIn("completion", data)

    def test_copilot_pr_summary_endpoint(self):
        """T-COP-701 : Test du point d'accès Copilot PR Summary."""
        from django.test import Client

        client = Client()
        res = client.post(
            "/api/ai/copilot/pr-summary/",
            data={"diff": "+ def new_feature(): pass", "title": "Add feature"},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIn("summary", data)

    def test_copilot_validation_errors(self):
        """T-COP-701 : Test de rejet si paramètres invalides."""
        from django.test import Client

        client = Client()
        res = client.post("/api/ai/copilot/explain/", data={}, content_type="application/json")
        self.assertEqual(res.status_code, 400)
        res2 = client.post("/api/ai/copilot/complete/", data={}, content_type="application/json")
        self.assertEqual(res2.status_code, 400)
        res3 = client.post("/api/ai/copilot/pr-summary/", data={}, content_type="application/json")
        self.assertEqual(res3.status_code, 400)

    def test_copilot_pr_review_bot_direct(self):
        """T-PR-801 : Test du bot de revue PR via appel direct."""
        from django.test import Client

        client = Client()
        res = client.post(
            "/api/ai/copilot/pr-review-bot/",
            data={
                "repo_name": "bantudevlab/forge",
                "pr_index": 42,
                "diff": "+ def test(): return True",
                "title": "Clean PR",
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["verdict"], "APPROVED")
        self.assertIn("review_comment", data)

    def test_copilot_pr_review_bot_webhook(self):
        """T-PR-801 : Test du bot de revue PR via charge webhook Gitea/GitHub."""
        from django.test import Client

        client = Client()
        webhook_payload = {
            "action": "opened",
            "pull_request": {
                "number": 7,
                "title": "Danger eval feature",
                "body": "+ eval(request.GET['cmd'])",
            },
            "repository": {"full_name": "bantudevlab/core"},
        }
        res = client.post(
            "/api/ai/copilot/pr-review-bot/",
            data=webhook_payload,
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["verdict"], "REQUEST_CHANGES")
