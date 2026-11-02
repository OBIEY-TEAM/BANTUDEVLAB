## Description de la Pull Request

### Contexte et Motivation
<!-- Expliquez brievement le but de cette modification et le probleme resolu. -->

### Type de Changement
- [ ] Correction de bug (fix)
- [ ] Nouvelle fonctionnalite (feat)
- [ ] Optimisation de performances (perf)
- [ ] Renforcement securite ou cryptographie (sec)
- [ ] Documentation ou gabarits UI (docs/ui)

### Verification Qualite et Souverainete
- [ ] La politique stricte Zero-Emoji est respectee (`python scripts/check_no_emoji.py`).
- [ ] Les tests de securite statique Bandit sont 100% propres (`bandit -r apps config -lll`).
- [ ] Le formatage et le linting Ruff sont valides (`ruff check .` et `ruff format --check .`).
- [ ] La suite de tests unitaires et de couverture passe a 100% (`pytest --cov`).
- [ ] Les traces d'audit et la conformite Malabo sont preservees.
