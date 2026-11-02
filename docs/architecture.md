# Architecture

## Contexte (C4 niveau 1)

```mermaid
flowchart TB
    Dev["Développeur africain"]
    Admin["Administrateur d'organisation"]
    Forge["BANTUDEVLAB<br/>Forge souveraine"]
    Gemma["Gemma 5B local"]
    Dev -->|"identité ZKP, git, audits"| Forge
    Admin -->|"organisations, tokens"| Forge
    Forge --> Gemma
```

## Conteneurs (C4 niveau 2)

```mermaid
flowchart LR
    subgraph sovereign_net
        Django["django_app<br/>Gunicorn + Uvicorn"]
        Gitea["gitea"]
        Celery["celery_worker"]
    end
    subgraph backend_net["backend_net (interne)"]
        PG[("PostgreSQL")]
        Redis[("Redis")]
    end
    Django --> PG
    Django --> Redis
    Celery --> Redis
    Celery --> PG
    Gitea --> PG
    Django -->|"REST + webhooks HMAC"| Gitea
```

## Composants Django

| Application | Responsabilité |
|---|---|
| `apps.core` | Pages, organisations multi-tenant, journal d'audit chaîné, santé, icônes |
| `apps.zkp_auth` | Identités souveraines, défis, preuves de Schnorr, tokens Git |
| `apps.gitea_client` | Client Gitea (circuit breaker, cache), webhook, synchronisation |
| `apps.security_scanner` | Analyse statique, score de souveraineté, export SARIF |
| `apps.ai_assistant` | Revue de code Gemma (JSON ou SSE), journalisation sans secrets |

## Flux d'authentification

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Serveur
    C->>S: POST /api/zkp/challenge/ (username)
    S-->>C: nonce à usage unique (5 min)
    C->>C: preuve (t, s) = Schnorr(x, nonce)
    C->>S: POST /api/zkp/verify/ (nonce, t, s)
    S->>S: consomme le nonce (atomique) puis vérifie g^s * y^c = t
    S-->>C: session ou 401
```

## Décisions d'architecture (ADR)

### ADR-001 - Gitea comme moteur Git, surcouche Django
- **Contexte** : écrire un moteur Git est hors de portée ; Gitea est open source, léger et auto-hébergeable.
- **Décision** : Gitea gère les dépôts ; Django ajoute identité ZKP, audit, scanner et IA.
- **Conséquences** : couplage par API REST et webhooks (signés) ; circuit breaker pour la résilience.

### ADR-002 - ZKP de Schnorr (Fiat-Shamir) pour l'identité
- **Décision** : aucune donnée secrète ne transite ; le serveur stocke uniquement `y = g^x mod p`.
- **Conséquences** : pas de mot de passe à voler ; perte de la clé = perte du compte (récupération à concevoir, voir backlog T-055). Voir [crypto-spec](security/crypto-spec.md).

### ADR-003 - IA locale (Gemma 5B)
- **Décision** : inférence sur l'infrastructure souveraine (Ollama/vLLM) ; repli par règles hors ligne.
- **Conséquences** : le code ne quitte pas la juridiction ; secrets masqués avant journalisation.

### ADR-004 - Sécurité par défaut
- **Décision** : `IsAuthenticated` par défaut, aucun secret par défaut, `DEBUG=False`, réseau Docker interne pour les données.
- **Conséquences** : toute nouvelle route publique doit être déclarée et justifiée en revue.

### ADR-005 - Icônes SVG auto-hébergées
- **Décision** : balises `{% icon %}`/`{% flag %}` rendant du SVG en ligne ; aucun emoji ni CDN.
- **Conséquences** : rendu identique sur tous les systèmes (les drapeaux emoji ne s'affichent pas sous Windows), compatible CSP stricte.
