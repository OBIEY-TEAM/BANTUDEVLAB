# Environnements de Developpement Web Souverains (Equivalent GitHub Codespaces) - T-EXT-602

Ce document decrit l'integration d'environnements de developpement en conteneurs au sein de la forge BantuDevLab, offrant une experience identique a **GitHub Codespaces**.

---

## 1. Acces Direct depuis l'Interface

Chaque page de depot Git dispose desormais d'un bouton direct :
`[ Codespaces / IDE ]`

Ce bouton ouvre l'espace de developpement souverain pre-configure (CodeMirror / VS Code Web) directement connecte au code source du depot.

---

## 2. Integration OAuth2 avec Gitea

L'environnement de developpement est interconnecte a l'instance Gitea locale :
- **Client ID & Secret :** configures via l'application OAuth2 Gitea dans `Parametres de l'application > Applications OAuth2`.
- **Authentification Unique (SSO) :** L'utilisateur se connecte avec son compte `bantu_admin` ou son identite Zero-Trust ZKP.
- **Droits Git :** Le conteneur monte automatiquement les identifiants Git pour autoriser les `git commit` et `git push` sans ressaisie de mot de passe.
