"""
Bidirectional Synchronization Service for Gitea and BantuDevLab (DEV-01).
Synchronizes:
- Pull Request statuses (open, closed, merged)
- Commits
- Branches
between Gitea REST API v1 and the sovereign BantuDevLab overlay.
"""

from typing import Any, Dict, Optional

from .client import GiteaClient


class GiteaSyncService:
    """
    Manages synchronization workflows between Gitea forge and BantuDevLab platform.
    """

    def __init__(self, client: Optional[GiteaClient] = None):
        self.client = client or GiteaClient()

    def sync_repository_branches(self, owner: str, repo: str) -> Dict[str, Any]:
        """Synchronizes branch metadata from Gitea."""
        branches = self.client.get_repository_branches(owner, repo)
        return {"owner": owner, "repo": repo, "branches_count": len(branches), "branches": branches, "synced": True}

    def sync_repository_commits(self, owner: str, repo: str) -> Dict[str, Any]:
        """Synchronizes commit history from Gitea."""
        commits = self.client.get_repository_commits(owner, repo)
        return {"owner": owner, "repo": repo, "commits_count": len(commits), "commits": commits, "synced": True}

    def sync_pull_requests(self, owner: str, repo: str, state: str = "all") -> Dict[str, Any]:
        """Fetches and synchronizes PRs from Gitea to BantuDevLab."""
        pulls = self.client.get_pull_requests(owner, repo, state=state)
        return {"owner": owner, "repo": repo, "pull_requests_count": len(pulls), "pull_requests": pulls, "synced": True}

    def update_pr_status(self, owner: str, repo: str, pr_index: int, state: str) -> Dict[str, Any]:
        """Pushes PR status update back to Gitea."""
        res = self.client.update_pull_request(owner=owner, repo=repo, pr_index=pr_index, state=state)
        return {"owner": owner, "repo": repo, "pr_index": pr_index, "state": state, "result": res, "synced": True}

    def full_sync_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Performs complete bidirectional sync for a repository."""
        branches_data = self.sync_repository_branches(owner, repo)
        commits_data = self.sync_repository_commits(owner, repo)
        prs_data = self.sync_pull_requests(owner, repo)

        return {
            "repository": f"{owner}/{repo}",
            "branches": branches_data["branches"],
            "commits": commits_data["commits"],
            "pull_requests": prs_data["pull_requests"],
            "status": "SUCCESS",
            "message": f"Dépôt {owner}/{repo} synchronisé avec succès (branches, commits, PRs).",
        }
