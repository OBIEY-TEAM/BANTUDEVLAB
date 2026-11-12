# Third-Party Software Licenses — BANTUDEVLAB

This file contains the comprehensive inventory of third-party software components, libraries, and tools used by **BantuDevLab**, audited for strict compliance with the CADEV 2026 regulations (Article 6).

Only permissive open-source licenses (**MIT, Apache-2.0, BSD 2/3-Clause, PSF, ISC, Public Domain**) are utilized for runtime dependencies.

---

## 1. Core Platform & Infrastructure Components

| Component | Version | License | Upstream Project / Repository | Usage Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Gitea Community Edition** | `1.22` | MIT License | https://github.com/go-gitea/gitea | Primary Git forge engine. Used as-is, without code modification. |
| **Valkey** | `7.2-alpine` | BSD-3-Clause | https://github.com/valkey-io/valkey | In-memory cache and task broker. Official Linux Foundation BSD-3 replacement for Redis >= 7.4. |
| **Nginx** | `1.27-alpine` | 2-Clause BSD License | https://nginx.org/ | Edge reverse proxy and TLS 1.3 gateway. |
| **PostgreSQL** | `16-alpine` | PostgreSQL License | https://www.postgresql.org/ | Relational database (optional production engine). Permissive OSI-approved license. |
| **Ollama** | `latest` | MIT License | https://github.com/ollama/ollama | Local inference runtime engine for offline AI assistance. |
| **Google Gemma 2 2B** | `2b-instruct` | Google Gemma Terms of Use | https://ai.google.dev/gemma | Local foundation model. Executed offline via Ollama. Not redistributed in the source repository. |
| **CodeMirror 5** | `5.65.16` | MIT License | https://github.com/codemirror/codemirror5 | Self-hosted embedded code editor in Workbench. Zero external CDN dependencies. |

---

## 2. Python Runtime Dependencies (`requirements.txt`)

All runtime packages are strictly permissive:

| Package | Version | License | Repository |
| :--- | :--- | :--- | :--- |
| **Django** | `5.2.18` | BSD-3-Clause | https://www.djangoproject.com/ |
| **djangorestframework** | `3.18.3` | BSD-3-Clause | https://www.django-rest-framework.org |
| **requests** | `2.34.2` | Apache-2.0 | https://requests.readthedocs.io |
| **requests-toolbelt** | `1.0.0` | Apache-2.0 | https://toolbelt.readthedocs.io/ |
| **cryptography** | `50.0.2` | Apache-2.0 OR BSD-3-Clause | https://cryptography.io |
| **python-dotenv** | `1.2.4` | BSD-3-Clause | https://github.com/theskumar/python-dotenv |
| **celery** | `5.6.3` | BSD-3-Clause | https://docs.celeryq.dev/ |
| **redis** | `8.1.0` | MIT | https://github.com/redis/redis-py |
| **gunicorn** | `26.2.0` | MIT | https://gunicorn.org |
| **uvicorn** | `0.54.0` | BSD-3-Clause | https://uvicorn.dev/ |
| **drf-spectacular** | `0.30.0` | BSD-3-Clause | https://github.com/tfranzel/drf-spectacular |
| **pillow** | `13.0.0` | MIT-CMU / HPND | https://python-pillow.org |

---

## 3. Transitive Python Dependencies

