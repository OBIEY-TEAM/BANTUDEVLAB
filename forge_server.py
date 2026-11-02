"""
Moteur de Forge Git Souveraine BANTUDEVLAB (Gitea / GitLab CE Engine).
Fournit :
1. Interface Web moderne pour explorer les depots, commits, branches et PRs.
2. API REST v1 compatible Gitea / GitLab CE (/api/v1/*).
3. Protocole Git Smart HTTP pour git clone / git push via git http-backend.
4. Emetteur de Webhooks cryptographiques signes HMAC-SHA256 vers BantuDevLab Core.
"""

import hashlib
import hmac
import json
import os
import re
import subprocess
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPOS_DIR = BASE_DIR / "forge_data" / "repos"
BANTU_CORE_URL = os.environ.get("BANTU_CORE_URL", "http://127.0.0.1:8001")
WEBHOOK_SECRET = os.environ.get("GITEA_WEBHOOK_SECRET", "bantu_dev_webhook_secret_key_2026")
PORT = int(os.environ.get("FORGE_PORT", 3001))

REPO_METADATA = {
    "sovereign-org/afri-fintech-gateway": {
        "description": "Passerelle panafricaine de paiement mobile & interoperabilite souveraine",
        "stars": 42,
        "forks": 12,
        "sovereignty_level": "Tier-1 Continental",
    },
    "sovereign-org/agro-sentinel-ai": {
        "description": "Modeles de vision embarquee pour la surveillance des recoltes saheliennes",
        "stars": 89,
        "forks": 27,
        "sovereignty_level": "Tier-1 Continental",
    },
    "bantudevlab/bantu-zkp-identity": {
        "description": "Bibliotheque cryptographique Zero-Knowledge Proof pour l'Afrique de l'Ouest",
        "stars": 154,
        "forks": 34,
        "sovereignty_level": "Tier-1 Continental",
    },
}

PULL_REQUESTS_STORE = [
    {
        "id": 1,
        "number": 1,
        "repo": "sovereign-org/afri-fintech-gateway",
        "title": "Integration du protocole Schnorr NIZKP",
        "state": "open",
        "head": {"label": "feat/schnorr-zkp", "ref": "feat/schnorr-zkp"},
        "base": {"label": "main", "ref": "main"},
        "user": {"username": "kouame-dev"},
        "created_at": "2026-05-10T10:00:00Z",
        "updated_at": "2026-05-10T12:00:00Z",
    }
]


class SovereignForgeHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Gitea-Signature")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_content, status=200):
        body = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Gitea-Signature")
        self.end_headers()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip("/")
        urllib.parse.parse_qs(url.query)

        # 1. API: /api/v1/version & /api/v4/version (GitLab CE)
        if path == "/api/v4/version":
            return self._send_json({
                "version": "16.11.0-gitlab-sovereign",
                "revision": "7bf3e9a4f21",
                "status": "ONLINE",
                "engine": "GitLab CE Panafricain",
            })

        if path == "/api/v4/user":
            return self._send_json({
                "id": 1,
                "username": "sovereign_admin",
                "name": "Administrateur Souverain",
                "state": "active",
            })

        if path == "/api/v4/projects":
            return self._send_json(self._get_gitlab_projects_list())

        m_gl_proj = re.match(r"^/api/v4/projects/(\d+)$", path)
        if m_gl_proj:
            pid = int(m_gl_proj.group(1))
            for p in self._get_gitlab_projects_list():
                if p["id"] == pid:
                    return self._send_json(p)
            return self._send_json({"message": "404 Project Not Found"}, status=404)

        if path == "/api/v1/version":
            return self._send_json({
                "version": "1.23.0-sovereign-panafrican",
                "status": "ONLINE",
                "engine": "Gitea / GitLab CE Hybrid",
                "cloud_provider": "Systalink Cloud Sovereign Cluster",
                "location": "Abidjan Tier-3 Datacenter",
            })

        # 2. API: /api/v1/repos/search
        if path == "/api/v1/repos/search":
            repos = self._get_repos_list()
            return self._send_json({"ok": True, "data": repos})

        # 3. API: /api/v1/repos/{owner}/{repo}/commits
        m_commits = re.match(r"^/api/v1/repos/([^/]+)/([^/]+)/commits$", path)
        if m_commits:
            owner, repo = m_commits.groups()
            commits = self._get_repo_commits(owner, repo)
            return self._send_json(commits)

        # 4. API: /api/v1/repos/{owner}/{repo}/branches
        m_branches = re.match(r"^/api/v1/repos/([^/]+)/([^/]+)/branches$", path)
        if m_branches:
            owner, repo = m_branches.groups()
            branches = self._get_repo_branches(owner, repo)
            return self._send_json(branches)

        # 5. API: /api/v1/repos/{owner}/{repo}/pulls
        m_pulls = re.match(r"^/api/v1/repos/([^/]+)/([^/]+)/pulls$", path)
        if m_pulls:
            owner, repo = m_pulls.groups()
            pulls = [p for p in PULL_REQUESTS_STORE if p["repo"] == f"{owner}/{repo}"]
            return self._send_json(pulls)

        # 6. Smart Git HTTP backend
        if ".git" in path:
            return self._handle_git_http(url)

        # 7. UI: Web Pages
        if path in ("", "/", "/explore"):
            return self._render_home_ui()

        m_repo_ui = re.match(r"^/([^/]+)/([^/]+)$", path)
        if m_repo_ui:
            owner, repo = m_repo_ui.groups()
            return self._render_repo_ui(owner, repo)

        return self._send_html("<h1>404 - Page Introuvable</h1>", status=404)

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip("/")
        content_len = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_len) if content_len > 0 else b""

        # 1. API: /api/v1/user/repos
        if path == "/api/v1/user/repos":
            try:
                data = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                data = {}
            name = data.get("name", "nouveau-depot")
            desc = data.get("description", "")
            private = bool(data.get("private", False))

            repo_full = self._create_repo("sovereign-org", name, desc, private)
            return self._send_json(repo_full, status=201)

        # 2. Trigger webhook towards BantuDevLab Core (Gitea / GitLab)
        if path in ("/trigger-webhook", "/trigger-gitlab-webhook"):
            try:
                data = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
            except Exception:
                data = {}
            if "gitlab" in path or data.get("forge") == "gitlab":
                result = self._dispatch_gitlab_webhook(data)
            else:
                result = self._dispatch_webhook(data)
            return self._send_json(result)

        # 3. Smart Git HTTP backend POST
        if ".git" in path:
            return self._handle_git_http_post(url, body_bytes)

        return self._send_json({"error": "Endpoint inconnu"}, status=404)

    def do_PATCH(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip("/")
        content_len = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_len) if content_len > 0 else b""
        try:
            data = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            data = {}

        m_pr = re.match(r"^/api/v1/repos/([^/]+)/([^/]+)/pulls/(\d+)$", path)
        if m_pr:
            owner, repo, pr_id = m_pr.groups()
            for p in PULL_REQUESTS_STORE:
                if p["repo"] == f"{owner}/{repo}" and str(p["number"]) == pr_id:
                    if "state" in data:
                        p["state"] = data["state"]
                    if "title" in data:
                        p["title"] = data["title"]
                    return self._send_json(p)
            return self._send_json({"error": "PR introuvable"}, status=404)

        return self._send_json({"error": "Endpoint inconnu"}, status=404)

    # ---------------- Git HTTP backend ----------------
    def _handle_git_http(self, url):
        # Service info/refs
        git_dir, service = self._resolve_git_repo(url.path)
        if not git_dir or not git_dir.exists():
            return self._send_html("Dépôt Git introuvable", status=404)

        query = urllib.parse.parse_qs(url.query)
        svc = query.get("service", [None])[0]
        if svc in ("git-upload-pack", "git-receive-pack"):
            cmd = ["git", svc.replace("git-", ""), "--stateless-rpc", "--advertise-refs", str(git_dir)]
            res = subprocess.run(cmd, capture_output=True)
            self.send_response(200)
            self.send_header("Content-Type", f"application/x-{svc}-advertisement")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()

            # Smart HTTP header packet
            packet = f"# service={svc}\n"
            hex_len = f"{len(packet) + 4:04x}"
            self.wfile.write(f"{hex_len}{packet}0000".encode("utf-8"))
            self.wfile.write(res.stdout)
            return

        self._send_html("Git HTTP info", status=200)

    def _handle_git_http_post(self, url, body_bytes):
        git_dir, service = self._resolve_git_repo(url.path)
        if not git_dir or not git_dir.exists():
            return self._send_html("Dépôt Git introuvable", status=404)

        svc = "upload-pack" if "upload-pack" in url.path else "receive-pack"
        cmd = ["git", svc, "--stateless-rpc", str(git_dir)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate(input=body_bytes)

        self.send_response(200)
        self.send_header("Content-Type", f"application/x-git-{svc}-result")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(out)

    def _resolve_git_repo(self, path):
        m = re.search(r"/([^/]+)/([^/]+)\.git", path)
        if m:
            owner, name = m.groups()
            return REPOS_DIR / owner / f"{name}.git", None
        return None, None

    # ---------------- Helpers Git ----------------
    def _get_repos_list(self):
        items = []
        if REPOS_DIR.exists():
            for owner_dir in REPOS_DIR.iterdir():
                if owner_dir.is_dir():
                    for repo_dir in owner_dir.glob("*.git"):
                        name = repo_dir.stem
                        full = f"{owner_dir.name}/{name}"
                        meta = REPO_METADATA.get(full, {
                            "description": "Dépôt souverain BANTUDEVLAB",
                            "stars": 10,
                            "forks": 2,
                            "sovereignty_level": "Tier-1 Continental",
                        })
                        items.append({
                            "id": abs(hash(full)) % 10000,
                            "name": name,
                            "full_name": full,
                            "description": meta["description"],
                            "private": False,
                            "stars_count": meta["stars"],
                            "forks_count": meta["forks"],
                            "open_issues_count": 1,
                            "owner": {"username": owner_dir.name},
                            "clone_url": f"http://localhost:{PORT}/{full}.git",
                            "html_url": f"http://localhost:{PORT}/{full}",
                            "default_branch": "main",
                            "sovereignty_level": meta["sovereignty_level"],
                        })
        return items

    def _get_gitlab_projects_list(self):
        repos = self._get_repos_list()
        projects = []
        for r in repos:
            owner, name = r["full_name"].split("/", 1)
            projects.append({
                "id": r["id"],
                "name": name,
                "path": name,
                "path_with_namespace": r["full_name"],
                "description": r["description"],
                "star_count": r["stars_count"],
                "forks_count": r["forks_count"],
                "web_url": f"http://localhost:{PORT}/{r['full_name']}",
                "http_url_to_repo": f"http://localhost:{PORT}/{r['full_name']}.git",
                "default_branch": "main",
                "visibility": "public",
                "created_at": "2026-01-01T00:00:00.000Z",
                "last_activity_at": "2026-11-02T04:00:00.000Z",
                "namespace": {"id": 1, "name": owner, "path": owner, "kind": "group"},
            })
        return projects

    def _get_repo_commits(self, owner, repo):
        repo_dir = REPOS_DIR / owner / f"{repo}.git"
        if not repo_dir.exists():
            return []
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "log", "-n", "10", "--pretty=format:%H||%an||%ad||%s", "--date=iso"],
            capture_output=True,
            text=True,
        )
        commits = []
        for line in res.stdout.splitlines():
            parts = line.split("||")
            if len(parts) == 4:
                commits.append({
                    "sha": parts[0],
                    "commit": {
                        "author": {"name": parts[1], "date": parts[2]},
                        "message": parts[3],
                    },
                })
        return commits

    def _get_repo_branches(self, owner, repo):
        repo_dir = REPOS_DIR / owner / f"{repo}.git"
        if not repo_dir.exists():
            return [{"name": "main", "commit": {"id": "000000"}}]
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "branch", "--format=%(refname:short)"],
            capture_output=True,
            text=True,
        )
        branches = [{"name": b.strip(), "commit": {"id": "HEAD"}} for b in res.stdout.splitlines() if b.strip()]
        return branches or [{"name": "main", "commit": {"id": "HEAD"}}]

    def _create_repo(self, owner, name, desc="", private=False):
        repo_dir = REPOS_DIR / owner / f"{name}.git"
        repo_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "--bare", str(repo_dir)], check=True, capture_output=True)
        REPO_METADATA[f"{owner}/{name}"] = {
            "description": desc or "Dépôt souverain BANTUDEVLAB",
            "stars": 1,
            "forks": 0,
            "sovereignty_level": "Tier-1 Continental",
        }
        return {
            "id": abs(hash(f"{owner}/{name}")) % 10000,
            "name": name,
            "full_name": f"{owner}/{name}",
            "description": desc,
            "private": private,
            "html_url": f"http://localhost:{PORT}/{owner}/{name}",
            "clone_url": f"http://localhost:{PORT}/{owner}/{name}.git",
        }

    def _dispatch_webhook(self, payload):
        import urllib.request
        webhook_url = f"{BANTU_CORE_URL}/api/forge/webhook/"
        body = json.dumps(payload).encode("utf-8")
        sig = hmac.new(WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
        req = urllib.request.Request(webhook_url, data=body, headers={
            "Content-Type": "application/json",
            "X-Gitea-Signature": sig,
            "X-Gitea-Event": "push",
        })
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"success": True, "bantu_response": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _dispatch_gitlab_webhook(self, payload):
        import urllib.request
        webhook_url = f"{BANTU_CORE_URL}/api/gitlab/webhook/"
        body = json.dumps(payload).encode("utf-8")
        token = os.environ.get("GITLAB_WEBHOOK_SECRET", "bantu_gitlab_webhook_secret_2026")
        req = urllib.request.Request(webhook_url, data=body, headers={
            "Content-Type": "application/json",
            "X-Gitlab-Token": token,
            "X-Gitlab-Event": "Push Hook",
        })
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"success": True, "gitlab_response": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ---------------- UI Templates ----------------
    def _render_home_ui(self):
        repos = self._get_repos_list()
        repos_html = "".join(f"""
        <div class="repo-card">
            <div class="repo-header">
                <a href="/{r['full_name']}" class="repo-title">{r['full_name']}</a>
                <span class="badge">Tier-1 Souverain</span>
            </div>
            <p class="repo-desc">{r['description']}</p>
            <div class="repo-footer">
                <span>Stars: {r['stars_count']}</span>
                <span>Forks: {r['forks_count']}</span>
                <code class="clone-snippet">git clone {r['clone_url']}</code>
            </div>
        </div>
        """ for r in repos)

        html = f"""<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <title>BANTUDEVLAB — Moteur Forge Git Souveraine</title>
    <style>
        :root {{
            --gold: #f59e0b;
            --emerald: #10b981;
            --bg: #0b0f19;
            --surface: #111827;
            --border: #1f2937;
            --text: #f9fafb;
            --muted: #9ca3af;
        }}
        body {{
            margin: 0; font-family: system-ui, -apple-system, sans-serif;
            background: var(--bg); color: var(--text); line-height: 1.6;
        }}
        .navbar {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 1rem 2rem; background: var(--surface); border-bottom: 2px solid var(--gold);
        }}
        .brand {{ display: flex; align-items: center; gap: 0.6rem; font-weight: 800; font-size: 1.25rem; color: #fff; text-decoration: none; }}
        .badge {{ background: var(--gold); color: #000; font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: bold; }}
        .container {{ max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
        .btn {{
            display: inline-block; padding: 0.5rem 1rem; border-radius: 6px;
            font-weight: 600; text-decoration: none; cursor: pointer; border: none;
        }}
        .btn-gold {{ background: var(--gold); color: #000; }}
        .btn-outline {{ background: transparent; border: 1px solid var(--border); color: var(--text); }}
        .btn-outline:hover {{ border-color: var(--gold); color: var(--gold); }}
        .hero {{
            background: radial-gradient(circle at 50% 10%, rgba(245, 158, 11, 0.15), transparent 70%);
            padding: 2.5rem; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 2rem; text-align: center;
        }}
        .repo-card {{
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;
        }}
        .repo-header {{ display: flex; justify-content: space-between; align-items: center; }}
        .repo-title {{ font-size: 1.15rem; font-weight: 700; color: var(--gold); text-decoration: none; }}
        .repo-desc {{ color: var(--muted); margin: 0.5rem 0; font-size: 0.95rem; }}
        .repo-footer {{ display: flex; gap: 1.5rem; align-items: center; font-size: 0.85rem; color: var(--muted); flex-wrap: wrap; }}
        .clone-snippet {{ background: #000; padding: 0.25rem 0.6rem; border-radius: 4px; color: var(--emerald); font-family: monospace; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="/" class="brand">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" style="vertical-align:middle;margin-right:6px;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
            <span>BANTUDEVLAB FORGE GIT</span>
            <span class="badge">SYSTALINK CLOUD</span>
        </a>
        <div style="display: flex; gap: 1rem; align-items: center;">
            <a href="{BANTU_CORE_URL}/" class="btn btn-outline">&larr; Retour au Portail BantuDevLab</a>
            <a href="{BANTU_CORE_URL}/dashboard/" class="btn btn-gold">Tableau de Bord & Audit</a>
        </div>
    </nav>

    <div class="container">
        <div class="hero">
            <h1 style="margin-top: 0;">Moteur Git Panafricain & Dépôts Souverains</h1>
            <p style="color: var(--muted); max-width: 700px; margin: 0 auto 1.5rem;">
                Forge logicielle distribuée connectée en temps réel au portail BantuDevLab.
                Protocoles Git Smart HTTP, Zero-Trust ZKP et Webhooks signés HMAC.
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center;">
                <button class="btn btn-gold" onclick="triggerTestWebhook()">Simuler Push Webhook vers BantuDevLab</button>
            </div>
            <div id="webhookResult" style="margin-top: 1rem; font-family: monospace; font-size: 0.85rem; color: var(--emerald);"></div>
        </div>

        <h2>Dépôts Hébergés sur l'Infrastructure Souveraine</h2>
        {repos_html}
    </div>

    <script>
    function triggerTestWebhook() {{
        const out = document.getElementById('webhookResult');
        out.textContent = "Envoi du webhook HMAC en cours...";
        fetch('/trigger-webhook', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                repository: {{ name: 'afri-fintech-gateway' }},
                pusher: {{ username: 'kouame_dev' }},
                ref: 'refs/heads/main'
            }})
        }})
        .then(r => r.json())
        .then(data => {{
            out.textContent = "Webhook acquitté par BantuDevLab Core : " + JSON.stringify(data.bantu_response || data);
        }})
        .catch(err => {{
            out.textContent = "Erreur webhook : " + err.message;
        }});
    }}
    </script>
</body>
</html>"""
        return self._send_html(html)

    def _render_repo_ui(self, owner, repo):
        repo_dir = REPOS_DIR / owner / f"{repo}.git"
        if not repo_dir.exists():
            return self._send_html("Dépôt introuvable", status=404)

        commits = self._get_repo_commits(owner, repo)
        self._get_repo_branches(owner, repo)
        commits_html = "".join(f"""
        <li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border); font-size: 0.9rem;">
            <strong>{c['commit']['message']}</strong>
            <div style="color: var(--muted); font-size: 0.8rem;">
                Par {c['commit']['author']['name']} • SHA: <code>{c['sha'][:8]}</code> • {c['commit']['author']['date']}
            </div>
        </li>
        """ for c in commits)

        html = f"""<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <title>{owner}/{repo} — BantuDevLab Forge</title>
    <style>
        :root {{ --gold: #f59e0b; --emerald: #10b981; --bg: #0b0f19; --surface: #111827; --border: #1f2937; --text: #f9fafb; --muted: #9ca3af; }}
        body {{ margin: 0; font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .navbar {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: var(--surface); border-bottom: 2px solid var(--gold); }}
        .container {{ max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }}
        .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }}
        .clone-box {{ background: #000; padding: 0.75rem; border-radius: 6px; font-family: monospace; color: var(--emerald); display: flex; justify-content: space-between; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="/" style="color: #fff; font-weight: 800; text-decoration: none;">BANTUDEVLAB FORGE GIT</a>
        <a href="{BANTU_CORE_URL}/dashboard/" style="color: var(--gold); text-decoration: none; font-weight: bold;">&larr; Tableau de Bord BantuDevLab</a>
    </nav>
    <div class="container">
        <h1>{owner}/{repo}</h1>
        <div class="card">
            <h3>Cloner le dépôt sur votre poste</h3>
            <div class="clone-box">
                <span>git clone http://localhost:{PORT}/{owner}/{repo}.git</span>
            </div>
            <p style="font-size: 0.85rem; color: var(--muted); margin-top: 0.5rem;">
                Pour pousser avec ZKP, utilisez votre token souverain généré depuis <a href="{BANTU_CORE_URL}/api/zkp/login-ui/" style="color: var(--gold);">l'assistant Zero-Trust</a>.
            </p>
        </div>
        <div class="card">
            <h3>Historique Récent des Commits ({len(commits)})</h3>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {commits_html}
            </ul>
        </div>
    </div>
</body>
</html>"""
        return self._send_html(html)


def run_server():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), SovereignForgeHandler)
    server.daemon_threads = True
    print(f"BantuDevLab Sovereign Git Forge Engine démarré sur http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
