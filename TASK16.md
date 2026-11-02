# TASK16.md - Cycle de Developpement Continu 10 / 20
# Centre de Notifications Moderne GitHub (Inbox, Filtres Unread / Participating / Mentioned)

> Ce cycle aligne l'interface du centre de notifications de Gitea sur GitHub moderne :
> onglets de filtrage (Inbox, Non lus, En cours de participation, Mentions), badges d'etat Primer,
> et raccourcis clavier de gestion des alertes.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK16

- [ ] **T-NTF-1601 : Styles Primer pour le Centre de Notifications**
  - [ ] Ajouter les classes `.gh-notifications-nav`, `.gh-notification-item`, `.gh-notification-unread`, `.gh-filter-badge` dans `custom/public/assets/css/theme-github.css` et `theme-github-dark.css`.
  - [ ] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-NTF-1602 : Script de Filtrage Dynamique et Raccourci Clavier**
  - [ ] Ajouter le mecanisme de tri cote client (Non lus, Mentions, Participations) et le raccourci `m` dans `custom/templates/custom/header.tmpl`.
  - [ ] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-NTF-1603 : Tests de Conformite et Pipeline CI/CD Notifications**
  - [ ] Rediger les tests unitaires dans `tests/test_ui_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/notifications_inbox.yml` et `.gitea/workflows/notifications_inbox.yaml`.
