# TASK24.md - Cycle de Developpement Continu 18 / 20
# File d'Attente de Fusion GitHub (Merge Queue & Simulation de Fusion Automatique)

> Ce cycle apporte a Gitea l'experience avancee de GitHub Merge Queue :
> serialisation securisee des Pull Requests pretes, execution des status checks en file d'attente,
> badges Primer de positionnement et validation avant fusion automatique.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK24

- [ ] **T-MRG-2401 : Styles Primer pour la File d'Attente de Fusion (Merge Queue)**
  - [ ] Ajouter les styles `.gh-merge-queue-badge`, `.gh-merge-queue-box`, `.gh-merge-queue-item` dans `theme-github.css` et `theme-github-dark.css`.
  - [ ] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-MRG-2402 : Moteur de Simulation et Specification de File de Fusion**
  - [ ] Implementer `scripts/simulate_merge_queue.py` pour valider les fusions en file selon les checks CI et l'ordre FIFO.
  - [ ] Documenter le fonctionnement dans `docs/SOVEREIGN_MERGE_QUEUE.md`.

- [ ] **T-MRG-2403 : Tests Unitaires et Workflows CI/CD Merge Queue**
  - [ ] Rediger les tests unitaires dans `tests/test_sec_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/merge_queue.yml` et `.gitea/workflows/merge_queue.yaml`.
