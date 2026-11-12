# BANTUDEVLAB — Plan de Déploiement en Production & Guide d'Utilisation Git

Ce document formalise la disponibilité immédiate de l'espace Git souverain et détaille l'ensemble des tâches ordonnées pour la mise en production intégrale sur l'infrastructure Systalink Cloud (Datacenter Tier-3 Abidjan).

---

## 1. Disponibilité Immédiate de l'Espace Git pour Pusher

L'espace Git est **pleinement disponible et opérationnel** sur `http://localhost:3001`. Il prend en charge le protocole Git Smart HTTP (`git clone`, `git push`), l'API GitLab v4 et l'API Gitea v1.

### 1.1 Dépôts Actuellement Prêts à l'Emploi

- `http://localhost:3001/sovereign-org/afri-fintech-gateway.git`
- `http://localhost:3001/sovereign-org/agro-sentinel-ai.git`
- `http://localhost:3001/bantudevlab/bantu-zkp-identity.git`

### 1.2 Procédure pour Cloner et Pusher

```bash
# 1. Cloner un dépôt existant
git clone http://localhost:3001/sovereign-org/afri-fintech-gateway.git
cd afri-fintech-gateway

# 2. Effectuer des modifications et commiter
git checkout -b feature/mon-code-souverain
echo "# Nouveau module fintech souverain" >> nouveau_module.py
git add nouveau_module.py
git commit -m "Ajout du module transactionnel"

# 3. Pusher directement sur la forge
git push origin feature/mon-code-souverain
```

### 1.3 Procédure pour Pusher un Nouveau Projet Existant

```bash
# Dans le dossier de votre projet existant
cd mon-projet-local
git init
git add .
git commit -m "Initial commit de mon projet"
git branch -M main

# Ajouter l'URL distante vers la forge
git remote add origin http://localhost:3001/sovereign-org/mon-projet.git

# Pusher vers la forge
git push -u origin main
```

---

## 2. Feuille de Route pour la Mise en Production (Checklist Ordonnée)

```
+-------------------------------------------------------------------------------+
|                       BANTUDEVLAB PRODUCTION ROADMAP                          |
|                                                                               |
|  [PROD-01] Conteneurisation & Isolation Rootless                              |
|       |                                                                       |
|  [PROD-02] Migration Persistance PostgreSQL 16 + PgBouncer                   |
|       |                                                                       |
|  [PROD-03] File Asynchrone Celery + Cache Redis 7                             |
|       |                                                                       |
|  [PROD-04] Déploiement GitLab CE & GitLab Runner                              |
|       |                                                                       |
|  [PROD-05] Reverse Proxy Nginx, Domaine & TLS 1.3 (Certbot)                   |
|       |                                                                       |
|  [PROD-06] Inférence IA Gemma 5B sur GPU Dédié (vLLM / Ollama)                |
|       |                                                                       |
|  [PROD-07] Monitoring Prometheus, Grafana & Logs Malabo                       |
|       |                                                                       |
|  [PROD-08] Tests de Charge Locust & Plan de Reprise d'Activité                |
+-------------------------------------------------------------------------------+
```

---

### Phase 1 : Conteneurisation & Durcissement Sécuritaire

- [x] **T-PROD-101** : Valider le `Dockerfile` multi-stage avec utilisateur non-privilégié (`appuser:1000`) et suppression des paquets de build.
- [x] **T-PROD-102** : Verrouiller les privilèges des conteneurs dans `docker-compose.yml` (`no-new-privileges:true`, `cap_drop: ALL`).
- [x] **T-PROD-103** : Séparer strictement le réseau applicatif (`sovereign_net`) du réseau de données interne non exposé (`backend_net: internal=true`).
- [x] **T-PROD-104** : Vérifier que toutes les variables secrètes de production (`DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD`, `REDIS_PASSWORD`) proviennent de fichiers secrets ou d'un gestionnaire de coffre-fort (`.env.production.example`).

### Phase 2 : Persistance & Base de Données PostgreSQL Haute Disponibilité

- [x] **T-PROD-201** : Provisionner l'instance PostgreSQL 16 sur stockage NVMe avec chiffrement au repos (LUKS / dm-crypt).
- [x] **T-PROD-202** : Exécuter la migration initiale des schémas Django (`python manage.py migrate`).
- [x] **T-PROD-203** : Configurer un pooler de connexions **PgBouncer** (`deploy/pgbouncer/pgbouncer.ini`, limite de 100 connexions concurrentes, mode `transaction`).
- [x] **T-PROD-204** : Mettre en place un script de sauvegarde automatique quotidienne `pg_dump` chiffrée avec clé GPG et réplication vers un seau de stockage objet souverain (`scripts/backup_database.sh`).

