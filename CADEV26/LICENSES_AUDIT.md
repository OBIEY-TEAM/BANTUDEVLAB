# Audit Exhaustif des Licences Logicielles — BANTUDEVLAB (CADEV 2026)

> **Équipe candidate : CYBERSOCLE**  
> - **Capitaine d'équipe :** OBIEY Christ Dany  
> - **Membre de l'équipe :** MAMPOUYA Alicia Syrianne  
> **Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
> **Conformité au règlement CADEV 2026 (Systalink) :**  
> Le règlement stipule que tout composant sous licence GPL, AGPL ou LGPL rend le projet irrecevable.  
> Seules les licences permissives (**MIT, Apache 2.0, BSD 2/3-Clause, PSF, ISC, Public Domain**) sont strictement admises.  
> Date d'audit : 12 novembre 2026 — Inventaire généré via `pip-licenses` et inspection approfondie de l'écosystème.

---

## 1. Synthèse Exécutive de Conformité

| Catégorie | Total Composants | Conformes (Permissifs) | Bloquants identifiés | À vérifier / Exceptions |
| :--- | :---: | :---: | :---: | :---: |
| **Dépendances Python (directes + transitives)** | 66 | 63 | 2 (`psycopg2-binary`, `python-gitlab`) | 1 (`certifi` - MPL 2.0) |
| **Infrastructure, Moteurs & Frontend** | 10 | 8 | 1 (`redis:7-alpine` remplacé par Valkey) | 1 (`gemma2:2b` - Google Terms) |

### Points d'Attention Majeurs & Mesures Prises

1. **Bascule immédiate de Redis vers Valkey 7.2 (BSD-3-Clause) :**
   - **Constat :** Depuis la version 7.4, Redis n'est plus distribué sous licence open-source BSD libre (passage sous double licence RSALv2 / SSPLv1).
   - **Mesure appliquée :** Remplacement immédiat dans `docker-compose.yml` et `docker-compose.production.yml` par **Valkey** (`valkey/valkey:7.2-alpine`), le fork communautaire sous égide de la **Linux Foundation** sous licence **BSD-3-Clause** stricte. Valkey est un *drop-in replacement* 100% compatible protocolairement et fonctionnellement avec Celery et Django-Redis.

2. **Composant bloquant `psycopg2-binary` (LGPL with exceptions) :**
   - **Constat :** Le driver PostgreSQL historique de Django `psycopg2-binary` (ainsi que `psycopg` v3) est sous licence GNU LGPL. Le backend PostgreSQL standard de Django s'appuie sur ce pilote.
   - **Remplacement permissif proposé :** Le pilote pur Python **`pg8000`** (distribué sous licence **BSD-3-Clause**) ou l'utilisation du backend SQLite (Domaine Public) pour les démonstrations autonomes.
   - **Évaluation du risque :** Remplacer le driver de base de données à quelques jours de la soumission présente un risque critique d'instabilité sur le schéma relationnel et les transactions de production. Conformément à la règle de prudence (« *Sinon, liste-le sans le modifier* »), `psycopg2-binary` est documenté comme composant bloquant avec son plan de transition sans altération prématurée de l'ORM.

3. **Composant bloquant `python-gitlab` (LGPL-3.0-or-later) :**
   - **Constat :** La bibliothèque cliente `python-gitlab` déclarée dans `requirements.txt` est sous licence LGPLv3.
   - **Remplacement permissif proposé :** Appels HTTP directs via la bibliothèque **`requests`** (déjà incluse sous licence **Apache 2.0**), exactement comme l'implémentation de référence de `GiteaClient` (`apps/gitea_client/client.py`) qui n'embarque aucun SDK externe et reste 100% Apache-2.0.

4. **Modèle de langage Google Gemma 2 2B (Ollama) :**
   - **Statut :** Le logiciel d'inférence Ollama est sous licence **MIT**. Le modèle de poids `gemma2:2b` est régi par les **Gemma Terms of Use de Google**. Il n'est pas redistribué dans le code source de BantuDevLab mais téléchargé localement sur le serveur d'inférence. Il ne doit pas être qualifié de permissif.

---

## 2. Inventaire des Composants d'Infrastructure et Frontend

