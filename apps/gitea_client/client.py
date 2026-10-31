"""
Modular API Client for Gitea / GitLab CE.
Provides seamless interaction between the BantuDevLab sovereign platform
and the underlying open-source Git forge.
"""

import requests
from django.conf import settings
from django.core.cache import cache
from typing import List, Dict, Any, Optional


class GiteaClient:
    """
    Client for interacting with Gitea REST API v1.
    Includes mock fallback mode if Gitea container is starting up or in offline/demo mode.
    Caches repository listings for 60 seconds (PERF-04).
    """

    CACHE_KEY_REPOS = 'gitea_repos_list'
    CACHE_TTL = 60

    def __init__(self, api_url: Optional[str] = None, token: Optional[str] = None):
        self.api_url = (api_url or getattr(settings, 'GITEA_API_URL', 'http://localhost:3000/api/v1')).rstrip('/')
        self.token = token or getattr(settings, 'GITEA_ADMIN_TOKEN', '')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "status_code": 200}
            return {"success": False, "error": response.text, "status_code": response.status_code}
        except Exception as e:
            return {"success": False, "error": str(e), "fallback": True}

    def _post(self, endpoint: str, json_data: Dict) -> Dict[str, Any]:
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.post(url, headers=self.headers, json=json_data, timeout=5)
            if response.status_code in (200, 201):
                return {"success": True, "data": response.json(), "status_code": response.status_code}
            return {"success": False, "error": response.text, "status_code": response.status_code}
        except Exception as e:
            return {"success": False, "error": str(e), "fallback": True}

    def _patch(self, endpoint: str, json_data: Dict) -> Dict[str, Any]:
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.patch(url, headers=self.headers, json=json_data, timeout=5)
            if response.status_code in (200, 201):
                return {"success": True, "data": response.json(), "status_code": response.status_code}
            return {"success": False, "error": response.text, "status_code": response.status_code}
        except Exception as e:
            return {"success": False, "error": str(e), "fallback": True}

    def get_server_version(self) -> Dict[str, Any]:
        """Returns Gitea server version or sovereign simulated response."""
        res = self._get('/version')
        if res.get('success'):
            return res
        return {
            "success": True,
            "data": {"version": "1.23.0-sovereign", "status": "Systalink Cloud Sovereign Forge"},
            "fallback": True
        }

    def list_repositories(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """Lists sovereign repositories, cached for 60 seconds (PERF-04)."""
        if use_cache:
            cached_repos = cache.get(self.CACHE_KEY_REPOS)
            if cached_repos is not None:
                return cached_repos

        res = self._get('/repos/search', params={'limit': 50})
        if res.get('success') and 'data' in res:
            repos = res['data'].get('data', [])
        else:
            # Sovereign default mock repositories for demo/hackathon display
            repos = [
                {
                    "id": 1,
                    "name": "afri-fintech-gateway",
                    "full_name": "sovereign-org/afri-fintech-gateway",
                    "description": "Passerelle panafricaine de paiement mobile & interopérabilité souveraine",
                    "private": False,
                    "stars_count": 42,
                    "forks_count": 12,
                    "open_issues_count": 3,
                    "owner": {"username": "afri-foundation"},
                    "clone_url": "https://forge.bantudevlab.africa/sovereign-org/afri-fintech-gateway.git",
                    "html_url": "https://forge.bantudevlab.africa/sovereign-org/afri-fintech-gateway",
                    "default_branch": "main",
                    "sovereignty_level": "Tier-1 Continental",
                },
                {
                    "id": 2,
                    "name": "agro-sentinel-ai",
                    "full_name": "sovereign-org/agro-sentinel-ai",
                    "description": "Modèles de vision embarquée pour la surveillance des récoltes sahéliennes",
                    "private": False,
                    "stars_count": 89,
                    "forks_count": 27,
                    "open_issues_count": 5,
                    "owner": {"username": "agro-tech-ci"},
                    "clone_url": "https://forge.bantudevlab.africa/sovereign-org/agro-sentinel-ai.git",
                    "html_url": "https://forge.bantudevlab.africa/sovereign-org/agro-sentinel-ai",
                    "default_branch": "main",
                    "sovereignty_level": "Tier-1 Continental",
                },
                {
                    "id": 3,
                    "name": "bantu-zkp-identity",
                    "full_name": "bantudevlab/bantu-zkp-identity",
                    "description": "Bibliothèque cryptographique Zero-Knowledge Proof pour l'Afrique de l'Ouest",
                    "private": False,
                    "stars_count": 154,
                    "forks_count": 34,
                    "open_issues_count": 1,
                    "owner": {"username": "bantudevlab"},
                    "clone_url": "https://forge.bantudevlab.africa/bantudevlab/bantu-zkp-identity.git",
                    "html_url": "https://forge.bantudevlab.africa/bantudevlab/bantu-zkp-identity",
                    "default_branch": "main",
                    "sovereignty_level": "Tier-1 Continental",
                }
            ]

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
            "default_branch": "main"
        }
        res = self._post('/user/repos', payload)
        # Invalider le cache des dépôts
        cache.delete(self.CACHE_KEY_REPOS)

        if res.get('success'):
            return res
        return {
            "success": True,
            "data": {
                "id": 99,
                "name": name,
                "full_name": f"sovereign-developer/{name}",
                "description": description,
                "private": private,
                "html_url": f"https://forge.bantudevlab.africa/sovereign-developer/{name}",
                "clone_url": f"https://forge.bantudevlab.africa/sovereign-developer/{name}.git"
            },
            "fallback": True
        }

    def get_repository_commits(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Retrieves commit history."""
        res = self._get(f'/repos/{owner}/{repo}/commits')
        if res.get('success') and isinstance(res.get('data'), list):
            return res['data']
        return [
            {
                "sha": "9a7f34bc8192a01d5e3",
                "commit": {
                    "author": {"name": "Kouamé N'Goran", "date": "2025-05-10T12:00:00Z"},
                    "message": "feat(crypto): add schnorr sigma zero-knowledge protocol"
                }
            },
            {
                "sha": "3b2e19aa78cd5012f45",
                "commit": {
                    "author": {"name": "Amina Diop", "date": "2025-05-09T15:30:00Z"},
                    "message": "fix(scanner): detect hardcoded private credentials and tokens"
                }
            }
        ]

    def get_repository_branches(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Retrieves list of branches for a repository."""
        res = self._get(f'/repos/{owner}/{repo}/branches')
        if res.get('success') and isinstance(res.get('data'), list):
            return res['data']
        return [
            {"name": "main", "commit": {"id": "9a7f34bc8192a01d5e3"}},
            {"name": "develop", "commit": {"id": "3b2e19aa78cd5012f45"}},
        ]

    def get_pull_requests(self, owner: str, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        """Retrieves pull requests for a repository."""
        res = self._get(f'/repos/{owner}/{repo}/pulls', params={'state': state})
        if res.get('success') and isinstance(res.get('data'), list):
            return res['data']
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
                "updated_at": "2025-05-10T12:00:00Z"
            }
        ]

    def update_pull_request(self, owner: str, repo: str, pr_index: int, state: Optional[str] = None, title: Optional[str] = None) -> Dict[str, Any]:
        """Updates PR status or title on Gitea."""
        payload: Dict[str, Any] = {}
        if state:
            payload['state'] = state
        if title:
            payload['title'] = title
        res = self._patch(f'/repos/{owner}/{repo}/pulls/{pr_index}', payload)
        if res.get('success'):
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
            "fallback": True
        }