| Package | Version | License | Upstream Link |
| :--- | :--- | :--- | :--- |
| **amqp** | `5.4.1` | BSD License | https://github.com/celery/py-amqp |
| **asgiref** | `3.13.0` | BSD-3-Clause | https://github.com/django/asgiref/ |
| **attrs** | `26.1.0` | MIT | https://www.attrs.org/ |
| **billiard** | `4.3.1` | BSD License | https://github.com/celery/billiard |
| **cffi** | `2.1.1` | MIT-0 | https://cffi.readthedocs.io/ |
| **charset-normalizer** | `3.5.2` | MIT | https://github.com/jawah/charset_normalizer |
| **click** | `8.5.0` | BSD-3-Clause | https://palletsprojects.com/p/click/ |
| **click-didyoumean** | `0.3.1` | MIT License | https://github.com/click-contrib/click-didyoumean |
| **click-plugins** | `1.1.1.2` | BSD License | https://github.com/click-contrib/click-plugins |
| **click-repl** | `0.4.1` | MIT | https://github.com/click-contrib/click-repl |
| **colorama** | `0.4.6` | BSD License | https://github.com/tartley/colorama |
| **greenlet** | `3.5.6` | MIT AND PSF-2.0 | https://greenlet.readthedocs.io |
| **h11** | `0.16.0` | MIT License | https://github.com/python-hyper/h11 |
| **idna** | `3.20` | BSD-3-Clause | https://github.com/kjd/idna |
| **inflection** | `0.5.1` | MIT License | https://github.com/jpvanhal/inflection |
| **iniconfig** | `2.3.1` | MIT | https://github.com/pytest-dev/iniconfig |
| **jsonschema** | `4.26.0` | MIT | https://github.com/python-jsonschema/jsonschema |
| **jsonschema-specifications** | `2025.9.1` | MIT | https://github.com/python-jsonschema/jsonschema-specifications |
| **kombu** | `5.6.2` | BSD-3-Clause | https://kombu.readthedocs.io |
| **markdown-it-py** | `4.2.0` | MIT License | https://github.com/executablebooks/markdown-it-py |
| **mdurl** | `0.1.2` | MIT License | https://github.com/executablebooks/mdurl |
| **packaging** | `26.3` | Apache-2.0 OR BSD-2-Clause | https://github.com/pypa/packaging |
| **pluggy** | `1.7.0` | MIT License | https://github.com/pytest-dev/pluggy |
| **prettytable** | `3.18.0` | BSD-3-Clause | https://github.com/jazzband/prettytable |
| **prompt_toolkit** | `3.0.53` | BSD License | https://github.com/prompt-toolkit/python-prompt-toolkit |
| **pycparser** | `3.12` | BSD-3-Clause | https://github.com/eliben/pycparser |
| **pyee** | `14.0.0` | MIT License | https://github.com/jfhbrook/pyee |
| **Pygments** | `2.21.0` | BSD-2-Clause | https://pygments.org |
| **python-dateutil** | `4.0.0` | BSD-3-Clause | https://github.com/dateutil/dateutil |
| **PyYAML** | `6.0.3` | MIT License | https://pyyaml.org/ |
| **referencing** | `0.37.0` | MIT | https://github.com/python-jsonschema/referencing |
| **rich** | `15.0.0` | MIT License | https://github.com/Textualize/rich |
| **rpds-py** | `2026.9.1` | MIT | https://github.com/crate-py/rpds |
| **sqlparse** | `0.6.1` | BSD License | https://github.com/andialbrecht/sqlparse |
| **stevedore** | `5.9.1` | Apache-2.0 | https://docs.openstack.org/stevedore |
| **typing_extensions** | `4.16.0` | PSF-2.0 | https://github.com/python/typing_extensions |
| **tzdata** | `2026.6` | Apache-2.0 | https://github.com/python/tzdata |
| **tzlocal** | `5.4.5` | MIT | https://github.com/regebro/tzlocal |
| **uritemplate** | `4.2.0` | BSD 3-Clause OR Apache-2.0 | https://uritemplate.readthedocs.org |
| **urllib3** | `2.8.0` | MIT | https://github.com/urllib3/urllib3 |
| **vine** | `5.1.0` | BSD License | https://github.com/celery/vine |
| **wcwidth** | `0.9.4` | MIT | https://github.com/jquast/wcwidth |
| **certifi** | `2026.10.23` | MPL-2.0 | https://github.com/certifi/python-certifi |

---

## 4. Development & Testing Dependencies (`requirements-dev.txt`)

Isolated from production runtime:

| Package | Version | License | Upstream Link |
| :--- | :--- | :--- | :--- |
| **bandit** | `1.9.4` | Apache-2.0 | https://bandit.readthedocs.io/ |
| **coverage** | `7.17.0` | Apache-2.0 | https://github.com/coveragepy/coveragepy |
| **playwright** | `1.64.1` | Apache-2.0 | https://github.com/Microsoft/playwright-python |
| **pytest** | `9.2.0` | MIT | https://docs.pytest.org/ |
| **pytest-cov** | `7.1.0` | MIT | https://pytest-cov.readthedocs.io/ |
| **pytest-django** | `4.14.0` | BSD License | https://github.com/pytest-dev/pytest-django |
| **ruff** | `0.17.3` | MIT | https://docs.astral.sh/ruff |
| **pip-licenses** | `5.5.5` | MIT | https://github.com/raimon49/pip-licenses |

---

## 5. Optional Production Driver (`requirements-postgres.txt`)

| Package | Version | License | Status |
| :--- | :--- | :--- | :--- |
| **psycopg2-binary** | `2.9.13` | LGPL-3.0 with exceptions | Optional. Excluded from the standard submitted CADEV 2026 build (which uses SQLite). |
