# Architecture de la File d'Attente de Fusion Souveraine (Merge Queue)

Ce document specifie le mecanisme de serialisation et de validation automatique des Pull Requests via Merge Queue sur la forge BantuDevLab / Gitea.

---

## 1. Principes et Necessite de la Merge Queue

Dans un projet collaboratif a haut debit de commits, deux Pull Requests testees individuellement au vert peuvent provoquer une rupture de build ou un conflit semantique une fois fusionnees ensemble sur `main`.

La Merge Queue resout ce defi par une serialisation ordonnee :
1. **Entree en file** : les PRs approuvees sont ajoutees a la file d'attente FIFO.
2. **Rebase d'essai temporaire** : chaque PR est testee sur la branche cible hypothetique incorporant les PRs precedemment validees de la file.
3. **Validation cryptographique** : confirmation que chaque commit composant la file est signe par une cle autorisee.
4. **Fusion atomique automatique** : fusion definitive des commits sur la branche cible principale.

---

## 2. Criteres d'Admission et d'Evaluation

| Critere | Statut Requis | Action en cas d'Echec |
| :--- | :--- | :--- |
| **Draft status** | Non-brouillon (`draft == false`) | Rejet immediat de la file d'attente |
| **Approbations** | `approvals >= required_approvals` | Maintien en attente de review |
| **Signature de commit** | `verified == true` et cle collaborateur | Blocage de securite, notification de re-signature |
| **Status checks CI** | `success` sur tous les contextes requis | Retrait de la file et alerte du committer |

---

## 3. Moteur de Simulation et Script d'Execution

Le composant `scripts/simulate_merge_queue.py` fournit une verification programmatique utilisable en ligne de commande ou dans les pipelines CI/CD :

```bash
python scripts/simulate_merge_queue.py --input build/pending_queue.json
```

Les resultats fournissent le decompte total (`total_queued`, `merged`, `blocked`) et le positionnement dans la file.
