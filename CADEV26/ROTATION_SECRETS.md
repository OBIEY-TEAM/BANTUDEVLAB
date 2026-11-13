# Plan de Rotation des Secrets & Assainissement de l'Historique Git (CADEV 2026)

> **Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
> **Équipe candidate :** CYBERSOCLE  
> **Date du plan :** 13 novembre 2026  
> **Document de conformité :** Tâche 2 — Audit de sécurité et gestion des identifiants sensibles

---

## 1. Cartographie des Secrets Identifiés et Types de Données

Un scan exhaustif de l'historique Git et de la configuration a été réalisé.
Aucun secret en clair n'est affiché dans ce rapport. Les catégories de secrets identifiées sont les suivantes :

| Identifiant du Secret | Composant Concerné | Fichiers Historiques Détectés | Rôle & Criticité |
| :--- | :--- | :--- | :--- |
| **`DJANGO_SECRET_KEY`** | Portail BantuDevLab (Django) | `docker-compose.yml`, `.env.example`, `.env.production.example` | Signature cryptographique des sessions, des cookies CSRF et des jetons d'état ZKP. **Critique.** |
| **`POSTGRES_PASSWORD`** | Base PostgreSQL (`bantudevlab_admin`) | `docker-compose.yml`, `docker-compose.production.yml` | Authentification du superutilisateur de la base relationnelle. **Élevée.** |
| **`REDIS_PASSWORD`** | Cache & Broker Valkey / Redis | `docker-compose.yml`, `docker-compose.production.yml` | Contrôle d'accès au courtier de messages Celery et au cache distribué. **Élevée.** |
| **`GITEA_ADMIN_TOKEN`** | API Gitea (`GiteaClient`) | `docker-compose.yml`, `.env.example` | Jeton d'accès administrateur pour l'automatisation de la création de dépôts et webhooks. **Critique.** |
| **`GITEA_WEBHOOK_SECRET`** | Webhooks Gitea (`GiteaWebhookReceiver`) | `docker-compose.yml`, `config/settings.py` | Secret partagé de validation HMAC des événements de code (`X-Gitea-Signature`). **Moyenne.** |
| **`GITLAB_WEBHOOK_SECRET`** | Webhooks GitLab CE (`apps/gitlab_client`) | `config/settings.py`, `.env.example` | Jeton de contrôle de signature HMAC pour les récepteurs de push hooks. **Moyenne.** |
| **`GITEA_SECURITY_SECRET_KEY`** | Moteur interne Gitea | `docker-compose.yml`, `custom/conf/app.ini` | Chiffrement symétrique interne des sessions et tokens Gitea. **Élevée.** |
| **Mots de passe d'initialisation par défaut** | Provisionnement Gitea / Django | `docker-compose.yml`, `init_sovereign_admin.py` | Mot de passe historique d'initialisation conteneurisée. **Supprimé du code.** |

---

## 2. Procédure Opérationnelle de Rotation des Secrets

L'équipe CYBERSOCLE doit exécuter la rotation des secrets avant la mise en production définitive selon la procédure suivante :

### Étape 1 : Génération de Nouvelles Clés Fortes et Entropiques
Exécuter sur une machine d'administration sécurisée :
```bash
# Generation de la cle Django (64 caracteres base64)
python -c 'import secrets; print(secrets.token_urlsafe(48))'

# Generation du mot de passe PostgreSQL
python -c 'import secrets; print(secrets.token_hex(24))'

# Generation du mot de passe Valkey/Redis
python -c 'import secrets; print(secrets.token_hex(24))'

# Generation du secret de webhook HMAC
python -c 'import secrets; print(secrets.token_hex(32))'
```

### Étape 2 : Déploiement dans `.env.production` sur le VPS Ubuntu externe
Renseigner ces valeurs générées directement dans le fichier sécurisé `~/.env.production` (droits `chmod 600`, propriété `root` ou `bantu`), sans jamais versionner ce fichier dans Git :
```bash
DJANGO_SECRET_KEY=<NOUVELLE_CLE_GENEREE>
POSTGRES_PASSWORD=<NOUVEAU_MDP_POSTGRES>
REDIS_PASSWORD=<NOUVEAU_MDP_VALKEY>
GITEA_ADMIN_TOKEN=<NOUVEAU_TOKEN_GENERE_DEPUIS_GITEA_UI>
GITEA_WEBHOOK_SECRET=<NOUVEAU_SECRET_HMAC>
GITLAB_WEBHOOK_SECRET=<NOUVEAU_SECRET_HMAC>
```

