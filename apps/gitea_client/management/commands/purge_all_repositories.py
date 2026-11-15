"""Management command to purge all repositories from Gitea, Django DB, and cache."""

import os

from django.core.cache import cache
from django.core.management.base import BaseCommand

from apps.gitea_client.client import GiteaClient
from apps.gitea_client.models import SovereignRepository


class Command(BaseCommand):
    """Delete all repositories in Gitea, SovereignRepository table, and cache."""

    help = "Supprime tous les dépôts sur Gitea, dans SovereignRepository et vide les caches associés."

    def handle(self, *args, **options):
        client = GiteaClient()
        admin_user = os.environ.get("GITEA_ADMIN_USER", "")
        admin_pass = os.environ.get("GITEA_ADMIN_PASSWORD", "")
        demo_pass = os.environ.get("DEMO_USER_PASSWORD", "DemoCadev2026!")

        auth_candidates = [None]
        if admin_user and admin_pass:
            auth_candidates.append((admin_user, admin_pass))
        auth_candidates.append(("cadev_evaluator", demo_pass))

        repos = client.list_repositories(use_cache=False)
        for repo in repos:
            full_name = repo.get("full_name")
            if not full_name or "/" not in full_name:
                continue
            deleted = False
            last_res = {}
            for auth in auth_candidates:
                kwargs = {"ok_codes": (204, 404)}
                if auth is not None:
                    kwargs["auth"] = auth
                last_res = client._request("delete", f"/repos/{full_name}", **kwargs)
                if last_res.get("success"):
                    deleted = True
                    break
            status = "supprimé" if deleted else last_res.get("status_code", last_res.get("error"))
            self.stdout.write(f"Gitea {full_name} -> {status}")

        deleted_db = SovereignRepository.objects.all().delete()
        cache.delete("bantudevlab_forge_repos_cache")
        cache.delete(GiteaClient.CACHE_KEY_REPOS)
        self.stdout.write(self.style.SUCCESS(f"Base Django nettoyée : {deleted_db}"))
