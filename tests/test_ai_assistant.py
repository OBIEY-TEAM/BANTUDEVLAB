from django.test import TestCase

from apps.ai_assistant.gemma import GemmaAssistant


class GemmaAssistantTestCase(TestCase):
    def test_gemma_fallback_analysis_clean_code(self):
        assistant = GemmaAssistant()
        code = "def sovereign_hash(data):\n    return hashlib.sha256(data).hexdigest()\n"
        result = assistant.analyze_code(code_snippet=code, context="unit_test")
        self.assertTrue(result["success"])
        self.assertIn("response", result)
        self.assertIn("BantuDevLab AI", result["response"])

    def test_gemma_fallback_analysis_eval_danger(self):
        assistant = GemmaAssistant()
        dangerous_code = "eval(user_untrusted_input)\n"
        result = assistant.analyze_code(code_snippet=dangerous_code, context="security_review")
        self.assertTrue(result["success"])
        self.assertIn("eval", result["response"])
