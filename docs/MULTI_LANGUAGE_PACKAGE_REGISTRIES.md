# Registres de Paquets Multi-Langages BantuDevLab (T-PKG-602)

La forge souveraine BantuDevLab prend en charge nativement les gestionnaires de paquets officiels, eliminant la dependance envers les registres publics etrangers.

---

## 1. Registre Python (PyPI / Wheels)

### Configuration `~/.pypirc` :

```ini
[distutils]
index-servers = bantudevlab

[bantudevlab]
repository = http://localhost:3002/api/packages/bantu_admin/pypi
username = bantu_admin
password = BantuAdmin2026!
```

### Publication et Installation :

```bash
# Publication avec twine
twine upload -r bantudevlab dist/*

# Installation via pip
pip install my-package --extra-index-url http://localhost:3002/api/packages/bantu_admin/pypi/simple/
```

---

## 2. Registre Node.js (npm)

### Configuration `.npmrc` :

```ini
@bantu:registry=http://localhost:3002/api/packages/bantu_admin/npm/
//localhost:3002/api/packages/bantu_admin/npm/:_authToken=1749a33d29fee921385f891d05e6cc2aa5fa97f2
```

### Publication et Installation :

```bash
npm publish
npm install @bantu/my-package
```

---

## 3. Registres Pris en Charge

| Ecosysteme | Protocole | Endpoint API |
|---|---|---|
| **Python** | PyPI | `/api/packages/<owner>/pypi` |
| **Node.js** | npm | `/api/packages/<owner>/npm` |
| **Rust** | Cargo | `/api/packages/<owner>/cargo` |
| **Java** | Maven / Gradle | `/api/packages/<owner>/maven` |
| **.NET** | NuGet | `/api/packages/<owner>/nuget` |
| **PHP** | Composer | `/api/packages/<owner>/composer` |
| **Kubernetes**| Helm | `/api/packages/<owner>/helm` |
| **Linux** | Debian / RPM | `/api/packages/<owner>/debian` |
