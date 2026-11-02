# Guide de Recherche de Code Avancee Souveraine (Bleve & Qualificateurs GitHub)

Ce document specifie les capacites du moteur de recherche de code et la syntaxe des requetes de recherche avancee sur l'infrastructure forge souveraine BantuDevLab / Gitea.

---

## 1. Moteur d'Indexation Bleve

Gitea integre le moteur d'indexation Bleve en Go natif. La configuration dans `app.ini` active l'indexation de code au niveau global :

```ini
[indexer]
ISSUE_INDEXER_TYPE = bleve
REPO_INDEXER_ENABLED = true
REPO_INDEXER_TYPE = bleve
REPO_INDEXER_PATH = data/indexers/repos.bleve
REPO_INDEXER_INCLUDE = **.py,**.js,**.ts,**.go,**.rs,**.html,**.css,**.md,**.tmpl,**.yml,**.yaml
REPO_INDEXER_EXCLUDE = **/node_modules/**,**/vendor/**,**/.git/**,**/tests/**
MAX_FILE_SIZE = 1048576
```

---

## 2. Qualificateurs de Recherche Supportes

A l'instar de GitHub, la recherche globale et de depot accepte les filtres semantiques suivants :

| Qualificateur | Description | Exemple de Requete |
| :--- | :--- | :--- |
| `path:` | Filtre par chemin de fichier | `auth path:apps/core/` |
| `extension:` | Filtre par extension de fichier | `def calculate extension:py` |
| `repo:` | Ciblage specifique d'un depot | `crypto repo:bantudev/bantudevlab` |
| `lang:` | Filtre par langage de programmation | `ZKPCrypto lang:python` |
| `symbol:` | Recherche de declaration de symbole | `symbol:AuditTrail` |

---

## 3. Recherche par Expressions Regulieres (Regex)

Le moteur supporte les requetes regex exactes entourees de barres obliques `/.../` :

```text
/def\s+[a-zA-Z0-9_]+\(/ extension:py
```

---

## 4. Interface Graphique Primer et Popover d'Auto-completion

Lorsque le champ de recherche global est active (`/` ou clic), un popover Primer (`.gh-search-qualifiers-popover`) presente les qualificateurs cliquables qui sont automatiquement injectes dans la requete utilisateur sans rechargement de page.
