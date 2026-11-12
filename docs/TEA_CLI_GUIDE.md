# Guide Officiel CLI tea (Equivalent GitHub CLI gh) - T-ADM-701

Ce guide presente l'outil CLI officiel **tea** de Gitea, equivalent direct de **gh** (GitHub CLI), permettant d'interagir avec la forge souveraine directement depuis votre terminal.

---

## 1. Installation de `tea`

### Sur Linux / macOS (via gestionnaire ou binaire autonome)
```bash
# Via Homebrew
brew install tea

# Via binaire direct (architecture amd64 / arm64)
curl -sL https://dl.gitea.com/tea/latest/tea-latest-linux-amd64 -o /usr/local/bin/tea
chmod +x /usr/local/bin/tea
```

### Sur Windows (via Scoop / Choco / Winget)
```powershell
scoop install tea
# ou
choco install tea-cli
```

---

## 2. Configuration et Connexion a BantuDevLab Forge

Pour initialiser la connexion a l'instance locale ou hebergee :

```bash
tea login add \
  --name bantudevlab \
  --url http://localhost:3002 \
  --token <VOTRE_JETON_ACCES_PERSONNEL>
```

Pour verifier les comptes configures :
```bash
tea login list
```

---

## 3. Matrice de Correspondance gh vs tea

| Commande GitHub CLI (`gh`) | Commande Gitea CLI (`tea`) | Description |
|---|---|---|
| `gh auth login` | `tea login add` | Authentification a l'instance |
| `gh auth status` | `tea login check` | Verification du statut de connexion |
| `gh repo clone <repo>` | `tea repo clone <repo>` | Cloner un depot Git |
| `gh repo create <nom>` | `tea repo create --name <nom>` | Creer un nouveau depot |
| `gh repo fork` | `tea repo fork` | Creer un fork du depot |
| `gh issue list` | `tea issues ls` | Lister les tickets |
| `gh issue create` | `tea issues create` | Ouvrir un nouveau ticket |
| `gh issue view <id>` | `tea issues <id>` | Consulter le detail d'un ticket |
| `gh issue close <id>` | `tea issues close <id>` | Fermer un ticket |
| `gh pr list` | `tea pulls ls` | Lister les Pull Requests |
| `gh pr create` | `tea pulls create` | Creer une Pull Request |
| `gh pr checkout <id>` | `tea pulls checkout <id>` | Basculer sur la branche de la PR |
| `gh pr merge <id>` | `tea pulls merge <id>` | Fusionner une Pull Request |
| `gh release list` | `tea releases ls` | Lister les releases |
| `gh release create <tag>` | `tea releases create <tag>` | Creer une nouvelle release |

---

## 4. Alias de Compatibilite Transparente

Pour une transition sans friction depuis GitHub CLI, vous pouvez creer un alias shell :

### Bash / Zsh (`~/.bashrc` ou `~/.zshrc`) :
```bash
alias gh='tea'
```

### PowerShell (`$PROFILE`) :
```powershell
Set-Alias -Name gh -Value tea
```
