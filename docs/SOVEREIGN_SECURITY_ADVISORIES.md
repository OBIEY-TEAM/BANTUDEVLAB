# Guide des Avis de Securite et Signalement Confidentiel (Security Advisories)

Ce document formalise la gestion des avis de securite (Security Advisories) et le cycle de divulgation responsable des vulnerabilites sur l'infrastructure forge souveraine BantuDevLab / Gitea.

---

## 1. Principes et Cycle de Divulgation Responsable

Pour eviter toute exploitation prematuree d'une faille, le protocole suit un canal strictement prive avant publication coordonnee :

1. **Signalement prive confidentiel** : les chercheurs soumettent un avis via le canal confidentiel prive sans creer d'issue publique.
2. **Tri et confirmation** : les maintainers de securite accusent reception sous 48 heures et valident le score CVSS v3.1.
3. **Developpement du correctif en branche privee** : collaboration restreinte aux contributeurs autorises sans exposer le diff publiquement.
4. **Attribution de CVE et divulgation publique** : une fois le correctif deploye en version stable, l'avis est publie publiquement avec attribution aux decouvreurs.

---

## 2. Echelle de Severite Primer et Niveaux CVSS v3.1

| Niveau de Severite | Score CVSS v3.1 | Badge Primer | Delai Cible de Remediation |
| :--- | :--- | :--- | :--- |
| **Critical** | 9.0 - 10.0 | `.gh-severity-badge.critical` | < 24 heures |
| **High** | 7.0 - 8.9 | `.gh-severity-badge.high` | < 72 heures |
| **Medium** | 4.0 - 6.9 | `.gh-severity-badge.medium` | < 14 jours |
| **Low** | 0.1 - 3.9 | `.gh-severity-badge.low` | < 30 jours |

---

## 3. Banniere d'Avertissement Confidentielle

Tout avis prive en cours d'investigation arbore la banniere d'avertissement Primer (`.gh-confidential-banner`) rappelant le secret de l'instruction et l'interdiction de divulgation prealable.