| Composant | Version | Licence Détectée | Rôle / Usage | Statut CADEV 2026 | Notes & Plan de Remplacement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Valkey (remplacement de Redis)** | `7.2.7-alpine` | BSD-3-Clause | Infrastructure / Cache & Broker | **OK (Permissif)** | Drop-in replacement 100% compatible Redis fork Linux Foundation sous licence BSD-3-Clause. Remplace Redis >= 7.4 qui n'est plus BSD. |
| **Redis (version antérieure)** | `7-alpine (>= 7.4)` | RSALv2 / SSPLv1 (Non BSD depuis 7.4) | Infrastructure / Cache & Broker | **À remplacer (Bloquant CADEV)** | Depuis Redis 7.4, Redis n'est plus distribué sous licence BSD libre. Remplacé sans risque par Valkey 7.2 (BSD-3-Clause). |
| **Gitea CE** | `1.22` | MIT License | Forge Git Principale | **OK (Permissif)** | Forge Git distribuée légère sous licence permissive MIT. |
| **GitLab CE (Omnibus)** | `16.11.0-ce.0` | MIT License (GitLab CE) | Forge Git Secondaire / Fédérée | **OK (Permissif)** | L'édition Community Edition (CE / FOSS) est sous licence MIT. |
| **PostgreSQL** | `16-alpine` | PostgreSQL License | Base de données | **OK (Permissif)** | Licence permissive approuvée OSI (équivalente BSD / MIT). |
| **PgBouncer** | `latest (edoburu/pgbouncer)` | BSD-2-Clause | Pooler de connexions PostgreSQL | **OK (Permissif)** | Licence permissive BSD 2-Clause. |
| **Nginx** | `1.27-alpine` | 2-Clause BSD License | Reverse Proxy & TLS 1.3 Gateway | **OK (Permissif)** | Licence permissive 2-Clause BSD. |
| **Ollama (moteur d'inférence)** | `latest` | MIT License | Serveur d'inférence IA locale | **OK (Permissif)** | Le logiciel Ollama est distribué sous licence MIT permissive. |
| **Gemma 2 2B (modèle IA Google)** | `2B-IT (quantifié Q4_K_M)` | Gemma Terms of Use (Google) | Modèle de poids d'IA | **À vérifier / Conforme aux CGU (Non redistribué)** | Exécuté localement sans redistribution. Non qualifié de permissif (conditions d'utilisation spécifiques Google). Non bloquant car exécuté localement comme un modèle tiers. |
| **CodeMirror 5** | `5.65.16` | MIT License | Composant Frontend / Éditeur de code | **OK (Permissif)** | Auto-hébergé dans `static/vendor/codemirror/` sous licence MIT (Marijn Haverbeke). Zéro CDN tiers. |

---

## 3. Inventaire Complet des Dépendances Python (Directes et Transitives)

Inventaire exhaustif généré dans l'environnement virtuel du projet (`.venv`) via `pip-licenses` et introspection `importlib.metadata` :

