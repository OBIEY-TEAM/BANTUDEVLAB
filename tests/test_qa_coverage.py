"""
QA-03: Tests Additionnels de Couverture Exhaustive (> 95%) pour BANTUDEVLAB.
Cible les branches de code manquantes dans apps/zkp_auth, apps/security_scanner, apps/ai_assistant.
"""

from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import Client, TestCase
from django.utils import timezone

from apps.ai_assistant.gemma import GemmaAssistant
from apps.ai_assistant.models import AIInteractionLog
from apps.security_scanner.models import SecurityAuditReport
from apps.zkp_auth.crypto import P, ZKPCrypto
from apps.zkp_auth.models import GitAccessToken, SovereignIdentity
from apps.zkp_auth.tokens import GitTokenService


class QACoverageExhaustiveTestCase(TestCase):
    """Couverture exhaustive pour atteindre > 95% sur les 3 modules cibles."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(username="coverage_user", email="cov@bantudevlab.africa")
        self.x, self.y = ZKPCrypto.generate_keypair("seed_coverage_test")
        self.identity = SovereignIdentity.objects.create(
            user=self.user, public_key_y=hex(self.y), country_code="CIV", is_verified=True
        )

    # -------------------------------------------------------------
    # 1. apps/ai_assistant (models, gemma live inference, views errors)
    # -------------------------------------------------------------
    def test_ai_assistant_models_and_gemma_live_inference(self):
        # AIInteractionLog __str__
        log_entry = AIInteractionLog.objects.create(
            query_context="code_review",
            prompt_snippet="test prompt",
            ai_response="test response",
            model_used="gemma2:2b",
        )
        self.assertIn("code_review", str(log_entry))

        # Gemma live inference (status 200)
        assistant = GemmaAssistant()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"response": "Analyse réussie par Gemma 5B"}
        with patch("requests.post", return_value=mock_resp):
            res = assistant.analyze_code("print('hello')", context="review")
            self.assertTrue(res["success"])
            self.assertEqual(res["mode"], "live_inference")
            self.assertEqual(res["response"], "Analyse réussie par Gemma 5B")

        # Gemma live streaming (status 200)
        mock_stream_resp = MagicMock()
        mock_stream_resp.status_code = 200
        mock_stream_resp.iter_lines.return_value = [
            b'{"response": "Mot1", "done": false}',
            b'{"response": " Mot2", "done": true}',
        ]
        with patch("requests.post", return_value=mock_stream_resp):
            stream_tokens = list(assistant.stream_analyze_code("print('hello')"))
            self.assertIn("Mot1", stream_tokens)
            self.assertIn(" Mot2", stream_tokens)

    def test_ai_assistant_views_edge_cases(self):
        # Missing code in review view
        res = self.client.post("/api/ai/review/", {}, content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("code snippet requis", res.json()["error"])

        # Non-streaming review view with fallback rules (SQL injection + secrets)
        code_with_rules = "cursor.execute('SELECT * FROM ' + table)\napi_token = 'my_secret_token'"
        res_sync = self.client.post(
            "/api/ai/review/", {"code": code_with_rules, "stream": False}, content_type="application/json"
        )
        self.assertEqual(res_sync.status_code, 200)
        self.assertTrue(res_sync.json()["success"])
        self.assertIn("Vulnérabilité SQL", res_sync.json()["response"])

        # Test streaming exception handling
        with patch.object(GemmaAssistant, "stream_analyze_code", side_effect=RuntimeError("Streaming error")):
            res_stream_err = self.client.post(
                "/api/ai/review/", {"code": "print('hello')", "stream": True}, content_type="application/json"
            )
            self.assertEqual(res_stream_err.status_code, 200)
            content = b"".join(res_stream_err.streaming_content).decode("utf-8")
            self.assertNotIn("Streaming error", content)  # SEC-043: pas de fuite de detail interne
            self.assertIn("Erreur interne", content)

        # GET method without code param
        res_get_err = self.client.get("/api/ai/review/")
        self.assertEqual(res_get_err.status_code, 400)

        # Gemma status view
        res_status = self.client.get("/api/ai/status/")
        self.assertEqual(res_status.status_code, 200)

    # -------------------------------------------------------------
    # 2. apps/security_scanner (models, views history & sarif, engine)
    # -------------------------------------------------------------
    def test_security_scanner_models_and_views(self):
        report = SecurityAuditReport.objects.create(
            repository_name="cov-repo",
            file_scanned="vuln.py",
            sovereignty_score=35,
            status_rating="CRITICAL_RISK",
            raw_findings=[
                {
                    "type": "SECRET_LEAK",
                    "description": "High entropy token",
                    "severity": "CRITICAL",
                    "file": "vuln.py",
                    "line": 2,
                },
                {
                    "type": "CODE_VULN",
                    "description": "Command execution",
                    "severity": "HIGH",
                    "file": "vuln.py",
                    "line": 5,
                },
            ],
        )
        self.assertIn("cov-repo", str(report))

        # Missing content in ScanCodeView
        res = self.client.post("/api/security/scan/", {}, content_type="application/json")
        self.assertEqual(res.status_code, 400)

        # SecurityAuditHistoryView
        res_history = self.client.get("/api/security/audits/")
        self.assertEqual(res_history.status_code, 200)
        self.assertTrue(len(res_history.json()["audits"]) >= 1)

        # SARIF Export View (by ID and not found)
        res_sarif = self.client.get(f"/api/security/audits/{report.id}/sarif/")
        self.assertEqual(res_sarif.status_code, 200)
        self.assertEqual(res_sarif.json()["version"], "2.1.0")

        # GitLab SAST Export View (T-GIT-304)
        res_gl_sast = self.client.get(f"/api/security/audits/{report.id}/gitlab-sast/")
        self.assertEqual(res_gl_sast.status_code, 200)
        self.assertEqual(res_gl_sast.json()["version"], "15.0.0")

        res_gl_sast_latest = self.client.get("/api/security/gitlab-sast/")
        self.assertEqual(res_gl_sast_latest.status_code, 200)

        res_sarif_404 = self.client.get("/api/security/audits/999999/sarif/")
        self.assertEqual(res_sarif_404.status_code, 404)
        res_gl_sast_404 = self.client.get("/api/security/audits/999999/gitlab-sast/")
        self.assertEqual(res_gl_sast_404.status_code, 404)

        # SARIF Export View when no reports exist
        SecurityAuditReport.objects.all().delete()
        res_sarif_empty = self.client.get("/api/security/sarif/")
        self.assertEqual(res_sarif_empty.status_code, 404)
        res_gl_sast_empty = self.client.get("/api/security/gitlab-sast/")
        self.assertEqual(res_gl_sast_empty.status_code, 404)

    # -------------------------------------------------------------
    # 3. apps/zkp_auth (crypto, models, tokens, views)
    # -------------------------------------------------------------
    def test_zkp_auth_models_and_str(self):
        # SovereignIdentity __str__
        self.assertIn("coverage_user", str(self.identity))

        # GitAccessToken __str__ and is_valid
        raw_tok = GitTokenService.generate_token_raw()
        tok = GitAccessToken.objects.create(
            user=self.user,
            name="Test Token",
            token_prefix=raw_tok[:12],
            token_hash=GitTokenService.hash_token(raw_tok),
            permissions="read",
            expires_at=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
        )
        self.assertIn("Test Token", str(tok))
        self.assertTrue(tok.is_valid())

        # Inactive token is_valid
        tok.is_active = False
        self.assertFalse(tok.is_valid())

        # Expired token is_valid
        tok.is_active = True
        tok.expires_at = timezone.now() - timezone.timedelta(days=1)
        self.assertFalse(tok.is_valid())

        # Test hash_to_int with bytes and arbitrary objects
        val_bytes = ZKPCrypto.hash_to_int(b"some_bytes", 12345, ["list_item"])
        self.assertIsInstance(val_bytes, int)

        # Test verify_proof with invalid subgroup public key
        invalid_pub_key = P - 1
        proof_sample = {"commitment_t": "0x123", "response_s": "0x456", "message": "msg"}
        self.assertFalse(ZKPCrypto.verify_proof(invalid_pub_key, proof_sample))

    def test_zkp_auth_tokens_and_views_branches(self):
        # Issue token for non-existent user
        res_tok = GitTokenService.issue_token_with_zkp(
            username="non_existent", challenge_nonce="nonce", commitment_t="0x123", response_s="0x456"
        )
        self.assertFalse(res_tok["success"])

        # Validate non-existent token format
        res_val1 = GitTokenService.validate_token("invalid_prefix_123")
        self.assertFalse(res_val1["valid"])

        # Validate valid prefix but non-existent token
        res_val2 = GitTokenService.validate_token("bnt_git_" + "0" * 40)
        self.assertFalse(res_val2["valid"])

        # ZKP Register View errors
        res_reg1 = self.client.post("/api/zkp/register/", {}, content_type="application/json")
        self.assertEqual(res_reg1.status_code, 400)

        res_reg2 = self.client.post(
            "/api/zkp/register/",
            {"username": self.user.username, "public_key_y": hex(self.y)},
            content_type="application/json",
        )
        self.assertEqual(res_reg2.status_code, 400)

        res_reg3 = self.client.post(
            "/api/zkp/register/", {"username": "new_user", "public_key_y": "not_hex"}, content_type="application/json"
        )
        self.assertEqual(res_reg3.status_code, 400)

        # ZKP Challenge View missing username
        res_chal = self.client.post("/api/zkp/challenge/", {}, content_type="application/json")
        self.assertEqual(res_chal.status_code, 400)

        # ZKP Verify View incomplete params
        res_ver1 = self.client.post("/api/zkp/verify/", {"username": "abc"}, content_type="application/json")
        self.assertEqual(res_ver1.status_code, 400)

        # ZKP Verify View non-existent challenge or user
        res_ver2 = self.client.post(
            "/api/zkp/verify/",
            {
                "username": "non_existent_usr",
                "challenge_nonce": "non_existent_nonce",
                "commitment_t": "0x123",
                "response_s": "0x456",
            },
            content_type="application/json",
        )
        self.assertEqual(res_ver2.status_code, 401)

        # GitTokenGenerateView missing params
        res_gen = self.client.post("/api/zkp/tokens/generate/", {}, content_type="application/json")
        self.assertEqual(res_gen.status_code, 400)

        # GitTokenValidateView missing token
        res_val_view = self.client.post("/api/zkp/tokens/validate/", {}, content_type="application/json")
        self.assertEqual(res_val_view.status_code, 400)

        # ZKP UserInfo View (T-GIT-301)
        from rest_framework.test import APIClient

        anon_client = APIClient()
        res_userinfo_missing = anon_client.get("/api/zkp/userinfo/")
        self.assertEqual(res_userinfo_missing.status_code, 400)

        res_userinfo_notfound = anon_client.get("/api/zkp/userinfo/?username=non_existent_zkp_user")
        self.assertEqual(res_userinfo_notfound.status_code, 404)

        res_userinfo_ok = anon_client.get(f"/api/zkp/userinfo/?username={self.user.username}")
        self.assertEqual(res_userinfo_ok.status_code, 200)
        self.assertEqual(res_userinfo_ok.json()["username"], self.user.username)
        self.assertEqual(res_userinfo_ok.json()["country_code"], "CIV")

        # ZKP Rotate Key View (T-SEC-504)
        auth_client = APIClient()
        auth_client.force_authenticate(user=self.user)
        res_rot_bad1 = auth_client.post("/api/zkp/rotate-key/", {}, format="json")
        self.assertEqual(res_rot_bad1.status_code, 400)

        res_rot_bad2 = auth_client.post("/api/zkp/rotate-key/", {"new_public_key_y": "invalid_hex"}, format="json")
        self.assertEqual(res_rot_bad2.status_code, 400)

        _, new_y = ZKPCrypto.generate_keypair()
        res_rot_ok = auth_client.post("/api/zkp/rotate-key/", {"new_public_key_y": hex(new_y)}, format="json")
        self.assertEqual(res_rot_ok.status_code, 200)
        self.assertTrue(res_rot_ok.json()["success"])

    # -------------------------------------------------------------
    # 4. finetuning/export_gguf (SOUV-04)
    # -------------------------------------------------------------
    def test_finetuning_export_gguf_tool(self):
        import os
        import tempfile

        from finetuning.export_gguf import export_to_gguf

        # Dry run execution
        res_dry = export_to_gguf(
            weights_dir="finetuning/lora_gemma_weights",
            output_path="finetuning/test_model.gguf",
            quantization="q4_k_m",
            dry_run=True,
        )
        self.assertEqual(res_dry, 0)

        # Actual file generation
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = f"{tmpdir}/output_model.gguf"
            res_actual = export_to_gguf(
                weights_dir=f"{tmpdir}/weights",
                output_path=out_path,
                quantization="q4_k_m",
                dry_run=False,
            )
            self.assertEqual(res_actual, 0)
            self.assertTrue(os.path.exists(out_path))
            with open(out_path, "rb") as f:
                header = f.read(4)
                self.assertEqual(header, b"GGUF")

    def test_zkp_tasks_and_session_invalidation(self):
        """Couverture pour apps/zkp_auth/tasks.py et invalidation de sessions."""
        from django.contrib.sessions.backends.db import SessionStore

        from apps.zkp_auth.tasks import purge_expired_zkp_challenges
        from apps.zkp_auth.views import invalidate_user_sessions

        # Create active session for user
        s = SessionStore()
        s["_auth_user_id"] = str(self.user.id)
        s.save()

        count = invalidate_user_sessions(self.user)
        self.assertGreaterEqual(count, 1)

        # Purge Celery task
        res = purge_expired_zkp_challenges()
        self.assertIsInstance(res, int)

    def test_security_scanner_engine_and_ast_visitor_exhaustive(self):
        """Couverture complète pour engine.py, AST visitor, Shannon entropy et SAST serializer."""
        import ast

        from apps.security_scanner.engine import (
            PythonASTSecurityVisitor,
            SecurityScannerEngine,
            calculate_shannon_entropy,
        )
        from apps.security_scanner.models import SecurityAuditReport
        from apps.security_scanner.serializers import SarifReportSerializer

        # 1. Shannon entropy edge cases
        self.assertEqual(calculate_shannon_entropy(""), 0.0)

        # 2. AST Visitor aliases & calls
        ast_code = """
