# Registre de Conteneurs OCI Souverain BantuDevLab (Equivalent ghcr.io) - T-PKG-601

Ce guide presente l'utilisation du registre de conteneurs OCI / Docker integre a la forge BantuDevLab, offrant une alternative souveraine et auto-hebergee a GitHub Container Registry (`ghcr.io`).

---

## 1. Connexion au Registre Souverain

Identifiez-vous au registre local ou distant a l'aide de vos identifiants ou d'un jeton d'acces personnel (Personal Access Token) :

```bash
docker login localhost:3002
# Nom d'utilisateur : bantu_admin
# Mot de passe : BantuAdmin2026! (ou votre PAT)
```

---

## 2. Construction et Marquage (Tagging) de l'Image

Associez l'image a l'espace de nommage de votre organisation ou utilisateur Gitea :

```bash
# Exemple pour le projet bantudevlab
docker build -t localhost:3002/bantu_admin/sovereign-app:1.0.0 .
docker tag localhost:3002/bantu_admin/sovereign-app:1.0.0 localhost:3002/bantu_admin/sovereign-app:latest
```

---

## 3. Publication (Push) vers le Registre

Envoyez l'image OCI sur la forge :

```bash
docker push localhost:3002/bantu_admin/sovereign-app:1.0.0
docker push localhost:3002/bantu_admin/sovereign-app:latest
```

Une fois publiee, l'image apparait directement dans l'onglet **Paquets** du depot et du profil utilisateur.

---

## 4. Deploiement Automatique via Gitea Actions / GitHub Actions

Dans votre fichier `.github/workflows/deploy.yml` ou `.gitea/workflows/deploy.yaml` :

```yaml
name: Build and Push OCI Image
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Log in to Sovereign Registry
        run: echo "${{ secrets.GITEA_TOKEN }}" | docker login localhost:3002 -u ${{ gitea.actor }} --password-stdin
      - name: Build & Push
        run: |
          docker build -t localhost:3002/${{ gitea.repository }}:latest .
          docker push localhost:3002/${{ gitea.repository }}:latest
```