| Paquet Python | Version | Licence Déclarée | Statut CADEV 2026 | Site Officiel / Référentiel | Remarques |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **amqp** | `5.4.1` | BSD License | **OK (Permissif)** | [amqp](http://github.com/celery/py-amqp) | Licence libre permissive conforme au règlement CADEV 2026. |
| **asgiref** | `3.13.0` | BSD-3-Clause | **OK (Permissif)** | [asgiref](https://github.com/django/asgiref/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **attrs** | `26.1.0` | MIT | **OK (Permissif)** | [attrs](https://www.attrs.org/en/stable/changelog.html) | Licence libre permissive conforme au règlement CADEV 2026. |
| **bandit** | `1.9.4` | Apache-2.0 | **OK (Permissif)** | [bandit](https://bandit.readthedocs.io/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **billiard** | `4.3.1` | BSD License | **OK (Permissif)** | [billiard](https://github.com/celery/billiard) | Licence libre permissive conforme au règlement CADEV 2026. |
| **celery** | `5.6.3` | BSD-3-Clause | **OK (Permissif)** | [celery](https://docs.celeryq.dev/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **certifi** | `2026.10.23` | Mozilla Public License 2.0 (MPL 2.0) | **À vérifier (Weak Copyleft)** | [certifi](https://github.com/certifi/python-certifi) | Mozilla Public License 2.0. Autorise l'intégration sans contamination si utilisé sous forme de bibliothèque dynamique sans modification. |
| **cffi** | `2.1.1` | MIT-0 | **OK (Permissif)** | [cffi](https://cffi.readthedocs.io/en/latest/whatsnew.html) | Licence libre permissive conforme au règlement CADEV 2026. |
| **charset-normalizer** | `3.5.2` | MIT | **OK (Permissif)** | [charset-normalizer](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md) | Licence libre permissive conforme au règlement CADEV 2026. |
| **click** | `8.5.0` | BSD-3-Clause | **OK (Permissif)** | [click](https://github.com/pallets/click/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **click-didyoumean** | `0.3.1` | MIT License | **OK (Permissif)** | [click-didyoumean](https://github.com/click-contrib/click-didyoumean) | Licence libre permissive conforme au règlement CADEV 2026. |
| **click-plugins** | `1.1.1.2` | BSD License | **OK (Permissif)** | [click-plugins](https://github.com/click-contrib/click-plugins) | Licence libre permissive conforme au règlement CADEV 2026. |
| **click-repl** | `0.4.1` | MIT | **OK (Permissif)** | [click-repl](https://github.com/click-contrib/click-repl) | Licence libre permissive conforme au règlement CADEV 2026. |
| **colorama** | `0.4.6` | BSD License | **OK (Permissif)** | [colorama](https://github.com/tartley/colorama) | Licence libre permissive conforme au règlement CADEV 2026. |
| **coverage** | `7.17.0` | Apache-2.0 | **OK (Permissif)** | [coverage](https://github.com/coveragepy/coveragepy) | Licence libre permissive conforme au règlement CADEV 2026. |
| **cryptography** | `50.0.2` | Apache-2.0 OR BSD-3-Clause | **OK (Permissif)** | [cryptography](https://github.com/pyca/cryptography) | Licence libre permissive conforme au règlement CADEV 2026. |
| **Django** | `5.2.18` | BSD-3-Clause | **OK (Permissif)** | [Django](https://www.djangoproject.com/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **djangorestframework** | `3.18.3` | BSD-3-Clause | **OK (Permissif)** | [djangorestframework](https://www.django-rest-framework.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **drf-spectacular** | `0.30.0` | BSD-3-Clause | **OK (Permissif)** | [drf-spectacular](https://github.com/tfranzel/drf-spectacular) | Licence libre permissive conforme au règlement CADEV 2026. |
| **greenlet** | `3.5.6` | MIT AND PSF-2.0 | **OK (Permissif)** | [greenlet](https://greenlet.readthedocs.io) | Licence libre permissive conforme au règlement CADEV 2026. |
| **gunicorn** | `26.2.0` | MIT | **OK (Permissif)** | [gunicorn](https://gunicorn.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **h11** | `0.16.0` | MIT License | **OK (Permissif)** | [h11](https://github.com/python-hyper/h11) | Licence libre permissive conforme au règlement CADEV 2026. |
| **idna** | `3.20` | BSD-3-Clause | **OK (Permissif)** | [idna](https://github.com/kjd/idna) | Licence libre permissive conforme au règlement CADEV 2026. |
| **inflection** | `0.5.1` | MIT License | **OK (Permissif)** | [inflection](https://github.com/jpvanhal/inflection) | Licence libre permissive conforme au règlement CADEV 2026. |
| **iniconfig** | `2.3.1` | MIT | **OK (Permissif)** | [iniconfig](https://github.com/pytest-dev/iniconfig) | Licence libre permissive conforme au règlement CADEV 2026. |
| **jsonschema** | `4.26.0` | MIT | **OK (Permissif)** | [jsonschema](https://github.com/python-jsonschema/jsonschema) | Licence libre permissive conforme au règlement CADEV 2026. |
| **jsonschema-specifications** | `2025.9.1` | MIT | **OK (Permissif)** | [jsonschema-specifications](https://github.com/python-jsonschema/jsonschema-specifications) | Licence libre permissive conforme au règlement CADEV 2026. |
| **kombu** | `5.6.2` | BSD-3-Clause | **OK (Permissif)** | [kombu](https://kombu.readthedocs.io) | Licence libre permissive conforme au règlement CADEV 2026. |
| **markdown-it-py** | `4.2.0` | MIT License | **OK (Permissif)** | [markdown-it-py](https://github.com/executablebooks/markdown-it-py) | Licence libre permissive conforme au règlement CADEV 2026. |
| **mdurl** | `0.1.2` | MIT License | **OK (Permissif)** | [mdurl](https://github.com/executablebooks/mdurl) | Licence libre permissive conforme au règlement CADEV 2026. |
| **packaging** | `26.3` | Apache-2.0 OR BSD-2-Clause | **OK (Permissif)** | [packaging](https://github.com/pypa/packaging) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pillow** | `13.0.0` | MIT-CMU | **OK (Permissif)** | [pillow](https://python-pillow.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pip** | `25.2` | MIT | **OK (Permissif)** | [pip](https://pip.pypa.io) | Outil de gestion des paquets Python sous licence libre MIT. |
| **pip-licenses** | `5.5.5` | MIT | **OK (Permissif)** | [pip-licenses](https://github.com/raimon49/pip-licenses) | Outil d'audit des licences logicielles sous licence libre MIT. |
| **playwright** | `1.64.1` | Apache-2.0 | **OK (Permissif)** | [playwright](https://github.com/Microsoft/playwright-python) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pluggy** | `1.7.0` | MIT License | **OK (Permissif)** | [pluggy](https://github.com/pytest-dev/pluggy) | Licence libre permissive conforme au règlement CADEV 2026. |
| **prettytable** | `3.18.0` | BSD-3-Clause | **OK (Permissif)** | [prettytable](https://github.com/jazzband/prettytable) | Affichage tabulaire sous licence libre BSD-3-Clause. |
| **prompt_toolkit** | `3.0.53` | BSD License | **OK (Permissif)** | [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) | Licence libre permissive conforme au règlement CADEV 2026. |
| **psycopg2-binary** | `2.9.13` | LGPL-3.0-or-later with exceptions | **À remplacer (Bloquant CADEV)** | [psycopg2-binary](https://psycopg.org/) | Pilote PostgreSQL officiel sous licence LGPLv3. Django dépend de psycopg2/psycopg3 (tous deux LGPL). Remplacement permissif proposé : pg8000 (BSD-3-Clause) ou SQLite (Public Domain). |
| **pycparser** | `3.12` | BSD-3-Clause | **OK (Permissif)** | [pycparser](https://github.com/eliben/pycparser) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pyee** | `14.0.0` | MIT License | **OK (Permissif)** | [pyee](https://github.com/jfhbrook/pyee) | Licence libre permissive conforme au règlement CADEV 2026. |
| **Pygments** | `2.21.0` | BSD-2-Clause | **OK (Permissif)** | [Pygments](https://pygments.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pytest** | `9.2.0` | MIT | **OK (Permissif)** | [pytest](https://docs.pytest.org/en/latest/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pytest-cov** | `7.1.0` | MIT | **OK (Permissif)** | [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/changelog.html) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pytest-django** | `4.14.0` | BSD License | **OK (Permissif)** | [pytest-django](https://github.com/pytest-dev/pytest-django) | Licence libre permissive conforme au règlement CADEV 2026. |
| **python-dateutil** | `4.0.0` | BSD-3-Clause | **OK (Permissif)** | [python-dateutil](https://github.com/dateutil/dateutil) | Licence libre permissive conforme au règlement CADEV 2026. |
| **python-dotenv** | `1.2.4` | BSD-3-Clause | **OK (Permissif)** | [python-dotenv](https://github.com/theskumar/python-dotenv) | Licence libre permissive conforme au règlement CADEV 2026. |
| **python-gitlab** | `8.6.0` | LGPL-3.0-or-later | **À remplacer (Bloquant CADEV)** | [python-gitlab](https://github.com/python-gitlab/python-gitlab) | SDK d'intégration GitLab API v4 sous licence LGPLv3. Remplacement permissif sans risque proposé : appels HTTP directs via 'requests' (Apache 2.0). |
| **PyYAML** | `6.0.3` | MIT License | **OK (Permissif)** | [PyYAML](https://pyyaml.org/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **redis** | `8.1.0` | MIT | **OK (Permissif)** | [redis](https://github.com/redis/redis-py) | Bibliothèque cliente Python sous licence MIT. Le serveur Redis >= 7.4 (non-BSD) a été remplacé par Valkey 7.2 (BSD-3). |
| **referencing** | `0.37.0` | MIT | **OK (Permissif)** | [referencing](https://github.com/python-jsonschema/referencing) | Licence libre permissive conforme au règlement CADEV 2026. |
| **requests** | `2.34.2` | Apache Software License | **OK (Permissif)** | [requests](https://github.com/psf/requests) | Licence libre permissive conforme au règlement CADEV 2026. |
| **requests-toolbelt** | `1.0.0` | Apache Software License | **OK (Permissif)** | [requests-toolbelt](https://toolbelt.readthedocs.io/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **rich** | `15.0.0` | MIT License | **OK (Permissif)** | [rich](https://github.com/Textualize/rich) | Licence libre permissive conforme au règlement CADEV 2026. |
| **rpds-py** | `2026.9.1` | MIT | **OK (Permissif)** | [rpds-py](https://github.com/crate-py/rpds) | Licence libre permissive conforme au règlement CADEV 2026. |
| **ruff** | `0.17.3` | MIT | **OK (Permissif)** | [ruff](https://docs.astral.sh/ruff) | Licence libre permissive conforme au règlement CADEV 2026. |
| **sqlparse** | `0.6.1` | BSD License | **OK (Permissif)** | [sqlparse](https://github.com/andialbrecht/sqlparse) | Licence libre permissive conforme au règlement CADEV 2026. |
| **stevedore** | `5.9.1` | Apache-2.0 | **OK (Permissif)** | [stevedore](https://docs.openstack.org/stevedore) | Licence libre permissive conforme au règlement CADEV 2026. |
| **typing_extensions** | `4.16.0` | PSF-2.0 | **OK (Permissif)** | [typing_extensions](https://github.com/python/typing_extensions) | Licence libre permissive conforme au règlement CADEV 2026. |
| **tzdata** | `2026.6` | Apache-2.0 | **OK (Permissif)** | [tzdata](https://github.com/python/tzdata) | Licence libre permissive conforme au règlement CADEV 2026. |
| **tzlocal** | `5.4.5` | MIT | **OK (Permissif)** | [tzlocal](https://github.com/regebro/tzlocal/blob/master/CHANGES.txt) | Licence libre permissive conforme au règlement CADEV 2026. |
| **uritemplate** | `4.2.0` | BSD 3-Clause OR Apache-2.0 | **OK (Permissif)** | [uritemplate](https://uritemplate.readthedocs.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **urllib3** | `2.8.0` | MIT | **OK (Permissif)** | [urllib3](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst) | Licence libre permissive conforme au règlement CADEV 2026. |
| **uvicorn** | `0.54.0` | BSD-3-Clause | **OK (Permissif)** | [uvicorn](https://uvicorn.dev/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **vine** | `5.1.0` | BSD License | **OK (Permissif)** | [vine](https://github.com/celery/vine) | Licence libre permissive conforme au règlement CADEV 2026. |
| **wcwidth** | `0.9.4` | MIT | **OK (Permissif)** | [wcwidth](https://github.com/jquast/wcwidth) | Calcul de largeur de caractères sous licence libre MIT. |

---

## 4. Recommandations et Plan d'Action pour le Comité CADEV 2026

1. **Validation de l'exception pour le pilote de base de données :** Demander formellement au comité CADEV (via `cadev@systalink.com`) une tolérance sur le driver client PostgreSQL (`psycopg2-binary`) en raison de l'architecture native du framework Django, ou présenter l'alternative conteneurisée SQLite/pg8000.
2. **Suppression ou réécriture de `apps/gitlab_client` :** Remplacer le SDK `python-gitlab` par de simples requêtes REST `requests.get()` / `requests.post()` vers `/api/v4` de GitLab pour éliminer toute dépendance LGPL du fichier `requirements.txt`.
3. **Maintien de Valkey en production :** Valider l'usage exclusif de Valkey 7.2 (BSD-3-Clause) sur l'infrastructure de déploiement Hostinger / Systalink Cloud.
