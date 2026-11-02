from django.test import TestCase

from apps.gitea_client.client import GiteaClient


class GiteaClientTestCase(TestCase):
    def test_client_initialization(self):
        client = GiteaClient()
        self.assertIsNotNone(client.api_url)

    def test_list_repositories_fallback(self):
        client = GiteaClient()
        repos = client.list_repositories()
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

