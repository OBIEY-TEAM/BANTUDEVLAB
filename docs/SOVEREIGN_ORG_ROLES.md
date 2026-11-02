# Specification de la Matrice de Roles et Equipes d'Organisation

Ce document formalise la cartographie des roles d'equipe d'organisation, alignant la gouvernance d'acces de BantuDevLab et Gitea sur le modele GitHub Enterprise.

---

## 1. Niveaux de Roles GitHub et Equivalences Gitea

GitHub definit 5 niveaux hierarchiques de roles sur les depots au sein des organisations :

| Role GitHub | Privileges et Responsabilites | Configuration d'Unite Gitea |
| :--- | :--- | :--- |
| **Read** | Lecture, clonage du code, consultation des issues/PRs | `units: ["repo.code", "repo.issues", "repo.pulls"]` avec acces `read` |
| **Triage** | Gestion des issues, tri des PRs, assignation de labels, sans ecriture de code | `units: ["repo.issues", "repo.pulls"]` en `write` ; `repo.code` en `read` |
| **Write** | Lecture, ecriture, push de branches, creation de releases | `units_map: {"repo.code": "write", "repo.releases": "write"}` |
| **Maintain** | Gestion des parametres de depot, des regles de branches, sans droit de suppression | `units_map: {"repo.code": "admin", "repo.settings": "write"}` (sans permission de suppression de depot) |
| **Admin** | Controle total incluant la suppression du depot et gestion des webhooks | `permission: "admin"` global sur l'equipe |

---

## 2. Badges de Roles Primer

L'interface utilise les badges graphiques conformes aux standards Primer :
- **Triage** (`.gh-role-badge.triage`) : bleu subtil `#0969da`
- **Maintain** (`.gh-role-badge.maintain`) : violet subtil `#8250df`
- **Admin** (`.gh-role-badge.admin`) : rouge securite `#cf222e`

---

## 3. Automatisation d'Equipe via l'API REST

Creation d'une equipe « Triage » pour une organisation :

```bash
curl -X POST "http://localhost:3002/api/v1/orgs/{org}/teams" \
  -H "Authorization: token $FORGE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security-Triage",
    "description": "Equipe de tri et audit de vulnerabilites",
    "permission": "read",
    "can_create_org_repo": false,
    "includes_all_repositories": true,
    "units": ["repo.code", "repo.issues", "repo.pulls"],
    "units_map": {
      "repo.code": "read",
      "repo.issues": "write",
      "repo.pulls": "write"
    }
  }'
```