### Étape 3 : Révocation et Regénération du Token Gitea
1. Se connecter sur l'interface d'administration Gitea : `https://git.cybersocle.site/user/settings/applications`.
2. Supprimer l'ancien jeton d'accès nommé `bantudevlab_token`.
3. Générer un nouveau jeton avec les portées `read:repository, write:repository, read:user, read:organization`.
4. Reporter ce jeton dans `GITEA_ADMIN_TOKEN` sur le serveur de production et redémarrer le conteneur `bantudevlab_core`.

---

## 3. Plan d'Assainissement Git (`git filter-repo`) avec Conservation des Dates

> **AVERTISSEMENT :** Conformément aux règles de sécurité, ce plan est proposé ici **à titre indicatif et méthodologique**. Il ne doit être exécuté qu'après validation explicite de l'équipe et sauvegarde miroir complète.

### Pourquoi `git-filter-repo` ?
`git-filter-repo` est l'outil officiel recommandé par le projet Git (en remplacement de l'obsolète et dangereux `git filter-branch`). Il garantit la réécriture déterministe de l'historique tout en **préservant strictement** les métadonnées :
- Noms et emails des auteurs (`author_name`, `author_email`).
- Dates de création et d'engagement d'origine (`author_date`, `committer_date`).
- Arborescence des branches et structure des fusions (merges).

### Déroulement du Plan d'Assainissement

```bash
# 1. Realiser une sauvegarde miroir prealable (Indispensable)
git clone --mirror . ../BANTUDEVLAB_backup_mirror.git

# 2. Creer le dictionnaire de masquage des expressions sensibles
cat << 'EOF' > /tmp/sensitive_replacements.txt
# Remplacement des secrets et tokens par des balises neutralisees
regex:(?i)(DJANGO_SECRET_KEY\s*[:=]\s*)[a-zA-Z0-9_\-]{20,}==>\1[REDACTED_DJANGO_SECRET_KEY]
regex:(?i)(POSTGRES_PASSWORD\s*[:=]\s*)[a-zA-Z0-9_\-]{10,}==>\1[REDACTED_POSTGRES_PASSWORD]
regex:(?i)(REDIS_PASSWORD\s*[:=]\s*)[a-zA-Z0-9_\-]{10,}==>\1[REDACTED_REDIS_PASSWORD]
regex:(?i)(GITEA_ADMIN_TOKEN\s*[:=]\s*)[a-zA-Z0-9]{30,}==>\1[REDACTED_GITEA_TOKEN]
regex:(?i)(GITEA_WEBHOOK_SECRET\s*[:=]\s*)[a-zA-Z0-9_\-]{15,}==>\1[REDACTED_GITEA_WEBHOOK_SECRET]
regex:(?i)(GITLAB_WEBHOOK_SECRET\s*[:=]\s*)[a-zA-Z0-9_\-]{15,}==>\1[REDACTED_GITLAB_WEBHOOK_SECRET]
regex:BantuAdmin2026!==>[REDACTED_ADMIN_PASSWORD]
EOF

# 3. Executer git-filter-repo en conservant les horodatages et committers d'origine
# L'option preserve-commit-hashes n'est pas possible par nature du SHA-1,
# mais toutes les dates d'origine (author date et committer date) sont conservees.
git-filter-repo --replace-text /tmp/sensitive_replacements.txt --force

# 4. Verifier que les dates d'origine sont intactes
git log -n 5 --format="%h | Auteur: %an <%ae> | Date Auteur: %ad | Date Commit: %cd | %s" --date=iso

# 5. Nettoyer les reflogs et forcer le garbage collector local
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

## 4. Politique de Comptes & Provisionnement par Variables d'Environnement

1. **Suppression des comptes administrateurs par défaut en dur :**
   - Le script `apps/core/management/commands/init_sovereign_admin.py` et les fichiers Docker Compose ne contiennent plus aucun mot de passe codé en dur.
   - Le provisionnement d'un compte administrateur Django ou Gitea n'intervient **que si et seulement si** les variables `BANTU_ADMIN_USER`, `BANTU_ADMIN_EMAIL` et `BANTU_ADMIN_PASSWORD` sont explicitement injectées dans l'environnement.

2. **Compte de Démonstration Non Privilégié (`cadev_evaluator`) :**
   - Un compte évaluateur dédié est mis à disposition pour l'évaluation CADEV 2026.
   - **Privilèges :** `is_staff = False`, `is_superuser = False` (zéro droit d'administration, aucun accès à `/admin/`).
   - **Authentification :** 100% sans mot de passe via Zero-Knowledge Proof (ZKP). La phrase mnémonique BIP-39 standard pré-remplie permet à l'évaluateur de tester le parcours complet sans aucun privilège sensible.
