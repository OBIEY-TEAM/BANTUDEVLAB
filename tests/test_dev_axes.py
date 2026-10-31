"""
Tests unitaires et d'intégration pour l'Axe 3 : Développement & Architecture Cœur de Forge (DEV).
Couvre DEV-01, DEV-02, DEV-03, DEV-04 et DEV-05.
"""

import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from apps.core.models import SovereignOrganization
from apps.gitea_client.client import GiteaClient
from apps.gitea_client.models import SovereignRepository
from apps.gitea_client.sync import GiteaSyncService
from apps.security_scanner.models import SecurityAuditReport
from apps.security_scanner.serializers import SarifReportSerializer
from apps.zkp_auth.crypto import ZKPCrypto
from apps.zkp_auth.models import SovereignIdentity, ZKPChallenge
from apps.zkp_auth.tokens import GitTokenService


class Axe3DevTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # DEV-01: Synchronisation Bidirectionnelle Gitea
    def test_dev01_gitea_client_pull_requests_and_branches(self):
        client = GiteaClient()
        branches = client.get_repository_branches(owner="sovereign-org", repo="afri-fintech-gateway")
        self.assertIsInstance(branches, list)
        self.assertGreater(len(branches), 0)
        self.assertIn("name", branches[0])

        prs = client.get_pull_requests(owner="sovereign-org", repo="afri-fintech-gateway")
        self.assertIsInstance(prs, list)
        self.assertGreater(len(prs), 0)
        self.assertEqual(prs[0]["state"], "open")

        update_res = client.update_pull_request(
            owner="sovereign-org", repo="afri-fintech-gateway", pr_index=1, state="closed"
        )
        self.assertTrue(update_res.get("success"))

    def test_dev01_gitea_sync_service_full_sync(self):
        sync_service = GiteaSyncService()
        result = sync_service.full_sync_repository(owner="sovereign-org", repo="afri-fintech-gateway")
        self.assertEqual(result["status"], "SUCCESS")
        self.assertIn("branches", result)
        self.assertIn("commits", result)
        self.assertIn("pull_requests", result)

    def test_dev01_sync_api_endpoints(self):
        # GET full sync
        get_resp = self.client.get("/api/forge/sync/?owner=sovereign-org&repo=afri-fintech-gateway")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json()["status"], "SUCCESS")

        # POST update PR status
        post_resp = self.client.post(
            "/api/forge/sync/",
            data=json.dumps(
                {
                    "owner": "sovereign-org",
                    "repo": "afri-fintech-gateway",
                    "action": "update_pr",
                    "pr_index": 1,
                    "state": "closed",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(post_resp.status_code, 200)
        self.assertTrue(post_resp.json()["synced"])

    # DEV-02: Support Multi-Tenancy & Organisations Africaines
    def test_dev02_sovereign_organization_model(self):
        org = SovereignOrganization.objects.create(
            name="Banque Centrale du Congo",
            slug="bcc-cd",
            entity_type="CENTRAL_BANK",
            country_code="COD",
            description="Banque Centrale souveraine",
            sovereignty_level="Tier-1 Continental",
        )
        self.assertEqual(str(org), "Banque Centrale du Congo (Banque Centrale - COD)")

        repo = SovereignRepository.objects.create(name="cbdc-congo-core", owner="bcc-cd", organization=org)
        self.assertEqual(repo.organization, org)
        self.assertEqual(org.repositories.count(), 1)

    def test_dev02_organization_api_endpoints(self):
        # Création d'une organisation
        create_resp = self.client.post(
            "/api/organizations/",
            data=json.dumps(
                {
                    "name": "Ministère de l Économie Numérique Sénégal",
                    "slug": "men-sn",
                    "entity_type": "MINISTRY",
                    "country_code": "SEN",
                    "description": "Entité publique souveraine",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)
        self.assertIn("organization", create_resp.json())

        # Liste et filtrage
        list_resp = self.client.get("/api/organizations/?country=SEN")
        self.assertEqual(list_resp.status_code, 200)
        data = list_resp.json()
        self.assertGreaterEqual(data["count"], 1)
        self.assertEqual(data["organizations"][0]["slug"], "men-sn")

    # DEV-03: Générateur et Validateur de Tokens d'Accès CLI Git
    def test_dev03_token_generation_and_validation_with_zkp(self):
        # Création d'un utilisateur et de son identité ZKP
        user = User.objects.create_user(username="fatou_dev", email="fatou@bantudevlab.africa")
        x, y = ZKPCrypto.generate_keypair()
        SovereignIdentity.objects.create(user=user, public_key_y=hex(y), country_code="CIV")

        chal = ZKPChallenge.create_challenge(user=user)
        proof = ZKPCrypto.generate_proof(secret_x=x, public_y=y, message=chal.challenge_nonce)

        # Génération du token
        gen_result = GitTokenService.issue_token_with_zkp(
            username="fatou_dev",
            challenge_nonce=chal.challenge_nonce,
            commitment_t=proof["commitment_t"],
            response_s=proof["response_s"],
            name="MacBook CLI Git Token",
            permissions="write",
        )
        self.assertTrue(gen_result["success"])
        raw_token = gen_result["token"]
        self.assertTrue(raw_token.startswith("bnt_git_"))

        # Validation du token
        val_result = GitTokenService.validate_token(raw_token)
        self.assertTrue(val_result["valid"])
        self.assertEqual(val_result["username"], "fatou_dev")
        self.assertEqual(val_result["permissions"], "write")

        # Invalidation sur token corrompu
        bad_val = GitTokenService.validate_token("bnt_git_corrupted_token_123456789")
        self.assertFalse(bad_val["valid"])

    def test_dev03_git_token_api_endpoints(self):
        user = User.objects.create_user(username="kofi_cli", email="kofi@bantudevlab.africa")
        x, y = ZKPCrypto.generate_keypair()
        SovereignIdentity.objects.create(user=user, public_key_y=hex(y), country_code="GHA")

        # Demande de challenge
        chal = ZKPChallenge.create_challenge(user=user)
        proof = ZKPCrypto.generate_proof(secret_x=x, public_y=y, message=chal.challenge_nonce)

        # Appel API POST /api/zkp/tokens/generate/
        resp_gen = self.client.post(
            "/api/zkp/tokens/generate/",
            data=json.dumps(
                {
                    "username": "kofi_cli",
                    "challenge_nonce": chal.challenge_nonce,
                    "commitment_t": proof["commitment_t"],
                    "response_s": proof["response_s"],
                    "name": "Kofi Linux Workstation",
                    "permissions": "write",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(resp_gen.status_code, 201)
        raw_token = resp_gen.json()["token"]

        # Appel API POST /api/zkp/tokens/validate/
        resp_val = self.client.post(
            "/api/zkp/tokens/validate/", data=json.dumps({"token": raw_token}), content_type="application/json"
        )
        self.assertEqual(resp_val.status_code, 200)
        self.assertTrue(resp_val.json()["valid"])
        self.assertEqual(resp_val.json()["username"], "kofi_cli")

    # DEV-04: Documentation API Interactive (OpenAPI / Swagger)
    def test_dev04_swagger_and_openapi_schema(self):
        schema_resp = self.client.get("/api/schema/")
        self.assertEqual(schema_resp.status_code, 200)
        self.assertIn("openapi", schema_resp.content.decode("utf-8"))

        docs_resp = self.client.get("/api/docs/")
        self.assertEqual(docs_resp.status_code, 200)
        self.assertIn("swagger-ui", docs_resp.content.decode("utf-8").lower())

    # DEV-05: Export des Rapports de Sécurité au Format SARIF
    def test_dev05_sarif_serializer_and_export(self):
        report = SecurityAuditReport.objects.create(
            repository_name="sovereign-vault-lib",
            file_scanned="auth_vault.py",
            total_issues=2,
            critical_count=1,
            high_count=1,
            medium_count=0,
            sovereignty_score=60,
            status_rating="WARNING",
            raw_findings=[
                {
                    "file": "auth_vault.py",
                    "line": 42,
                    "type": "SECRET_LEAK",
                    "severity": "CRITICAL",
                    "description": "Clé privée RSA détectée",
                    "snippet": "-----BEGIN RSA PRIVATE KEY-----",
                    "recommendation": "Utiliser BantuDevLab Vault",
                },
                {
                    "file": "auth_vault.py",
                    "line": 105,
                    "type": "VULNERABILITY",
                    "severity": "HIGH",
                    "description": "Utilisation dangereuse de eval()",
                    "snippet": "eval(user_input)",
                    "recommendation": "Supprimer eval()",
                },
            ],
        )

        sarif_obj = SarifReportSerializer.serialize(report)
        self.assertEqual(sarif_obj["version"], "2.1.0")
        self.assertEqual(len(sarif_obj["runs"]), 1)
        run = sarif_obj["runs"][0]
        self.assertEqual(run["tool"]["driver"]["name"], "BantuDevLab Sovereign Security Scanner")
        self.assertEqual(len(run["results"]), 2)
        self.assertEqual(run["results"][0]["level"], "error")
        self.assertEqual(
            run["results"][0]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"], "auth_vault.py"
        )
        self.assertEqual(run["results"][0]["locations"][0]["physicalLocation"]["region"]["startLine"], 42)

        # Test export view
        export_resp = self.client.get(f"/api/security/audits/{report.id}/sarif/")
        self.assertEqual(export_resp.status_code, 200)
        self.assertEqual(export_resp["Content-Type"], "application/sarif+json")
        self.assertEqual(export_resp.json()["version"], "2.1.0")

        # Test latest export view
        latest_resp = self.client.get("/api/security/sarif/")
        self.assertEqual(latest_resp.status_code, 200)
        self.assertEqual(latest_resp.json()["version"], "2.1.0")