import os as my_os
from os import system as sys_exec

alias_eval = eval
alias_sys = os.system

my_os.system("ls")
sys_exec("whoami")
alias_eval("1 + 1")
alias_sys("id")
"""
        tree = ast.parse(ast_code, filename="test_ast.py")
        visitor = PythonASTSecurityVisitor(filename="test_ast.py")
        visitor.visit(tree)
        self.assertGreaterEqual(len(visitor.issues), 4)

        # 3. High entropy secret detection & URL ignore
        code_with_high_entropy = """
secret_token = "aB3+kL9/xY2zmN8qpQ1swZ7pvR4wtE5uK"
safe_url = "https://sovereign.bantudevlab.africa/api/v1/resource/endpoint"
"""
        scan_res = SecurityScannerEngine.scan_code("entropy.py", code_with_high_entropy)
        self.assertEqual(scan_res["critical"], 1)

        # 4. Invalid syntax fallback
        invalid_code = "def invalid_syntax(: {{"
        scan_invalid = SecurityScannerEngine.scan_code("syntax_err.py", invalid_code)
        self.assertIsNotNone(scan_invalid)

        # 5. Low score (score < 50 -> CRITICAL_RISK)
        bad_code = """
import os
os.system("rm -rf /")
eval("bad")
exec("bad")
password = "hardcoded_password_12345"
aws_key = "AKIA1234567890ABCDEF"
secret2 = "9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d"
"""
        scan_bad = SecurityScannerEngine.scan_code("bad.py", bad_code)
        self.assertEqual(scan_bad["status_rating"], "CRITICAL_RISK")

        # 6. GitLab SAST serializer with raw findings
        report = SecurityAuditReport.objects.create(
            repository_name="test_repo",
            file_scanned="vuln.py",
            sovereignty_score=35,
            status_rating="CRITICAL_RISK",
            raw_findings=[
                {
                    "type": "SECRET_LEAK",
                    "description": "High entropy token",
                    "severity": "CRITICAL",
                    "file": "vuln.py",
                    "line": 2,
                },
                {
                    "type": "CODE_VULN",
                    "description": "Command execution",
                    "severity": "HIGH",
                    "file": "vuln.py",
                    "line": 5,
                },
            ],
        )
        sast_artifact = SarifReportSerializer.serialize_gitlab_sast(report)
        self.assertEqual(len(sast_artifact["vulnerabilities"]), 2)
        self.assertEqual(sast_artifact["vulnerabilities"][0]["severity"], "Critical")

    def test_coverage_gap_fillers(self):
        """Comblement precis des branches pour atteindre > 97% sur zkp_auth, security_scanner et ai_assistant."""
        from unittest.mock import patch

        from apps.ai_assistant.views import mask_secrets, validate_input
        from apps.security_scanner.tasks import async_scan_code
        from apps.zkp_auth.models import ZKPChallenge
        from apps.zkp_auth.tasks import purge_expired_zkp_challenges
        from apps.zkp_auth.tokens import GitTokenService

        # 1. ai_assistant gaps
        self.assertEqual(mask_secrets("test"), "test")
        self.assertEqual(validate_input("print(1)", "a" * 100), "context invalide")

        # GET request with valid code
        res_get_valid = self.client.get("/api/ai/review/?code=print(1)&context=review")
        self.assertEqual(res_get_valid.status_code, 200)

        # Successful streaming response
        valid_code = "def valid_code():\n    return 42\n"
        res_stream_ok = self.client.post(
            "/api/ai/review/",
            {"code": valid_code, "stream": True},
            content_type="application/json",
        )
        self.assertEqual(res_stream_ok.status_code, 200)
        chunks = list(res_stream_ok.streaming_content)
        self.assertGreater(len(chunks), 0)

        # 2. security_scanner tasks & async view
        clean_content = "x = 1\ny = 2\n"
        scan_task_res = async_scan_code(filename="clean.py", content=clean_content)
        self.assertEqual(scan_task_res["total_issues"], 0)

        with patch("apps.security_scanner.tasks.async_scan_code.delay") as mock_scan_delay:
            mock_task = MagicMock()
            mock_task.id = "mock-scan-task-42"
            mock_scan_delay.return_value = mock_task
            res_async_view = self.client.post(
                "/api/security/scan/",
                {"filename": "app.py", "content": "x = 1", "async": True},
                content_type="application/json",
            )
            self.assertEqual(res_async_view.status_code, 202)
            self.assertEqual(res_async_view.json()["status"], "PENDING")
            self.assertEqual(res_async_view.json()["task_id"], "mock-scan-task-42")

        # 3. zkp_auth gaps (task exception, token validation, crypto validation)
        with patch.object(ZKPChallenge, "purge_expired_challenges", side_effect=Exception("DB Error")):
            self.assertEqual(purge_expired_zkp_challenges(), 0)

        # Valid git token validation
        from apps.zkp_auth.models import GitAccessToken

        raw_tok = GitTokenService.generate_token_raw()
        GitAccessToken.objects.create(
            user=self.user,
            name="gap_token",
            token_prefix=raw_tok[:12],
            token_hash=GitTokenService.hash_token(raw_tok),
            permissions="write",
            expires_at=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
        )
        val_res = self.client.post(
            "/api/zkp/tokens/validate/",
            {"token": raw_tok},
            content_type="application/json",
        )
        self.assertEqual(val_res.status_code, 200)
        self.assertTrue(val_res.json()["valid"])

        # Crypto error paths
        self.assertFalse(ZKPCrypto.validate_public_key("not_an_int"))
        self.assertFalse(ZKPCrypto.verify_proof(self.y, {"commitment_t": "xyz"}))
        self.assertFalse(ZKPCrypto.verify_proof(self.y, {"commitment_t": "0", "response_s": "1", "message": "msg"}))
        self.assertFalse(
            ZKPCrypto.verify_proof(self.y, {"commitment_t": "2", "response_s": hex(P + 10), "message": "msg"})
        )
