# Modèle de menaces (STRIDE)

Périmètre : API Django, authentification ZKP, tokens Git, webhook Gitea, scanner, assistant IA, infrastructure Docker.

## Actifs

| Actif | Valeur |
|---|---|
| Clés secrètes ZKP (côté client) | Identité du développeur |
| Clés publiques, tokens Git (hachés) | Intégrité de l'accès aux dépôts |
| Code source des dépôts | Propriété intellectuelle |
| Journal d'audit | Preuve et conformité |
| Secrets d'infrastructure | Contrôle total du système |

## Menaces et mesures

| # | Catégorie | Menace | Mesure en place | Risque résiduel |
|---|---|---|---|---|
| 1 | Spoofing | Rejeu d'une preuve ZKP | Nonce à usage unique, consommation atomique, expiration 5 min, y compris pour les tokens Git | Faible |
| 2 | Spoofing | Énumération d'utilisateurs | Réponse uniforme au défi, throttle 5/min | Faible (timing à mesurer) |
| 3 | Spoofing | Webhook falsifié | HMAC-SHA256, comparaison en temps constant, désactivé sans secret | Faible |
| 4 | Tampering | Clé publique malveillante (petit sous-groupe) | `validate_public_key` (y^q = 1) | Faible |
| 5 | Tampering | Altération du journal d'audit | Chaîne de hachage, insertion transactionnelle, vérification par lots | Moyen (pas d'ancrage externe) |
| 6 | Repudiation | Action non traçable | `AuditTrail` (scan, dépôt, auth) | Faible |
| 7 | Information disclosure | Secrets en base via l'IA | Masquage avant persistance | Moyen (regex, pas d'entropie) |
| 8 | Information disclosure | Détail d'erreur interne | Messages génériques, pas de `str(e)` | Faible |
| 9 | Information disclosure | PostgreSQL/Redis exposés | Réseau `internal`, mots de passe obligatoires | Faible |
| 10 | Denial of service | Inscription/scan/IA en masse | Throttles par portée, limites de taille (1 Mo global, 20 Ko IA) | Moyen (pas de WAF) |
| 11 | Denial of service | Gitea indisponible | Timeouts, circuit breaker, cache 60 s | Faible |
| 12 | Elevation of privilege | Route sensible anonyme | `IsAuthenticated` par défaut, `IsAdminUser` pour la création d'organisations | Faible |
| 13 | Elevation of privilege | Token Git surdimensionné | `permissions` restreintes, durée 1-365 j | Faible |
| 14 | Elevation of privilege | Conteneur compromis | non-root, `no-new-privileges`, `cap_drop: ALL` | Moyen |
| 15 | Injection | XSS via messages UI | Toasts en `textContent`, CSP | Moyen (CSP autorise encore `unsafe-inline`, voir T-040) |
| 16 | Injection | Prompt injection vers Gemma | Taille limitée, sorties non exécutées | Moyen |
| 17 | SSRF | Redirection vers hôte interne via Gitea | `allow_redirects=False`, validation `owner/repo` | Faible |

## Points ouverts (backlog)

- CSP stricte sans `unsafe-inline` (T-040) : nécessite d'externaliser le JavaScript des gabarits.
- Preuve de possession de clé à l'inscription (T-032) et dérivation de clé robuste (T-033).
- Verrouillage progressif des comptes (T-035), récupération d'identité (T-055).
- Audit cryptographique externe (T-036).
