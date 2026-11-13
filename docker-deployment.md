# Deploiement Conteneurise Docker - BANTUDEVLAB

Ce guide explique comment deployer l'integralite de la plateforme BantuDevLab et de sa forge Git souveraine dans un environnement Docker conteneurise, cle-en-main, sans aucune reinstallation manuelle de dependances (Python, PostgreSQL, Redis, Gitea).

---

## 1. Prerequis Uniques

- **Docker Desktop** (version 24+ ou superieure)
- **Docker Compose** (v2 ou v5 integre a Docker CLI)

*Aucune installation locale de Python, Git, SQLite ou Gitea n'est requise sur la machine hote.*

---

## 2. Deploiement en 1 Clic / 1 Commande

### Option A : Ligne de commande universelle
A la racine du projet, lancez :

```bash
docker compose up -d --build
```

### Option B : Scripts d'automatisation fournis
- **Sous Windows (Invite de commandes)** : double-cliquez sur `deploy_docker.bat`
- **Sous Windows (PowerShell)** : executez `.\deploy_docker.ps1`
- **Sous Linux / macOS** : executez `./deploy_docker.sh`

---

## 3. Cartographie des Services et Ports

Tous les conteneurs sont relies sur un reseau interne securise `sovereign_net` et exposent directement les memes ports d'acces que votre environnement local :

| Conteneur | Service | Port Hote | URL d'Acces | Role |
|---|---|---|---|---|
| `bantudevlab_core` | Portail Django Web | `8001` | [http://localhost:8001/](http://localhost:8001/) | Portail central, audit ZKP, IA souveraine |
| `bantudevlab_gitea` | Gitea Forge Officielle | `3002` | [http://localhost:3002/user/login](http://localhost:3002/user/login) | Serveur Git complet officiel v1.22 |
| `bantudevlab_forge` | Moteur Forge Souverain | `3001` | [http://localhost:3001/](http://localhost:3001/) | Passerelle Git HTTP, Smart HTTP & API CE |
| `bantudevlab_postgres` | Base relationnelle | `5432` | Reseau interne | Stockage PostgreSQL 16 Alpine |
| `bantudevlab_redis` | Cache & Broker | `6379` | Reseau interne | Broker Redis 7 Alpine |
| `bantudevlab_celery` | File de taches | - | Reseau interne | Worker asynchrone Celery |
| `bantudevlab_celery_beat` | Ordonnanceur periodique | - | Reseau interne | Celery Beat periodic scheduler |
| `bantudevlab_ollama` | Moteur IA locale | - | Reseau interne | Inférence Gemma 2 2B (port 11434) |
| `bantudevlab_renovate` | Bot dependances | - | Reseau interne | Analyse continue des dependances |
| `bantudevlab_act_runner` | Runner CI/CD | - | Reseau interne | Execution locale des actions CI |
| `bantudevlab_gitea_init` | Init automatique | - | One-shot | Creation automatique du compte `bantu_admin` |

---

## 3.bis Deploiement Industriel Haute Disponibilite (Production)

Pour deployer l'architecture durcie 3 tiers avec GitLab CE Omnibus, PgBouncer et terminaison TLS 1.3 Nginx :

```bash
docker compose -f docker-compose.production.yml --env-file .env.production up -d --build
```

### Mise a jour d'un VPS deja deploye
Pour mettre a jour le VPS sans ecraser `.env.production` ni les volumes de donnees :

```bash
chmod +x deploy/vps_update.sh
./deploy/vps_update.sh docker-cadev26
```

### Cartographie de Production
- **Nginx Reverse Proxy** : Ports `8080` (HTTP -> HTTPS) et `8443` (TLS 1.3 durci, certbot LetsEncrypt)
- **GitLab CE Omnibus** : Service interne `gitlab:80` et SSH sur port `2222`
- **Django Core** : Service interne `django_app:8000` avec Uvicorn/Gunicorn rootless en lecture seule
- **PgBouncer** : Port interne `6432` en mode transactionnel
- **PostgreSQL 16 Alpine** : Port interne `5432` sur `backend_net` isole
- **Redis 7 Alpine** : Port interne `6379` avec authentification obligatoire et persistance AOF
- **Celery Worker & Beat** : Traitement asynchrone et ordonnancement de production
- **Ollama AI** : Inférence souveraine Gemma 2 2B sur réseau interne isolé

---

## 4. Provisionnement des Comptes & Securite (CADEV 2026)

Conformement aux exigences de securite CADEV 2026, aucun mot de passe d'administration n'est fixe en dur :
- **Compte Administrateur :** Defini lors du deploiement via les variables d'environnement (`BANTU_ADMIN_USER`, `BANTU_ADMIN_PASSWORD`, `GITEA_ADMIN_USER`, `GITEA_ADMIN_PASSWORD`).
- **Compte de Demonstration CADEV :** Compte `cadev_evaluator` (authentification ZKP Zero-Trust sans mot de passe, non-privilegie).
- **Mots de passe des services (PostgreSQL / Valkey) :** Configures dans `.env.production` isole (voir `CADEV26/ROTATION_SECRETS.md`).

---

## 5. Commandes Utiles au Quotidien

### Verifier l'etat des conteneurs
```bash
docker compose ps
```

### Consulter les journaux en direct
```bash
# Tous les services
docker compose logs -f

# Un service specifique
docker compose logs -f django_app
docker compose logs -f gitea
docker compose logs -f forge_engine
```

### Arreter la composition
```bash
docker compose stop
```

### Relancer les conteneurs deja construits (sans recompiler)
```bash
docker compose start
```

### Tout supprimer (conteneurs et reseaux, en conservant les volumes de donnees)
```bash
docker compose down
```

### Reinitialiser completement (y compris les donnees persistees)
```bash
docker compose down -v
```
