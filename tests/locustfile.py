"""
Test de charge et montee en capacite (500 utilisateurs concurrents) pour BANTUDEVLAB.
Simule les flux de requetes Git, de verification Zero-Trust ZKP et d'appels API.
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

    @task(1)
    def test_gitlab_projects_api(self):
        self.client.get("/api/gitlab/webhook/")
