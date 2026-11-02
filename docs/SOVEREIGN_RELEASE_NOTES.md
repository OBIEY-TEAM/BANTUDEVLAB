# Specification du Generateur Automatique de Notes de Version

Ce document decrit le systeme de generation automatisee des notes de publication (Release Notes) au standard GitHub pour BantuDevLab et la forge souveraine Gitea.

---

## 1. Principes et Fonctionnement

Le generateur automatise analyse l'ensemble des Pull Requests et commits fusionnes entre deux jalons Git (tags) et structure le rapport selon les directives de configuration `.github/release.yml` et `.gitea/release.yml` :

1. **Extraction semantique** : classification automatique selon les pre動es conventionnels (`feat:`, `fix:`, `sec:`, `docs:`, `test:`, `refactor:`, `chore:`).
2. **Attribution des auteurs** : reconnaissance des contributeurs `@username` et mise en avant des nouvelles contributions.
3. **Lien de comparaison complet** : reference directe vers le diff comparatif de la forge (`/compare/{prev_tag}...{current_tag}`).
4. **Filtrage des dependances** : exclusion optionnelle des bots de mise a jour (`dependabot`, `renovate`).

---

## 2. Configuration Standard (.github/release.yml & .gitea/release.yml)

```yaml
changelog:
  exclude:
    labels:
      - ignore-for-release
      - dependencies
    authors:
      - dependabot
      - renovate[bot]
  categories:
    - title: Exciting New Features
      labels:
        - feature
        - enhancement
    - title: Bug Fixes
      labels:
        - fix
        - bug
    - title: Security & Hardening
      labels:
        - security
        - vulnerability
    - title: Documentation Updates
      labels:
        - documentation
        - docs
    - title: Maintenance & Testing
      labels:
        - refactor
        - test
        - chore
```

---

## 3. Utilisation en Ligne de Commande

Le script `scripts/generate_release_notes.py` s'execute nativement dans les pipelines CI/CD :

```bash
python scripts/generate_release_notes.py \
  --input build/merged_prs.json \
  --prev v1.0.0 \
  --current v1.1.0 \
  --repo-url https://forge.bantudevlab.local/bantudev/bantudevlab
```

Le document Markdown genere respecte l'apparence et les composants Primer de GitHub Releases.
