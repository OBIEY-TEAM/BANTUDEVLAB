# TASK20.md - Cycle de Developpement Continu 14 / 20
# Graphe de Commits Moderne GitHub et Topologie de Branches SVG (Network Graph Primer)

> Ce cycle aligne l'affichage de l'historique et du reseau de branches de Gitea sur le graphe GitHub moderne :
> sommets de commits colores, tracage de courbes de fusion SVG, badges de branches Primer et legende
> topologique multi-couleurs.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK20

- [x] **T-GRP-2001 : Styles Primer pour le Graphe de Commits et Reseau de Branches**
  - [x] Ajouter les classes `.gh-graph-container`, `.gh-graph-dot`, `.gh-graph-branch-tag` dans `theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-GRP-2002 : Script d'Amelioration Topologique du Graphe SVG**
  - [ ] Ajouter la palette de couleurs GitHub (Bleu, Vert, Violet, Orange, Rouge) et le lissage SVG dans `custom/templates/custom/header.tmpl`.
  - [ ] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-GRP-2003 : Tests Unitaires et Workflows CI/CD Commit Graph**
  - [ ] Rediger les tests unitaires dans `tests/test_ui_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/commit_graph.yml` et `.gitea/workflows/commit_graph.yaml`.
