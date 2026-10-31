from django.test import TestCase
from apps.gitea_client.client import GiteaClient
from apps.gitea_client.models import SovereignRepository

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
