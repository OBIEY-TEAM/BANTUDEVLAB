# Guide de contribution

Merci de contribuer à BANTUDEVLAB.

## Mise en place

```bash
python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env && export DEBUG=True
python manage.py migrate
pytest
```

## Flux de travail

1. Créez une branche : `feat/<sujet>`, `fix/<sujet>` ou `docs/<sujet>`.
2. Faites des commits atomiques (convention : `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `security:`).
3. Avant de pousser :

```bash
ruff check . && ruff format --check .
bandit -r apps config -c pyproject.toml
python scripts/check_no_emoji.py
pytest
```

4. Ouvrez une Pull Request avec : contexte, changements, tests ajoutés, impact sécurité.
5. La CI doit être verte et une revue est requise.

## Règles du projet

- **Sécurité d'abord** : toute nouvelle route DRF déclare explicitement `permission_classes` (le défaut est `IsAuthenticated`). Validez et bornez toutes les entrées.
- **Pas de secret en dur** : utilisez les variables d'environnement (`.env.example` documente chaque variable).
- **Pas d'emoji** dans l'interface, le CSS/JS et la documentation : utilisez `{% icon "nom" %}` / `{% flag "CIV" %}`. Pour ajouter une icône, complétez `ICONS` dans `apps/core/templatetags/icons.py`.
- **Pas de CDN** : toutes les ressources sont auto-hébergées (souveraineté et CSP).
- **Tests** : toute correction ou fonctionnalité s'accompagne de tests ; couverture minimale imposée par `pyproject.toml`.
- **Encodage** : UTF-8, voir `.editorconfig`.

## Rapporter un bug

Ouvrez une issue avec les étapes de reproduction, le comportement attendu et observé, la version. Pour une faille de sécurité, suivez [SECURITY.md](SECURITY.md).
