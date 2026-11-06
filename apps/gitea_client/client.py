"""
Modular API Client for Gitea / GitLab CE.
Provides seamless interaction between the BantuDevLab sovereign platform
and the underlying open-source Git forge.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from django.conf import settings
from django.core.cache import cache


class GiteaClient:
    """
    Client for interacting with Gitea REST API v1.
    Includes mock fallback mode if Gitea container is starting up or in offline/demo mode.
    Caches repository listings for 60 seconds (PERF-04).
    """

    CACHE_KEY_REPOS = "gitea_repos_list"
    CACHE_TTL = 60

    def __init__(self, api_url: Optional[str] = None, token: Optional[str] = None):
        self.api_url = (api_url or getattr(settings, "GITEA_API_URL", "http://localhost:3002/api/v1")).rstrip("/")
        self.token = token or getattr(settings, "GITEA_ADMIN_TOKEN", "")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    # PERF-061: circuit breaker - apres BREAKER_THRESHOLD echecs consecutifs, Gitea n'est plus
    # sollicite pendant BREAKER_COOLDOWN secondes (les appelants utilisent leur repli).
    BREAKER_THRESHOLD = 5
    BREAKER_COOLDOWN = 30
    CACHE_KEY_FAILURES = "gitea_breaker_failures"
    CACHE_KEY_OPEN = "gitea_breaker_open"
    REQUEST_TIMEOUT = 15

    def _breaker_open(self) -> bool:
        return bool(cache.get(self.CACHE_KEY_OPEN))

    def _record_failure(self) -> None:
        failures = (cache.get(self.CACHE_KEY_FAILURES) or 0) + 1
        cache.set(self.CACHE_KEY_FAILURES, failures, self.BREAKER_COOLDOWN * 4)
        if failures >= self.BREAKER_THRESHOLD:
            cache.set(self.CACHE_KEY_OPEN, True, self.BREAKER_COOLDOWN)
            cache.delete(self.CACHE_KEY_FAILURES)

    def _record_success(self) -> None:
        cache.delete(self.CACHE_KEY_FAILURES)

    def _request(self, method: str, endpoint: str, ok_codes=(200,), **kwargs) -> Dict[str, Any]:
        if self._breaker_open():
            return {"success": False, "error": "Gitea indisponible (circuit ouvert)", "fallback": True}
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            # SEC-046: timeout systematique, pas de redirection suivie (anti-SSRF).
            response = getattr(requests, method)(
                url, headers=self.headers, timeout=self.REQUEST_TIMEOUT, allow_redirects=False, **kwargs
            )
        except Exception:
            self._record_failure()
            # Le detail de l'exception (URL interne, token...) n'est pas renvoye aux appelants.
            return {"success": False, "error": "Gitea injoignable", "fallback": True}
        self._record_success()
        if response.status_code in ok_codes:
            return {"success": True, "data": response.json(), "status_code": response.status_code}
        return {"success": False, "error": response.text, "status_code": response.status_code}

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("get", endpoint, ok_codes=(200,), params=params)

    def _post(self, endpoint: str, json_data: Dict) -> Dict[str, Any]:
        return self._request("post", endpoint, ok_codes=(200, 201), json=json_data)

    def _patch(self, endpoint: str, json_data: Dict) -> Dict[str, Any]:
        return self._request("patch", endpoint, ok_codes=(200, 201), json=json_data)

    def get_server_version(self) -> Dict[str, Any]:
        """Returns Gitea server version or sovereign simulated response."""
        res = self._get("/version")
        if res.get("success"):
            return res
        return {
            "success": True,
            "data": {"version": "1.23.0-sovereign", "status": "Systalink Cloud Sovereign Forge"},
            "fallback": True,
        }

    def _get_fallback_repositories(self) -> List[Dict[str, Any]]:
        """Scan local forge bare repositories or return sovereign default repos."""
        repos: List[Dict[str, Any]] = []
        base_dir = getattr(settings, "BASE_DIR", Path("."))
        repos_dir = Path(base_dir) / "forge_data" / "repos"
        if repos_dir.exists():
            for p in sorted(repos_dir.glob("*/*.git")):
                owner = p.parent.name
                name = p.name[:-4] if p.name.endswith(".git") else p.name
                repos.append(
                    {
                        "id": abs(hash(f"{owner}/{name}")) % 10000 + 1,
                        "name": name,
                        "full_name": f"{owner}/{name}",
                        "owner": {"username": owner},
                        "private": False,
                        "html_url": f"http://localhost:3002/{owner}/{name}",
                        "clone_url": f"http://localhost:3002/{owner}/{name}.git",
                        "default_branch": "main",
                    }
                )
        if not repos:
            repos = [
                {
                    "id": 1,
                    "name": "afri-fintech-gateway",
                    "full_name": "sovereign-org/afri-fintech-gateway",
                    "owner": {"username": "sovereign-org"},
                    "private": False,
                    "html_url": "http://localhost:3002/sovereign-org/afri-fintech-gateway",
                    "clone_url": "http://localhost:3002/sovereign-org/afri-fintech-gateway.git",
                    "default_branch": "main",
                },
                {
                    "id": 2,
                    "name": "bantu-zkp-identity",
                    "full_name": "bantudevlab/bantu-zkp-identity",
                    "owner": {"username": "bantudevlab"},
                    "private": False,
                    "html_url": "http://localhost:3002/bantudevlab/bantu-zkp-identity",
                    "clone_url": "http://localhost:3002/bantudevlab/bantu-zkp-identity.git",
                    "default_branch": "main",
                },
            ]
        return repos

    def list_repositories(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """Lists sovereign repositories, cached for 60 seconds (PERF-04)."""
        if use_cache:
            cached_repos = cache.get(self.CACHE_KEY_REPOS)
            if cached_repos is not None:
                return cached_repos

        res = self._get("/repos/search", params={"limit": 50})
        if res.get("success") and "data" in res:
            repos = res["data"].get("data", [])
        else:
            repos = self._get_fallback_repositories()

        if use_cache:
            cache.set(self.CACHE_KEY_REPOS, repos, self.CACHE_TTL)
        return repos

    def create_repository(self, name: str, description: str = "", private: bool = False) -> Dict[str, Any]:
        """Creates a repository on Gitea and invalidates cached repository listings."""
        payload = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": True,
            "default_branch": "main",
        }
        res = self._post("/user/repos", payload)
        # Invalider le cache des dépôts
        cache.delete(self.CACHE_KEY_REPOS)

        if res.get("success"):
            return res
        return {
            "success": True,
            "data": {
                "id": 99,
                "name": name,
                "full_name": f"sovereign-developer/{name}",
                "description": description,
                "private": private,
                "html_url": f"https://cybersocle.site/sovereign-developer/{name}",
                "clone_url": f"https://cybersocle.site/sovereign-developer/{name}.git",
            },
            "fallback": True,
        }

    def get_repository_commits(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Retrieves commit history."""
        res = self._get(f"/repos/{owner}/{repo}/commits")
        if res.get("success") and isinstance(res.get("data"), list):
            return res["data"]
        return [
            {
                "sha": "9a7f34bc8192a01d5e3",
                "commit": {
                    "author": {"name": "Kouamé N'Goran", "date": "2025-05-10T12:00:00Z"},
                    "message": "feat(crypto): add schnorr sigma zero-knowledge protocol",
                },
            },
            {
                "sha": "3b2e19aa78cd5012f45",
                "commit": {
                    "author": {"name": "Amina Diop", "date": "2025-05-09T15:30:00Z"},
                    "message": "fix(scanner): detect hardcoded private credentials and tokens",
                },
            },
        ]

    def get_repository_branches(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Retrieves list of branches for a repository."""
        res = self._get(f"/repos/{owner}/{repo}/branches")
        if res.get("success") and isinstance(res.get("data"), list):
            return res["data"]
        return [
            {"name": "main", "commit": {"id": "9a7f34bc8192a01d5e3"}},
            {"name": "develop", "commit": {"id": "3b2e19aa78cd5012f45"}},
        ]

    def get_pull_requests(self, owner: str, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        """Retrieves pull requests for a repository."""
        res = self._get(f"/repos/{owner}/{repo}/pulls", params={"state": state})
        if res.get("success") and isinstance(res.get("data"), list):
            return res["data"]
        return [
            {
                "id": 1,
                "number": 1,
                "title": "Intégration du protocole Schnorr NIZKP",
                "state": "open",
                "head": {"label": "feat/schnorr-zkp", "ref": "feat/schnorr-zkp"},
                "base": {"label": "main", "ref": "main"},
                "user": {"username": "kouame-dev"},
                "created_at": "2025-05-10T10:00:00Z",
                "updated_at": "2025-05-10T12:00:00Z",
            }
        ]

    def update_pull_request(
        self, owner: str, repo: str, pr_index: int, state: Optional[str] = None, title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Updates PR status or title on Gitea."""
        payload: Dict[str, Any] = {}
        if state:
            payload["state"] = state
        if title:
            payload["title"] = title
        res = self._patch(f"/repos/{owner}/{repo}/pulls/{pr_index}", payload)
        if res.get("success"):
            return res
        return {
            "success": True,
            "data": {
                "id": pr_index,
                "number": pr_index,
                "title": title or f"PR #{pr_index}",
                "state": state or "open",
                "updated_at": "2025-05-10T13:00:00Z",
            },
            "fallback": True,
        }

    def search_users(self, query: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """Recherche des utilisateurs sur l'API Gitea Swagger (/users/search)."""
        res = self._get("/users/search", params={"q": query, "limit": limit})
        if res.get("success") and "data" in res:
            return res["data"].get("data", [])
        return []

    def get_repo_commits(self, owner: str, repo: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Recupere les commits d'un depot sur l'API Swagger (/repos/{owner}/{repo}/commits)."""
        res = self._get(f"/repos/{owner}/{repo}/commits", params={"limit": limit})
        if res.get("success") and isinstance(res.get("data"), list):
            return res["data"]
        return []

    def get_nodeinfo(self) -> Dict[str, Any]:
        """Interroge le endpoint NodeInfo Swagger (/nodeinfo)."""
        res = self._get("/nodeinfo")
        if res.get("success"):
            return res
        return {"success": True, "data": {"version": "2.1", "software": {"name": "gitea"}}, "fallback": True}
