# Partage de Snippets de Code Souverains (Equivalent GitHub Gist) - T-EXT-603

Ce guide presente le service de partage de code, de notes et de fragments souverains, equivalent a **GitHub Gist**, s'appuyant sur **Opengist**.

---

## 1. Fonctionnalites

- Partage de snippets publics, non-repertories (unlisted) ou strictement prives.
- Coloration syntaxique multi-langages, indentation et numerotation des lignes.
- Revision Git de chaque snippet (historique des modifications, diff, clone Git).
- Authentification unifiee avec votre compte Gitea / BantuDevLab via OAuth2.

---

## 2. Deploiement du Service

Pour demarrer le service de snippets :

```bash
docker compose -f deploy/gist/docker-compose.opengist.yml up -d
```

L'interface de partage est alors accessible sur :
[http://localhost:6157/](http://localhost:6157/)
