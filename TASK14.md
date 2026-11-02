# TASK14.md - Cycle de Developpement Continu 8 / 20
# Inspection des Livraisons Webhook et Simulateur de Rejeu (Redelivery)

> Ce cycle apporte a Gitea l'equivalent moderne de l'inspecteur de livraisons de webhooks de GitHub,
> permettant d'analyser les en-tetes, le payload, le code retour HTTP, et de declencher le rejeu (Redeliver).

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK14

- [x] **T-WHK-1401 : Point d'Acces de Rejeu de Livraisons Webhook (`/api/forge/webhooks/redeliver/`)**
  - [x] Implementer la vue `WebhookRedeliverView` dans `apps/gitea_client/views.py` et `urls.py`.
  - [x] Permettre la reinjection securisee des evenements `push`, `pull_request` et `issues`.

- [x] **T-WHK-1402 : Styles Primer pour l'Inspecteur de Livraisons de Webhooks**
  - [x] Integrer les classes `.gh-webhook-delivery-item`, `.gh-status-pill` dans `custom/public/assets/css/theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-WHK-1403 : Tests Unitaires et Pipeline CI/CD pour les Webhooks**
  - [ ] Rediger les tests unitaires dans `tests/test_gitea_client.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/webhook_deliveries.yml` et `.gitea/workflows/webhook_deliveries.yaml`.
