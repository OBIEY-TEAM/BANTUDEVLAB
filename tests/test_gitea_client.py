from unittest.mock import patch

from django.test import TestCase

from apps.gitea_client.client import GiteaClient


class GiteaClientTestCase(TestCase):
    def test_client_initialization(self):
        client = GiteaClient()
        self.assertIsNotNone(client.api_url)

    @patch("apps.gitea_client.client.requests.get")
    def test_list_repositories_fallback(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": [{"name": "repo-souverain-test", "id": 1}]}
        client = GiteaClient()
        repos = client.list_repositories(use_cache=False)
        self.assertIsInstance(repos, list)
        self.assertGreater(len(repos), 0)
        self.assertIn("name", repos[0])

    def test_server_version(self):
        client = GiteaClient()
        version = client.get_server_version()
        self.assertTrue(version.get("success"))

    def test_create_repository(self):
        client = GiteaClient()
        res = client.create_repository(name="sovereign-smart-contract", description="Test repo")
        self.assertTrue(res.get("success"))
        self.assertEqual(res["data"]["name"], "sovereign-smart-contract")

    def test_t_whk_1401_webhook_redeliver_endpoint(self):
        """T-WHK-1401 : Verification du rejeu de webhook."""
        from django.test import Client

        client = Client()
        res = client.post(
            "/api/forge/webhooks/redeliver/",
            data={
                "event": "push",
                "delivery_id": "deliv-12345",
                "payload": {"ref": "refs/heads/main"},
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertTrue(data["redelivered"])
        self.assertEqual(data["event"], "push")
        self.assertEqual(data["delivery_id"], "deliv-12345")

    def test_t_whk_1401_webhook_redeliver_missing_payload(self):
        from django.test import Client

        client = Client()
        res = client.post(
            "/api/forge/webhooks/redeliver/",
            data={"event": "push"},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)

    def test_demo_repo_creation_appears_in_list_and_dashboard(self):
        from django.contrib.auth import get_user_model

        demo_user = get_user_model().objects.create_user(username="cadev_evaluator", password="x")
        self.client.force_login(demo_user)
        with patch("apps.gitea_client.client.GiteaClient.create_repository") as mock_create, patch(
            "apps.gitea_client.client.GiteaClient.list_repositories", return_value=[]
        ):
            mock_create.return_value = {
                "success": True,
                "fallback": True,
                "data": {
                    "id": 99,
                    "name": "demo-cadev-sovereign",
                    "full_name": "cadev_evaluator/demo-cadev-sovereign",
                    "owner": {"username": "cadev_evaluator"},
                    "html_url": "https://git.cybersocle.site/cadev_evaluator/demo-cadev-sovereign",
                    "clone_url": "https://git.cybersocle.site/cadev_evaluator/demo-cadev-sovereign.git",
                },
            }
            res_create = self.client.post(
                "/api/forge/repositories/",
                data={"name": "demo-cadev-sovereign", "description": "Demo repo"},
                content_type="application/json",
            )
            self.assertEqual(res_create.status_code, 201)

            res_list = self.client.get("/api/forge/repositories/")
            self.assertEqual(res_list.status_code, 200)
            names = [r["name"] for r in res_list.json().get("repositories", [])]
            self.assertIn("demo-cadev-sovereign", names)

            res_dash = self.client.get("/dashboard/")
            self.assertEqual(res_dash.status_code, 200)
            self.assertContains(res_dash, "demo-cadev-sovereign")
