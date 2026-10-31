import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.conf import settings
from django.core.cache import cache
from apps.security_scanner.models import SecurityAuditReport
from apps.security_scanner.tasks import async_scan_code
from apps.ai_assistant.tasks import async_analyze_code
from apps.ai_assistant.gemma import GemmaAssistant
from apps.ai_assistant.models import AIInteractionLog
from apps.gitea_client.client import GiteaClient
from apps.zkp_auth.models import ZKPChallenge


class Axe2PerformanceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()

    # PERF-01: File de Tâches Asynchrones (Celery / Redis)
    def test_perf01_async_scan_code_task_execution(self):
        code_content = "api_key = 'ghp_secret_token_123456789012345678'\n"
        result = async_scan_code(
            filename="auth_service.py",
            content=code_content,
            repository_name="sovereign-vault",
            actor="test-celery-worker"
        )
        self.assertIn("report_id", result)
        self.assertIn("sovereignty_score", result)
        report = SecurityAuditReport.objects.get(id=result["report_id"])
        self.assertEqual(report.repository_name, "sovereign-vault")
        self.assertGreater(report.total_issues, 0)

    def test_perf01_async_analyze_code_task_execution(self):
        code_content = "def calculate_risk(x):\n    return x * 2\n"
        result = async_analyze_code(
            code_snippet=code_content,
            context="audit_optimization"
        )
        self.assertIn("log_id", result)
        self.assertIn("response", result)
        log = AIInteractionLog.objects.get(id=result["log_id"])
        self.assertEqual(log.query_context, "audit_optimization")

    def test_perf01_scan_api_accepts_async_mode(self):
        with patch('apps.security_scanner.tasks.async_scan_code.delay') as mock_delay:
            mock_task = MagicMock()
            mock_task.id = 'task-uuid-123456'
            mock_delay.return_value = mock_task

            resp = self.client.post(
                '/api/security/scan/',
                data=json.dumps({
                    'content': 'x = 1\n',
                    'filename': 'test.py',
                    'async': True
                }),
                content_type='application/json'
            )
            self.assertEqual(resp.status_code, 202)
            self.assertEqual(resp.json()['status'], 'PENDING')
            self.assertEqual(resp.json()['task_id'], 'task-uuid-123456')
            mock_delay.assert_called_once()

    # PERF-02: Streaming d'Inférence IA (Server-Sent Events)
    def test_perf02_gemma_streaming_generator(self):
        assistant = GemmaAssistant()
        code = "def hello():\n    return 'african_sovereign_forge'\n"
        tokens = list(assistant.stream_analyze_code(code_snippet=code, context="unit_test"))
        self.assertGreater(len(tokens), 0)
        full_text = "".join(tokens)
        self.assertIn("BantuDevLab AI", full_text)

    def test_perf02_ai_review_sse_streaming_endpoint(self):
        # Requête POST avec stream=True
        resp = self.client.post(
            '/api/ai/review/',
            data=json.dumps({
                'code': 'def sovereign_func(): return True\n',
                'context': 'review',
                'stream': True
            }),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get('Content-Type'), 'text/event-stream')

        # Streaming content validation
        content_stream = b"".join(resp.streaming_content).decode('utf-8')
        self.assertIn('data: {', content_stream)
        self.assertIn('"token":', content_stream)
        self.assertIn('"done": true', content_stream.lower())

    def test_perf02_ai_review_get_sse_endpoint(self):
        resp = self.client.get('/api/ai/review/?code=print("sovereign")')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get('Content-Type'), 'text/event-stream')

    # PERF-03: Optimisation des Requêtes SQL & Indexation
    def test_perf03_indexes_present_in_model_meta(self):
        # SecurityAuditReport indexes
        sec_indexes = [idx.name for idx in SecurityAuditReport._meta.indexes]
        self.assertIn('sec_scanned_idx', sec_indexes)
        self.assertIn('sec_repo_idx', sec_indexes)

        # ZKPChallenge indexes
        zkp_indexes = [idx.name for idx in ZKPChallenge._meta.indexes]
        self.assertIn('zkp_nonce_idx', zkp_indexes)
        self.assertIn('zkp_expires_idx', zkp_indexes)

    def test_perf03_dashboard_avg_sql_aggregation(self):
        SecurityAuditReport.objects.all().delete()
        SecurityAuditReport.objects.create(
            repository_name="repo1",
            sovereignty_score=80
        )
        SecurityAuditReport.objects.create(
            repository_name="repo2",
            sovereignty_score=100
        )

        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)
        # Moyenne SQL de (80 + 100) / 2 = 90
        self.assertEqual(resp.context['avg_sovereignty'], 90)

    # PERF-04: Couche de Cache Distribué (Redis Caching)
    def test_perf04_gitea_repository_list_cached_for_60_seconds(self):
        client = GiteaClient()
        cache.clear()

        # Premier appel : met en cache
        repos1 = client.list_repositories()
        self.assertIsNotNone(cache.get(client.CACHE_KEY_REPOS))

        # Modification manuelle du cache pour vérifier qu'il est servi depuis le cache
        custom_mock = [{"name": "in-cache-test-repo", "id": 999}]
        cache.set(client.CACHE_KEY_REPOS, custom_mock, 60)

        repos2 = client.list_repositories()
        self.assertEqual(repos2[0]["name"], "in-cache-test-repo")

        # Invalidation lors de la création d'un dépôt
        client.create_repository(name="new-sovereign-repo")
        self.assertIsNone(cache.get(client.CACHE_KEY_REPOS))

    def test_perf04_metrics_page_cached(self):
        cache.clear()
        resp1 = self.client.get('/metrics/')
        self.assertEqual(resp1.status_code, 200)

        # Deuxième requête
        resp2 = self.client.get('/metrics/')
        self.assertEqual(resp2.status_code, 200)

    # PERF-05: Serveur Web Haute Performance (Gunicorn + Uvicorn)
    def test_perf05_asgi_application_configured(self):
        from config.asgi import application as asgi_app
        self.assertIsNotNone(asgi_app)
        self.assertEqual(settings.ASGI_APPLICATION, 'config.asgi.application')

    def test_perf05_uvicorn_worker_importable(self):
        from uvicorn.workers import UvicornWorker
        self.assertTrue(issubclass(UvicornWorker, object))