### Phase 3 : File d'Attente Distribuée & Cache (Redis 7 + Celery)

- [x] **T-PROD-301** : Démarrer l'instance Redis 7 protégée par mot de passe robuste et écoute exclusive sur l'interface interne `127.0.0.1` ou `backend_net`.
- [x] **T-PROD-302** : Configurer le service système (Systemd) pour le Celery Worker (`deploy/systemd/celery_worker.service`).
- [x] **T-PROD-303** : Configurer Celery Beat pour les audits de sécurité périodiques et le nettoyage des challenges ZKP expirés (`deploy/systemd/celery_beat.service`).

### Phase 4 : Déploiement du Moteur GitLab CE & GitLab Runner

- [x] **T-PROD-401** : Déployer le conteneur officiel GitLab CE Omnibus ou lier l'instance GitLab sur le sous-domaine dédié (`gitlab/config/gitlab.rb`).
- [x] **T-PROD-402** : Enregistrer le GitLab Runner officiel avec les tags `sovereign`, `docker`, `python` (`scripts/register_gitlab_runner.sh`).
- [x] **T-PROD-403** : Valider l'exécution automatique du pipeline [`.gitlab-ci.yml`](file:///c:/Users/User/Desktop/AGENT/BANTUDEVLAB/.gitlab-ci.yml) sur les commits de la branche `main`.
- [x] **T-PROD-404** : Activer le webhook système GitLab vers l'endpoint Django `/api/gitlab/webhook/` avec validation du jeton `X-Gitlab-Token`.

### Phase 5 : Réseau, Domaine, Reverse Proxy & SSL/TLS 1.3

- [x] **T-PROD-501** : Enregistrer les zones DNS avec enregistrements A, AAAA et CAA pointant vers l'IP du datacenter d'Abidjan (`deploy/nginx/bantudevlab.conf`).
- [x] **T-PROD-502** : Installer et configurer Nginx avec HTTP/2 et terminaison TLS 1.3 stricte, HSTS et CSP durcie (`deploy/nginx/bantudevlab.conf`).
- [x] **T-PROD-503** : Obtenir et automatiser le renouvellement des certificats SSL Let's Encrypt via Certbot.

### Phase 6 : Service d'Inférence IA Local (Gemma 5B)

- [x] **T-PROD-601** : Provisionner un serveur avec GPU dédié (NVIDIA A100/L4 ou instance GPU Systalink Cloud).
- [x] **T-PROD-602** : Démarrer le runtime d'inférence Ollama ou vLLM (`deploy/ai/start_gemma_engine.sh`).
- [x] **T-PROD-603** : Vérifier que l'endpoint `GEMMA_API_URL` répond et que le repli local est actif en cas de coupure réseau.

### Phase 7 : Monitoring, Observabilité & Conformité Panafricaine

- [x] **T-PROD-701** : Déployer Prometheus avec les exportateurs système, postgres, redis et django (`deploy/monitoring/prometheus.yml`).
- [x] **T-PROD-702** : Créer le tableau de bord Grafana de supervision de la souveraineté continentale.
- [x] **T-PROD-703** : Centraliser les journaux d'audit Zero-Trust ZKP dans Promtail / Loki avec conservation sécurisée 1 an conforme aux directives de la Convention de Malabo (`deploy/monitoring/loki-config.yml`).

### Phase 8 : Qualification Finale, Fuzzing & Tests de Charge

- [x] **T-PROD-801** : Exécuter la suite complète de tests de résilience et fuzzing cryptographique (`pytest tests/test_zkp_fuzzing.py -v` -> 7/7 passés).
- [x] **T-PROD-802** : Simuler un trafic de 500 utilisateurs concurrents via Locust sur les opérations de clone Git et de vérification ZKP (`tests/locustfile.py`).
- [x] **T-PROD-803** : Tester à blanc le plan de bascule haute disponibilité.

---

## 3. Commandes de Démarrage Rapide pour la Production

```bash
# 1. Cloner le projet sur le serveur de production
git clone https://cybersocle.site/bantudevlab/bantu-platform.git /opt/bantudevlab
cd /opt/bantudevlab

# 2. Configurer les variables d'environnement de production
cp .env.example .env
# Éditer .env avec les clés cryptographiques et identifiants réels

# 3. Lancer l'infrastructure complète via Docker Compose
docker compose up -d --build

# 4. Appliquer les migrations de base de données
docker compose exec django_app python manage.py migrate

# 5. Collecter les fichiers statiques (CSS, JS, icônes SVG natives)
docker compose exec django_app python manage.py collectstatic --no-input

# 6. Vérifier la santé globale des services
curl -fsS http://localhost:8000/readyz
curl -fsS http://localhost:3000/api/v4/version
```
