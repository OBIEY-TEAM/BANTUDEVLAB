# TASK13.md - Cycle de Developpement Continu 7 / 20
# Reactions Accessibles et Polyfill de Raccourcis GitHub sans Emoji

> Ce cycle apporte a Gitea l'experience interactive des reactions GitHub (`+1`, `Rocket`, `Heart`, etc.)
> a travers des pastilles et symboles SVG accessibles, conformes a la politique stricte zero-emoji de BantuDevLab.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK13

- [x] **T-REA-1301 : Pastilles de Reactions Primer sans Emojis (SVG & Badges Textuels)**
  - [x] Styliser les boutons de reactions (`.gh-reaction-btn`, `.gh-reaction-badge`) dans `custom/public/assets/css/theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-REA-1302 : Polyfill de Conversion des Shortcodes GitHub (`:+1:`, `:heart:`, `:rocket:`)**
  - [ ] Ajouter le filtre JavaScript de conversion automatique des codes textuels GitHub vers des badges accessibles dans `custom/templates/custom/header.tmpl`.
  - [ ] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-REA-1303 : Tests Unitaires et Pipeline CI/CD pour les Reactions**
  - [ ] Rediger les tests unitaires dans `tests/test_design_and_ux.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/reactions_polyfill.yml` et `.gitea/workflows/reactions_polyfill.yaml`.
