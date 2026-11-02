# Guide des Rulesets de Protection de Branches Souverains (GitHub / Gitea)

Ce document formalise les regles de protection de branches avancees, reproduisant l'architecture des Rulesets de GitHub Enterprise sur l'infrastructure forge souveraine Gitea.

---

## 1. Principes et Objectifs

Les Rulesets etablissent un cadre de controle d'acces et d'integrite strict sur les branches critiques (`main`, `master`, `release/*`) :

1. **Obligation de signature cryptographique** : tout commit introduit dans l'historique doit etre signe par une cle GPG ou SSH verifiee.
2. **Revue de code obligatoire** : interdiction du push direct ; passage requis par une Pull Request avec approbation d'au moins un reviewer / CODEOWNER.
3. **Verification continue des status checks** : obligation de passage au vert de la suite de tests CI/CD avant toute fusion.
4. **Verrouillage de l'historique** : interdiction stricte des push forces (`git push --force`) et des suppressions de branches protegees.

---

## 2. Configuration des Rulesets dans Gitea

### Parametres d'app.ini pour la signature stricte

Dans la section `[repository]` et `[repository.signing]` :

```ini
[repository]
DEFAULT_BRANCH = main
ENABLE_PUSH_CREATE_USER = true

[repository.signing]
SIGNING_KEY = default
SIGNING_NAME = BantuForge Bot
SIGNING_EMAIL = bot@bantuforge.local
INITIAL_COMMIT = always
WIKI = never
CRUD_ACTIONS = pubkey
MERGES = pubkey
DEFAULT_TRUST_MODEL = collaborator
```

---

## 3. Matrice de Protection de Branche

| Regle GitHub Ruleset | Directive Gitea | Effet et Comportement |
| :--- | :--- | :--- |
| Require signed commits | `enable_status_check` + trust_model | Rejette les commits non signes ou avec cle invalide. Badge « Verified » Primer affiche. |
| Require pull request before merging | `enable_push = false` | Bloque les commits directs sur la branche. Seules les PRs validees sont mergeables. |
| Require approvals | `required_approvals >= 1` | Empeche le merge tant que le quota d'approbations n'est pas atteint. |
| Dismiss stale approvals | `dismiss_stale_approvals = true` | Annule les approbations des qu'un nouveau commit est pousse sur la PR. |
| Require status checks | `status_check_contexts` | Attend les validations CI/CD (ex. `pytest`, `sast-security`). |
| Block force pushes | `block_on_official_review_requests = true` | Rejette categoriquement `git push --force` et `git push --delete`. |

---

## 4. Automatisation via l'API REST Forge

Creation ou mise a jour d'une regle de protection via l'API REST de Gitea :

```bash
curl -X POST "http://localhost:3002/api/v1/repos/{owner}/{repo}/branch_protections" \
  -H "Authorization: token $FORGE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rule_name": "main",
    "enable_push": false,
    "enable_push_whitelist": false,
    "push_whitelist_usernames": [],
    "push_whitelist_teams": [],
    "require_signed_commits": true,
    "required_approvals": 1,
    "enable_approvals_whitelist": false,
    "block_on_rejected_reviews": true,
    "dismiss_stale_approvals": true,
    "require_codeowner_review": true,
    "status_check_contexts": ["ci/tests", "security/sast"]
  }'
```

---

## 5. Badges d'Integrite Visuelle Primer

Chaque commit inspecte dans l'interface web affiche son badge conforme Primer :
- **Verified** (`.gh-commit-badge.verified`) : Cle GPG ou SSH validee, trust model collaborateur confirme.
- **Unverified** (`.gh-commit-badge.unverified`) : Signature absente, corrompue ou cle non associee a un compte connu.
