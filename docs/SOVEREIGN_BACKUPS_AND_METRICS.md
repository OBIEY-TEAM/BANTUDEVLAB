# Sauvegardes Automatisées et Supervision Prometheus (T-ADM-703)

Ce document décrit la politique de sauvegarde souveraine et la configuration de la supervision Prometheus pour Gitea.

---

## 1. Sauvegardes Quotidiennes Gitea Dump & GPG

Le script `scripts/backup_gitea.sh` (et son alternative portable `scripts/backup_gitea.py`) réalise un instantané complet de la forge :
- Base de données (utilisateurs, tickets, pull requests, revues).
- Dépôts Git et stockage Git LFS.
- Configurations (`app.ini`, clés SSH/GPG).
- Pièces jointes et avatars.

### Exécution manuelle ou via cron :
```bash
# Sauvegarde Shell Linux
./scripts/backup_gitea.sh

# Sauvegarde portable Python
python scripts/backup_gitea.py --backup-dir backups/gitea --retention-days 14
```

Les archives sont chiffrées au repos via GPG avec la clé souveraine de sauvegarde, garantissant la confidentialité des données même en cas de compromission du support de stockage distant.

---

## 2. Métriques Prometheus et Observabilité Grafana

Gitea expose ses métriques de performance et de santé au format standard OpenMetrics / Prometheus.

### Configuration active dans `custom/conf/app.ini` :
```ini
[metrics]
ENABLED = true
TOKEN =
```

Le point de terminaison de scraping est accessible sur :
`http://localhost:3002/metrics`

### Métriques clés supervisées :
- `gitea_uptime_seconds` : Temps de fonctionnement de l'instance.
- `gitea_repos` : Nombre total de dépôts hébergés.
- `gitea_users` : Nombre d'utilisateurs actifs.
- `gitea_issues_total` : Nombre total de tickets et pull requests.
- `gitea_actions_runs_total` : Statut et débit des pipelines CI/CD Gitea Actions.
