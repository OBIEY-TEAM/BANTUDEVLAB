import json
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.core.cache import cache
from django.test import Client, TestCase

from apps.gitlab_client.client import GitLabClient


class GitLabClientTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()

    def test_gitlab_client_initialization(self):
        client = GitLabClient(url="http://test-gitlab.local:3001", private_token="secret-token-123")
        self.assertEqual(client.url, "http://test-gitlab.local:3001")
        self.assertEqual(client.token, "secret-token-123")

    @patch("gitlab.Gitlab")
    def test_gitlab_client_list_repositories_with_sdk(self, mock_gitlab_cls):
        mock_gl = MagicMock()
        mock_p1 = MagicMock()
        mock_p1.id = 101
        mock_p1.name = "afri-fintech-gateway"
        mock_p1.path_with_namespace = "sovereign-org/afri-fintech-gateway"
        mock_p1.description = "Passerelle bancaire panafricaine"
        mock_p1.star_count = 12
        mock_p1.forks_count = 4
        mock_p1.web_url = "http://localhost:3001/sovereign-org/afri-fintech-gateway"
        mock_p1.http_url_to_repo = "http://localhost:3001/sovereign-org/afri-fintech-gateway.git"
        mock_p1.default_branch = "main"

        mock_gl.projects.list.return_value = [mock_p1]
        mock_gitlab_cls.return_value = mock_gl

        client = GitLabClient()
        client.gl = mock_gl

        repos = client.list_repositories()
        self.assertEqual(len(repos), 1)
        self.assertEqual(repos[0]["id"], 101)
        self.assertEqual(repos[0]["name"], "afri-fintech-gateway")
        self.assertEqual(repos[0]["sovereignty_level"], "Tier-1 Continental")

        # Vérifier que le résultat est mis en cache
        cached = cache.get(client.CACHE_KEY_PROJECTS)
        self.assertIsNotNone(cached)
        self.assertEqual(cached[0]["name"], "afri-fintech-gateway")

    @patch("requests.get")
    def test_gitlab_client_fallback_http(self, mock_requests_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [
            {
                "id": 202,
                "name": "agro-sentinel-ai",
                "path_with_namespace": "sovereign-org/agro-sentinel-ai",
                "description": "IA agricole souveraine",
                "star_count": 8,
                "forks_count": 2,
                "web_url": "http://localhost:3001/sovereign-org/agro-sentinel-ai",
                "http_url_to_repo": "http://localhost:3001/sovereign-org/agro-sentinel-ai.git",
                "default_branch": "main",
            }
        ]
        mock_requests_get.return_value = mock_resp

        client = GitLabClient()
        client.gl = None  # Simule l'échec ou l'absence du SDK

        repos = client.list_repositories()
        self.assertEqual(len(repos), 1)
        self.assertEqual(repos[0]["id"], 202)
        self.assertEqual(repos[0]["name"], "agro-sentinel-ai")

    def test_gitlab_client_get_version(self):
        client = GitLabClient()
        version = client.get_version()
        self.assertIn("version", version)
        self.assertIn("status", version)

    def test_gitlab_webhook_receiver_invalid_token(self):
        payload = json.dumps({"project": {"name": "mon-depot"}})
        response = self.client.post(
            "/api/gitlab/webhook/",
            data=payload,
            content_type="application/json",
            headers={"X-Gitlab-Token": "mauvais-token"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("error", response.json())

    def test_gitlab_webhook_receiver_valid_token(self):
        secret = getattr(settings, "GITLAB_WEBHOOK_SECRET", "bantu_gitlab_webhook_secret_2026")
        payload = {
            "project": {"name": "afri-fintech-gateway"},
            "user_username": "ibrahim_dev",
            "commits": [{"id": "sha123", "message": "feat: integration zkp et gitlab"}],
        }
        response = self.client.post(
            "/api/gitlab/webhook/",
            data=json.dumps(payload),
            content_type="application/json",
            headers={
                "X-Gitlab-Token": secret,
                "X-Gitlab-Event": "Push Hook",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["received"])
        self.assertEqual(data["project"], "afri-fintech-gateway")
        self.assertEqual(data["triggered_by"], "ibrahim_dev")
        self.assertIn("GitLab CE Panafricain", data["engine"])

    def test_gitlab_webhook_receiver_invalid_json(self):
        secret = getattr(settings, "GITLAB_WEBHOOK_SECRET", "bantu_gitlab_webhook_secret_2026")
        response = self.client.post(
            "/api/gitlab/webhook/",
            data="invalid-json-payload-string",
            content_type="application/json",
            headers={"X-Gitlab-Token": secret},
        )
        self.assertEqual(response.status_code, 400)
