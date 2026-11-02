"""
Test de charge haute performance (> 1 000 utilisateurs concurrents) pour BANTUDEVLAB (T-TST-504).
Simule les flux de requetes Git Smart HTTP, de verification Zero-Trust ZKP, d'audit SAST et d'appels API GitLab.
"""

from locust import HttpUser, between, task


class BantuDevLabLoadTestUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def test_homepage_and_dashboard(self):
        self.client.get("/")
        self.client.get("/dashboard/")
        self.client.get("/metrics/")

    @task(2)
    def test_healthchecks(self):
        self.client.get("/healthz")
        self.client.get("/readyz")

    @task(2)
    def test_zkp_challenge_request(self):
        self.client.post("/api/zkp/challenge/", json={"username": "test_user_load"})

    @task(2)
    def test_gitlab_projects_and_mrs(self):
        self.client.get("/api/merge-requests/101/approvals/")

    @task(1)
    def test_security_scan_api(self):
        self.client.post("/api/security/scan/", json={"filename": "fintech.py", "content": "x = 1"})
