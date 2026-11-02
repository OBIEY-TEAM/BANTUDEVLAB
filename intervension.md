# Guide d'Intervention et d'Utilisation - Forge Gitea Souveraine

Ce document recapitule l'installation native, la configuration et les actions disponibles pour l'utilisation de Gitea au sein de l'environnement BantuDevLab.

---

## 1. Diagnostic de la Boucle Initiale

### Cause du probleme
Le bouton "Basculer sur Gitea" pointait auparavant vers `http://localhost:3001/gitea`, qui etait intercepte par le serveur forge Python (sur le port 3001) simulant une interface GitLab. Cette route provoquait une redirection circulaire ou une reponse inattendue.

### Solution apportee
1. Le vrai moteur officiel Gitea v1.22.6 (binaire natif Windows 64-bit) a ete telecharge et installe dans `bin/gitea.exe`.
2. Le moteur Gitea a ete configure et demarre de facon autonome sur le port dedie **3002**.
3. Tous les liens "Basculer vers Gitea" (Navbar principale, Drawer mobile, Tableau de bord) ont ete mis a jour pour pointer directement vers `http://localhost:3002/user/login`.
4. Le client Django BantuDevLab (`apps/gitea_client`) est desormais connecte en direct a l'API REST v1 de ce serveur Gitea natif.

---

## 2. Informations d'Acces au Serveur Gitea

- **Interface Web Gitea** : [http://localhost:3002/](http://localhost:3002/)
- **Page de Connexion Directe** : [http://localhost:3002/user/login](http://localhost:3002/user/login)
- **API REST v1** : [http://localhost:3002/api/v1/](http://localhost:3002/api/v1/)
- **Statut du serveur** : Actif (Processus Gitea en cours d'execution)

### Identifiants Administrateur Pre-configures

| Parametre | Valeur |
|---|---|
| **Nom d'utilisateur** | `bantu_admin` |
| **Mot de passe** | `BantuAdmin2026!` |
| **Adresse Email** | `admin@bantudevlab.africa` |
| **Jeton API (Personal Access Token)** | `1749a33d29fee921385f891d05e6cc2aa5fa97f2` |
| **Secret Webhook** | `bantu_dev_webhook_secret_key_2026` |

---

## 3. Actions Requises / Guide Utilisateur

### Action 1 : Connexion a l'interface Gitea
1. Ouvrez votre navigateur sur [http://localhost:3002/user/login](http://localhost:3002/user/login).
2. Saisissez le login `bantu_admin` et le mot de passe `BantuAdmin2026!`.
3. Vous arrivez directement sur votre tableau de bord Gitea avec tous les privileges administrateur.

### Action 2 : Envoyer (Push) votre code source sur Gitea
Un premier depot nomme `bantudevlab` a deja ete initialise sur votre Gitea.
Pour y pousser votre code source local, executez les commandes suivantes dans votre terminal :

```bash
# Ajouter le remote Gitea local
git remote add gitea http://localhost:3002/bantu_admin/bantudevlab.git

# Pousser la branche principale
git push -u gitea main
```

*(Lors de la demande d'authentification Git, utilisez `bantu_admin` et `BantuAdmin2026!`)*

### Action 3 : Creer de nouveaux depots
- Vous pouvez creer autant de depots publics ou prives que vous le souhaitez depuis le bouton "+" en haut a droite de l'interface Gitea.
- Les depots sont automatiquement stockes localement dans :
  `C:\Users\User\Desktop\AGENT\BANTUDEVLAB\forge_data\repos\`

### Action 4 : Verifier les Webhooks vers BantuDevLab
Pour que chaque push ou Pull Request declenche l'analyse de securite, d'audit IA et de souverainete sur BantuDevLab :
1. Dans votre depot Gitea, rendez-vous dans `Parametres` > `Webhooks` > `Ajouter un Webhook` > `Gitea`.
2. URL cible : `http://127.0.0.1:8001/api/forge/webhook/`
3. Secret : `bantu_dev_webhook_secret_key_2026`
4. Cochez : Tous les evenements (Push, Pull Request, Release).
5. Cliquez sur "Ajouter le Webhook".

---

## 4. Architecture des Processus et Ports

| Service | Port Local | URL | Role |
|---|---|---|---|
| **BantuDevLab Portal** | 8001 | http://127.0.0.1:8001/ | Portail central, audit ZKP, gouvernance IA |
| **Gitea Forge Native** | 3002 | http://localhost:3002/user/login | Serveur Git complet officiel (version 1.22.6) |
| **GitLab Sovereign Engine** | 3001 | http://localhost:3001/ | Passerelle de compatibilite GitLab CE |

---

## 5. Commandes de Maintenance Locale

Si vous souhaitez relancer manuellement le serveur Gitea en local :

```powershell
.\bin\gitea.exe web --work-path C:\Users\User\Desktop\AGENT\BANTUDEVLAB\gitea_home --config C:\Users\User\Desktop\AGENT\BANTUDEVLAB\gitea_home\custom\conf\app.ini
```

Le fichier de configuration principal est consultable et modifiable a l'emplacement suivant :
`gitea_home\custom\conf\app.ini`

---

## 6. Option Deploiement Conteneurise Docker (Recommande)

Pour eviter de reinstaller ou reconfigurer les dependances (Python, PostgreSQL, Redis, Gitea) sur une autre machine ou apres redemarrage :

1. **Lancement en 1 commande** :
   ```bash
   docker compose up -d --build
   ```
2. **Ou via les scripts d'automatisation fournis** :
   - Sous Windows : double-cliquez sur `deploy_docker.bat` ou lancez `.\deploy_docker.ps1`
   - Sous Linux / macOS : executez `./deploy_docker.sh`

Tous les conteneurs (Django, Gitea, Forge Engine, Postgres, Redis, Celery) demarrent automatiquement avec les memes ports (`8001`, `3002`, `3001`). Voir `docker-deployment.md` pour le guide complet.
