from django.test import TestCase
from apps.security_scanner.engine import SecurityScannerEngine

class SecurityScannerTestCase(TestCase):
    def test_clean_code_scan(self):
        clean_code = "def add(a, b):\n    return a + b\n"
        report = SecurityScannerEngine.scan_code("math.py", clean_code)
        self.assertEqual(report["total_issues"], 0)
        self.assertEqual(report["sovereignty_score"], 100)
        self.assertEqual(report["status_rating"], "EXCELLENT")

    def test_detect_hardcoded_secrets(self):
        leaked_code = "api_key = 'ghp_123456789012345678901234567890123456'\n"
        report = SecurityScannerEngine.scan_code("config.py", leaked_code)
        self.assertGreater(report["critical"], 0)
        self.assertLess(report["sovereignty_score"], 100)
        self.assertEqual(report["issues"][0]["type"], "SECRET_LEAK")

    def test_detect_sql_injection(self):
        sql_vuln = "cursor.execute('SELECT * FROM users WHERE id = %s' + user_id)\n"
        report = SecurityScannerEngine.scan_code("models.py", sql_vuln)
        self.assertGreater(report["high"], 0)
        self.assertIn("Injection SQL", report["issues"][0]["description"])

    def test_detect_sovereignty_leak(self):
        foreign_telemetry = "telemetry_url = 'https://tracking.analytics.xyz/v1'\n"
        report = SecurityScannerEngine.scan_code("app.py", foreign_telemetry)
        self.assertGreater(report["medium"], 0)
        self.assertEqual(report["issues"][0]["type"], "SOVEREIGNTY_RISK")
