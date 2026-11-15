"""Generate CADEV 2026 pitch + live demo navigation videos (FR & EN).

Features:
- Audio-reactive talking presenter in front of Pointe-Noire CFCO railway station
- African developer & cybersecurity scenes + BantuDevLab logo watermark
- Real live demo navigation screenshots from cybersocle.site & git.cybersocle.site
- Smooth Ken Burns motion, crossfade transitions, lower-thirds, progress bar, and subtitles
"""

import asyncio
import json
import os
from pathlib import Path
from typing import List

import edge_tts
import numpy as np
from moviepy import AudioFileClip, CompositeVideoClip, ImageClip, VideoClip, concatenate_videoclips, vfx
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DEMO_DIR = ASSETS_DIR / "demo"
OUTPUT_DIR = BASE_DIR / "output"
TMP_DIR = BASE_DIR / "tmp"

WIDTH, HEIGHT = 1280, 720
FPS = 24

LOGO_PATH = ASSETS_DIR / "logo_bantudevlab.png"
SCENE_PRESENTER = ASSETS_DIR / "scene_presenter_gare.jpg"
SCENE_PRESENTER_TALK = ASSETS_DIR / "scene_presenter_gare_talk.jpg"
SCENE_DEVS = ASSETS_DIR / "scene_devs_collab.jpg"
SCENE_CYBER = ASSETS_DIR / "scene_cyber_sast.jpg"
SCENE_LAUNCH = ASSETS_DIR / "scene_launch_team.jpg"

DEMO_HOME = DEMO_DIR / "demo_01_home.png"
DEMO_KISWAHILI = DEMO_DIR / "demo_02_kiswahili.png"
DEMO_ZKP = DEMO_DIR / "demo_03_zkp_login.png"
DEMO_DASHBOARD = DEMO_DIR / "demo_04_dashboard.png"
DEMO_SAST = DEMO_DIR / "demo_05_sast_audit.png"
DEMO_GEMMA = DEMO_DIR / "demo_05_gemma_ai.png"
DEMO_FAQ = DEMO_DIR / "demo_06_faq.png"
DEMO_METRICS = DEMO_DIR / "demo_07_metrics.png"
DEMO_LATENCY = DEMO_DIR / "demo_07_latency.png"
DEMO_GITEA = DEMO_DIR / "demo_08_gitea.png"


SCENES_SPEC = {
    "fr": {
        "voice": "fr-FR-VivienneMultilingualNeural",
        "output": OUTPUT_DIR / "BANTUDEVLAB_CADEV26_FR.mp4",
        "intro_title": "BANTUDEVLAB",
        "intro_sub": "Forge Logicielle Souveraine Panafricaine — Pitch & Démo CADEV 2026",
        "outro_sub": "cybersocle.site  |  git.cybersocle.site  |  Équipe CYBERSOCLE — Pointe-Noire",
        "segments": [
            {
                "id": "fr_01_accroche",
                "image": SCENE_PRESENTER,
                "talk_image": SCENE_PRESENTER_TALK,
                "badge": "Pointe-Noire, Congo  |  Équipe CYBERSOCLE",
                "headline": "Alicia Syrianne Mampouya — Le Paradoxe Numérique Africain",
                "text": (
                    "Excellents membres du jury, bonjour depuis la gare de Pointe-Noire. "
                    "À cet instant précis, des milliers de développeurs africains conçoivent les systèmes bancaires, "
                    "les infrastructures d'énergie et les services publics du continent. "
                    "Mais aujourd'hui, ce patrimoine stratégique réside à huit mille kilomètres d'ici, "
                    "soumis à des juridictions étrangères et analysé par des intelligences artificielles externes."
                ),
            },
            {
                "id": "fr_02_identite",
                "image": SCENE_PRESENTER,
                "talk_image": SCENE_PRESENTER_TALK,
                "badge": "BANTUDEVLAB  |  Par les devs, pour les devs",
                "headline": "Une forge logicielle panafricaine souveraine",
                "text": (
                    "Je m'appelle Alicia Syrianne Mampouya, membre de l'équipe CYBERSOCLE, "
                    "aux côtés de notre capitaine et architecte Christ Dany Obiey. "
                    "Nous avons refusé cette dépendance. Voici BantuDevLab : "
                    "une forge logicielle panafricaine souveraine, conçue par des développeurs africains, "
                    "pour les développeurs africains, alignée sur la Convention de Malabo."
                ),
            },
            {
                "id": "fr_03_probleme",
                "image": SCENE_DEVS,
                "badge": "Constats  |  Triple Rupture Technologique",
                "headline": "Extraterritorialité • Mots de passe • Fuite vers l'IA Cloud",
                "text": (
                    "Notre dépendance aux plateformes étrangères engendre trois ruptures critiques : "
                    "l'extraterritorialité de nos dépôts et secrets industriels, "
                    "la vulnérabilité des mots de passe et jetons transmis en clair sur les réseaux, "
                    "et la fuite de notre propriété intellectuelle vers des assistants d'IA hébergés hors d'Afrique."
                ),
            },
            {
                "id": "fr_04_piliers",
                "image": SCENE_CYBER,
                "badge": "Architecture  |  Souveraineté & Zero-Trust ZKP",
                "headline": "Docker • Gitea CE • Preuve de Schnorr RFC 3526 (2048 bits)",
                "text": (
                    "BantuDevLab répond par une architecture industrielle conteneurisée avec Gitea, Valkey, PostgreSQL "
                    "et un journal d'audit SHA-256 immuable. "
                    "L'authentification élimine les mots de passe grâce aux preuves à divulgation nulle de Schnorr 2048 bits : "
                    "le navigateur prouve son secret sans jamais le transmettre au serveur."
                ),
            },
            {
                "id": "fr_05_ia_sast",
                "image": SCENE_CYBER,
                "badge": "Sécurité & IA Locale  |  Zéro Fuite de Données",
                "headline": "Entropie de Shannon • Export SARIF 2.1.0 • Ollama Gemma 2 2B",
                "text": (
                    "Notre scanner SAST calcule l'entropie de Shannon pour bloquer les clés secrètes enfouies, "
                    "exporte des rapports OASIS SARIF 2.1.0 pour la CI/CD, "
                    "et exécute localement le modèle Google Gemma 2 2B via Ollama "
                    "pour auditer le code sans qu'aucune ligne ne quitte notre infrastructure."
                ),
            },
            {
                "id": "fr_06_demo_home",
                "image": DEMO_HOME,
                "is_demo": True,
                "badge": "DÉMO LIVE (1/7)  |  https://cybersocle.site/",
                "headline": "Portail Souverain : Interface Primer auto-hébergée sans CDN externe",
                "text": (
                    "Passons à la démonstration en direct sur cybersocle point site. "
                    "Sur la page d'accueil, l'interface Primer est entièrement auto-hébergée sans aucun CDN étranger. "
                    "On retrouve immédiatement le score de souveraineté numérique et la télémétrie des nœuds."
                ),
            },
            {
                "id": "fr_07_demo_i18n",
                "image": DEMO_KISWAHILI,
                "is_demo": True,
                "badge": "DÉMO LIVE (2/7)  |  Multilingue & Thème Synchronisé",
                "headline": "Français, Anglais, Kiswahili, Portugais & Bascule Sombre/Clair",
                "text": (
                    "BantuDevLab parle aux développeurs de tout le continent en français, anglais, kiswahili et portugais, "
                    "avec synchronisation bidirectionnelle du thème sombre et clair sans flash blanc entre le portail et Gitea."
                ),
            },
            {
                "id": "fr_08_demo_zkp",
                "image": DEMO_ZKP,
                "is_demo": True,
                "badge": "DÉMO LIVE (3/7)  |  Connexion Zero-Trust 1-Clic",
                "headline": "Vérification cryptographique Schnorr réussie sans mot de passe",
                "text": (
                    "Dans le module de connexion Zero-Trust, le compte évaluateur cadev_evaluator génère localement "
                    "son engagement et sa réponse Fiat-Shamir. En quelques millisecondes, le serveur valide la preuve mathématique "
                    "sans jamais connaître ni stocker aucun mot de passe."
                ),
            },
            {
                "id": "fr_09_demo_dashboard",
                "image": DEMO_DASHBOARD,
                "is_demo": True,
                "badge": "DÉMO LIVE (4/7)  |  Tableau de Bord Souverain",
                "headline": "Centre de contrôle, dépôts actifs et actions rapides",
                "text": (
                    "Une fois authentifié, l'évaluateur accède au tableau de bord souverain. "
                    "Il visualise la latence des nœuds, gère ses dépôts de démonstration et lance directement "
                    "les analyses de sécurité depuis le Workbench intégré."
                ),
            },
            {
                "id": "fr_10_demo_sast",
                "image": DEMO_SAST,
                "is_demo": True,
                "badge": "DÉMO LIVE (5/7)  |  Scanner SAST & Entropie de Shannon",
                "headline": "Détection instantanée de secrets (H = 4,29) et d'injections SQL",
                "text": (
                    "En soumettant un extrait de code vulnérable dans le Workbench, le scanner SAST détecte immédiatement "
                    "les clés API codées en dur grâce à l'entropie de Shannon, signale les injections SQL "
                    "et génère un rapport structuré prêt pour l'export SARIF."
                ),
            },
            {
                "id": "fr_11_demo_gemma",
                "image": DEMO_GEMMA,
                "is_demo": True,
                "badge": "DÉMO LIVE (6/7)  |  Revue de Code IA Locale Gemma 2 2B",
                "headline": "Audit et correction de sécurité hors-ligne via Ollama",
                "text": (
                    "En un clic sur la revue IA, notre modèle local Gemma 2 2B quantifié en 4 bits analyse les failles "
                    "et propose des correctifs précis en temps réel, tout en garantissant que zéro octet de code "
                    "ne traverse les frontières."
                ),
            },
            {
                "id": "fr_12_demo_metrics_gitea",
                "image": DEMO_METRICS,
                "is_demo": True,
                "badge": "DÉMO LIVE (7/7)  |  Topologie Panafricaine & Forge Gitea CE",
                "headline": "Carte cible (Abidjan, Dakar, Lagos, Nairobi, Kigali) & git.cybersocle.site",
                "text": (
                    "Enfin, la page de métriques mesure la latence directe du serveur actif et présente notre topologie cible "
                    "panafricaine. Côté forge sur git point cybersocle point site, Gitea CE offre une expérience complète "
                    "avec boutons d'audit SAST et revue Gemma intégrés."
                ),
            },
            {
                "id": "fr_13_traction",
                "image": SCENE_LAUNCH,
                "badge": "Traction & Conformité  |  CADEV 2026",
                "headline": "325 Commits • 202 Tests (95,65 %) • 63/63 Licences Permissives",
                "text": (
                    "BantuDevLab n'est pas un concept : c'est une forge opérationnelle forte de trois cent vingt-cinq commits, "
                    "deux cent deux tests automatisés à quatre-vingt-quinze virgule soixante-cinq pour cent de couverture, "
                    "et soixante-trois dépendances vérifiées sous licences permissives, avec des domaines acquis chez Systalink Datacloud."
                ),
            },
            {
                "id": "fr_14_conclusion",
                "image": SCENE_PRESENTER,
                "talk_image": SCENE_PRESENTER_TALK,
                "badge": "Souveraineté Numérique  |  Équipe CYBERSOCLE",
                "headline": "Construisons notre autonomie technologique depuis Pointe-Noire",
                "text": (
                    "L'Afrique doit posséder ses forges, ses clés cryptographiques et son intelligence artificielle. "
                    "BantuDevLab est prêt, sécurisé et accessible dès maintenant sur cybersocle point site. "
                    "Merci pour votre attention."
                ),
            },
        ],
    },
    "en": {
        "voice": "en-NG-EzinneNeural",
        "output": OUTPUT_DIR / "BANTUDEVLAB_CADEV26_EN.mp4",
        "intro_title": "BANTUDEVLAB",
        "intro_sub": "Pan-African Sovereign Software Forge — CADEV 2026 Pitch & Live Demo",
        "outro_sub": "cybersocle.site  |  git.cybersocle.site  |  CYBERSOCLE Team — Pointe-Noire",
        "segments": [
            {
                "id": "en_01_hook",
                "image": SCENE_PRESENTER,
                "talk_image": SCENE_PRESENTER_TALK,
                "badge": "Pointe-Noire, Congo  |  CYBERSOCLE Team",
                "headline": "Alicia Syrianne Mampouya — Africa's Digital Sovereignty Paradox",
                "text": (
                    "Distinguished members of the jury, greetings from Pointe-Noire railway station. "
                    "At this very moment, thousands of African developers are building our continent's banking systems, "
                    "energy grids, and public digital services. "
                    "Yet today, that strategic source code lives eight thousand kilometers away, "
                    "subject to foreign jurisdictions and analyzed by external cloud AI models."
                ),
            },
            {
                "id": "en_02_identity",
                "image": SCENE_PRESENTER,
                "talk_image": SCENE_PRESENTER_TALK,
                "badge": "BANTUDEVLAB  |  By Devs, For Devs",
                "headline": "A Pan-African Sovereign Software Forge",
                "text": (
                    "I am Alicia Syrianne Mampouya from Team CYBERSOCLE, "
                    "alongside our captain and lead architect Christ Dany Obiey. "
                    "We refused this dependency. Meet BantuDevLab: "
                    "a sovereign Pan-African software forge built by African developers, for African developers, "
                    "aligned with the African Union Malabo Convention."
                ),
            },
            {
                "id": "en_03_problem",
                "image": SCENE_DEVS,
                "badge": "The Challenge  |  Three Critical Gaps",
                "headline": "Extraterritoriality • Password Risk • Cloud AI Data Leaks",
                "text": (
                    "Reliance on foreign hosting platforms creates three critical risks: "
                    "extraterritorial exposure of our repositories and trade secrets, "
                    "password and token interception across public networks, "
                    "and intellectual property leakage whenever proprietary code is sent to external AI assistants."
                ),
            },
            {
                "id": "en_04_pillars",
                "image": SCENE_CYBER,
                "badge": "Architecture  |  Sovereignty & Zero-Trust ZKP",
                "headline": "Docker • Gitea CE • 2048-bit Schnorr ZKP (RFC 3526)",
                "text": (
                    "BantuDevLab solves this with an autonomous containerized stack powered by Gitea, Valkey, PostgreSQL, "
                    "and an immutable SHA-256 audit log. "
                    "Our Zero-Trust authentication eliminates passwords using 2048-bit Schnorr Zero-Knowledge Proofs: "
                    "your browser proves ownership of its secret without ever transmitting it to the server."
                ),
            },
            {
                "id": "en_05_ai_sast",
                "image": SCENE_CYBER,
                "badge": "Security & Local AI  |  Zero Telemetry Leakage",
                "headline": "Shannon Entropy • OASIS SARIF 2.1.0 • Ollama Gemma 2 2B",
                "text": (
                    "Our built-in SAST scanner computes Shannon entropy to catch leaked secrets, "
                    "exports industry-standard OASIS SARIF 2.1.0 reports for CI/CD pipelines, "
                    "and runs Google Gemma 2 2B locally via Ollama for code reviews "
                    "without a single line of code leaving our infrastructure."
                ),
            },
            {
                "id": "en_06_demo_home",
                "image": DEMO_HOME,
                "is_demo": True,
                "badge": "LIVE DEMO (1/7)  |  https://cybersocle.site/",
                "headline": "Sovereign Portal: Self-Hosted Primer UI with Zero External CDNs",
                "text": (
                    "Let us walk through the live demo at cybersocle dot site. "
                    "On the landing page, the Primer interface is completely self-hosted with zero external CDNs. "
                    "Evaluators immediately see the digital sovereignty score and real-time node telemetry."
                ),
            },
            {
                "id": "en_07_demo_i18n",
                "image": DEMO_KISWAHILI,
                "is_demo": True,
                "badge": "LIVE DEMO (2/7)  |  Multilingual & Theme Sync",
                "headline": "English, French, Kiswahili, Portuguese & Dark/Light Theme Sync",
                "text": (
                    "BantuDevLab speaks to developers across the continent in English, French, Kiswahili, and Portuguese, "
                    "with seamless bidirectional Dark and Light theme synchronization and zero white flash between the portal and Gitea."
                ),
            },
            {
                "id": "en_08_demo_zkp",
                "image": DEMO_ZKP,
                "is_demo": True,
                "badge": "LIVE DEMO (3/7)  |  1-Click Zero-Trust ZKP Login",
                "headline": "Passwordless Schnorr Cryptographic Verification Passed",
                "text": (
                    "In the Zero-Trust login module, the cadev_evaluator account locally computes its cryptographic commitment "
                    "and Fiat-Shamir response. Within milliseconds, the server verifies the mathematical proof "
                    "without ever seeing or storing a password."
                ),
            },
            {
                "id": "en_09_demo_dashboard",
                "image": DEMO_DASHBOARD,
                "is_demo": True,
                "badge": "LIVE DEMO (4/7)  |  Sovereign Control Center",
                "headline": "Node Monitoring, Active Repositories & Fast Actions",
                "text": (
                    "Once authenticated, the evaluator lands on the sovereign dashboard "
                    "to monitor node latency, inspect repositories, and launch security audits directly from the integrated workbench."
                ),
            },
            {
                "id": "en_10_demo_sast",
                "image": DEMO_SAST,
                "is_demo": True,
                "badge": "LIVE DEMO (5/7)  |  SAST Scanner & Shannon Entropy",
                "headline": "Instant Secret Detection (H = 4.29) & SQL Injection Alerts",
                "text": (
                    "When pasting vulnerable code into the workbench, the SAST engine immediately catches hardcoded API keys "
                    "using Shannon entropy, flags SQL injection patterns, and prepares an OASIS SARIF report."
                ),
            },
            {
                "id": "en_11_demo_gemma",
                "image": DEMO_GEMMA,
                "is_demo": True,
                "badge": "LIVE DEMO (6/7)  |  Local Gemma 2 2B AI Code Review",
                "headline": "Offline Security Remediation via Local Ollama Inference",
                "text": (
                    "With one click on Ask Gemma Review, our 4-bit quantized Gemma 2 2B model analyzes the vulnerabilities locally "
                    "and streams actionable security patches with zero external cloud data egress."
                ),
            },
            {
                "id": "en_12_demo_metrics_gitea",
                "image": DEMO_GITEA,
                "is_demo": True,
                "badge": "LIVE DEMO (7/7)  |  Gitea CE Forge & Pan-African Metrics",
                "headline": "git.cybersocle.site & Target Nodes (Dakar, Abidjan, Lagos, Nairobi, Kigali)",
                "text": (
                    "Finally, our sovereignty metrics page benchmarks live server latency and maps our target Pan-African topology. "
                    "Inside Gitea CE at git dot cybersocle dot site, developers enjoy a full Git forge with integrated SAST and Gemma review buttons."
                ),
            },
            {
                "id": "en_13_traction",
                "image": SCENE_LAUNCH,
                "badge": "Engineering Proof  |  CADEV 2026 Compliance",
                "headline": "325 Commits • 202 Tests (95.65% Coverage) • 63/63 Permissive Licenses",
                "text": (
                    "BantuDevLab is production-ready: three hundred and twenty-five engineering commits, "
                    "two hundred and two automated tests with ninety-five point sixty-five percent coverage, "
                    "sixty-three verified permissive dependencies, and domains acquired through Systalink Datacloud."
                ),
            },
            {
                "id": "en_14_closing",
                "image": SCENE_PRESENTER,
                "talk_image": SCENE_PRESENTER_TALK,
                "badge": "Digital Sovereignty  |  CYBERSOCLE Team",
                "headline": "Building Africa's Technological Autonomy from Pointe-Noire",
                "text": (
                    "Africa must own its software forges, its cryptographic keys, and its artificial intelligence. "
                    "BantuDevLab is ready, secure, and live today at cybersocle dot site. "
                    "Thank you for your attention."
                ),
            },
        ],
    },
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load a clean Windows sans-serif font with fallback."""
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    """Wrap text into lines that fit within max_width pixels."""
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_cover_image(img_path: Path) -> Image.Image:
    """Resize and center-crop an image to exact 1280x720 RGBA."""
    bg = Image.open(img_path).convert("RGBA")
    bg_ratio = bg.width / bg.height
    target_ratio = WIDTH / HEIGHT
    if bg_ratio > target_ratio:
        new_h = HEIGHT
        new_w = int(new_h * bg_ratio)
    else:
        new_w = WIDTH
        new_h = int(new_w / bg_ratio)
    bg = bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - WIDTH) // 2
    top = (new_h - HEIGHT) // 2
    return bg.crop((left, top, left + WIDTH, top + HEIGHT))


def compose_overlay(badge: str, headline: str, subtitle: str, progress: float, is_demo: bool = False) -> Image.Image:
    """Create transparent 1280x720 RGBA overlay with logo, badge, lower-third, subtitles, and progress bar."""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    # Bottom gradient for readability (lighter for demo screenshots so UI stays visible)
    grad_height = 225 if is_demo else 255
    max_alpha = 205 if is_demo else 220
    for y in range(HEIGHT - grad_height, HEIGHT):
        alpha = int(max_alpha * ((y - (HEIGHT - grad_height)) / grad_height) ** 1.15)
        ov_draw.line([(0, y), (WIDTH, y)], fill=(8, 13, 24, alpha))

    # Top-left pill badge
    badge_color = (245, 166, 35, 230) if is_demo else (0, 212, 255, 200)
    ov_draw.rounded_rectangle([(28, 22), (620, 62)], radius=12, fill=(10, 18, 34, 225), outline=badge_color, width=2)

    # Lower-third accent bar & headline box
    ov_draw.rounded_rectangle([(28, HEIGHT - 188), (WIDTH - 28, HEIGHT - 130)], radius=10, fill=(10, 18, 34, 228), outline=(0, 212, 255, 165), width=2)
    ov_draw.rectangle([(28, HEIGHT - 188), (38, HEIGHT - 130)], fill=(245, 166, 35, 255))

    # Subtitle box
    ov_draw.rounded_rectangle([(28, HEIGHT - 120), (WIDTH - 28, HEIGHT - 22)], radius=10, fill=(8, 13, 24, 238), outline=(255, 255, 255, 45), width=1)

    # Bottom progress bar
    ov_draw.rectangle([(0, HEIGHT - 6), (WIDTH, HEIGHT)], fill=(20, 30, 50, 200))
    bar_w = max(8, int(WIDTH * min(max(progress, 0.0), 1.0)))
    ov_draw.rectangle([(0, HEIGHT - 6), (bar_w, HEIGHT)], fill=(0, 212, 255, 255))
    ov_draw.rectangle([(max(0, bar_w - 28), HEIGHT - 6), (bar_w, HEIGHT)], fill=(245, 166, 35, 255))

    # Top-right BantuDevLab logo
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo.thumbnail((108, 108), Image.Resampling.LANCZOS)
        overlay.paste(logo, (WIDTH - logo.width - 24, 16), logo)

    font_badge = load_font(18, bold=True)
    font_head = load_font(23, bold=True)
    font_sub = load_font(20, bold=False)

    badge_text_color = (255, 205, 86, 255) if is_demo else (0, 229, 255, 255)
    ov_draw.text((44, 30), badge, font=font_badge, fill=badge_text_color)
    ov_draw.text((52, HEIGHT - 173), headline, font=font_head, fill=(255, 255, 255, 255))

    lines = wrap_text(ov_draw, subtitle, font_sub, WIDTH - 96)[:3]
    y_text = HEIGHT - 110
    for line in lines:
        ov_draw.text((46, y_text), line, font=font_sub, fill=(230, 238, 250, 255))
        y_text += 27

    return overlay


def prepare_static_frame(bg_path: Path, badge: str, headline: str, subtitle: str, progress: float, is_demo: bool, out_path: Path) -> Path:
    """Compose a static 1280x720 frame for non-talking scenes."""
    canvas = fit_cover_image(bg_path)
    overlay = compose_overlay(badge, headline, subtitle, progress, is_demo=is_demo)
    canvas = Image.alpha_composite(canvas, overlay)
    canvas.convert("RGB").save(out_path, quality=93)
    return out_path


def compute_audio_envelope(audio_clip: AudioFileClip, duration: float, fps: int = FPS) -> np.ndarray:
    """Compute normalized per-frame RMS speech amplitude in [0, 1] for lip-sync blending."""
    n_frames = max(1, int(np.ceil(duration * fps)))
    try:
        samples = audio_clip.to_soundarray(fps=16000)
        if samples.ndim == 2:
            mono = samples.mean(axis=1)
        else:
            mono = samples
        samples_per_frame = max(1, int(16000 / fps))
        env = np.zeros(n_frames, dtype=np.float32)
        for i in range(n_frames):
            start = i * samples_per_frame
            end = min(len(mono), start + samples_per_frame)
            if start < len(mono):
                chunk = mono[start:end]
                env[i] = float(np.sqrt(np.mean(chunk * chunk)))
        peak = float(np.percentile(env, 95)) if len(env) else 1.0
        peak = max(peak, 1e-4)
        env = np.clip(env / peak, 0.0, 1.0)
        # Smooth slightly to avoid jitter while preserving syllable cadence
        kernel = np.array([0.25, 0.5, 0.25], dtype=np.float32)
        env = np.convolve(env, kernel, mode="same")
        return np.clip(env, 0.0, 1.0)
    except Exception:
        return np.zeros(n_frames, dtype=np.float32)


def make_talking_presenter_clip(
    closed_path: Path,
    talk_path: Path,
    audio_clip: AudioFileClip,
    duration: float,
    badge: str,
    headline: str,
    subtitle: str,
    progress: float,
) -> VideoClip:
    """Create an audio-reactive talking-presenter clip with subtle zoom and full overlay."""
    closed_arr = np.array(fit_cover_image(closed_path).convert("RGB"), dtype=np.float32)
    talk_arr = np.array(fit_cover_image(talk_path).convert("RGB"), dtype=np.float32)
    overlay_img = compose_overlay(badge, headline, subtitle, progress, is_demo=False)
    ov_arr = np.array(overlay_img, dtype=np.float32)
    ov_alpha = ov_arr[:, :, 3:4] / 255.0
    ov_rgb = ov_arr[:, :, :3]

    env = compute_audio_envelope(audio_clip, duration, FPS)

    def make_frame(t: float) -> np.ndarray:
        idx = min(int(t * FPS), len(env) - 1)
        w = float(env[idx])
        blended = closed_arr * (1.0 - w) + talk_arr * w
        # Subtle breathing/zoom motion on the presenter background
        zoom = 1.0 + 0.025 * (t / max(duration, 0.1))
        if zoom > 1.001:
            pil_bg = Image.fromarray(blended.astype(np.uint8))
            zw, zh = int(WIDTH * zoom), int(HEIGHT * zoom)
            pil_bg = pil_bg.resize((zw, zh), Image.Resampling.BILINEAR)
            lx = (zw - WIDTH) // 2
            ty = (zh - HEIGHT) // 2
            blended = np.array(pil_bg.crop((lx, ty, lx + WIDTH, ty + HEIGHT)), dtype=np.float32)
        composited = blended * (1.0 - ov_alpha) + ov_rgb * ov_alpha
        return np.clip(composited, 0, 255).astype(np.uint8)

    return VideoClip(make_frame, duration=duration).with_fps(FPS)


def create_brand_card(title: str, subtitle: str, out_path: Path) -> Path:
    """Create a 1280x720 cyber-sovereign intro/outro card with BantuDevLab logo."""
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), (9, 15, 28, 255))
    draw = ImageDraw.Draw(canvas)

    for x in range(0, WIDTH, 64):
        draw.line([(x, 0), (x, HEIGHT)], fill=(0, 212, 255, 24), width=1)
    for y in range(0, HEIGHT, 64):
        draw.line([(0, y), (WIDTH, y)], fill=(0, 212, 255, 24), width=1)

    # Gold & cyan top accent strip
    draw.rectangle([(0, 0), (WIDTH, 6)], fill=(0, 212, 255, 255))
    draw.rectangle([(0, 0), (WIDTH // 3, 6)], fill=(245, 166, 35, 255))

    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo.thumbnail((250, 250), Image.Resampling.LANCZOS)
        canvas.paste(logo, ((WIDTH - logo.width) // 2, 125), logo)

    font_title = load_font(56, bold=True)
    font_sub = load_font(24, bold=False)

    tb = draw.textbbox((0, 0), title, font=font_title)
    draw.text(((WIDTH - (tb[2] - tb[0])) // 2, 405), title, font=font_title, fill=(255, 255, 255, 255))

    sb = draw.textbbox((0, 0), subtitle, font=font_sub)
    draw.text(((WIDTH - (sb[2] - sb[0])) // 2, 485), subtitle, font=font_sub, fill=(0, 229, 255, 255))

    canvas.convert("RGB").save(out_path, quality=93)
    return out_path


async def synthesize_voice(text: str, voice: str, out_mp3: Path) -> None:
    """Synthesize female speech audio using Edge neural TTS."""
    communicate = edge_tts.Communicate(text, voice, rate="+3%")
    await communicate.save(str(out_mp3))


def make_ken_burns_clip(image_path: Path, duration: float, zoom_in: bool = True) -> ImageClip:
    """Create a smooth Ken Burns zoom clip."""
    base_clip = ImageClip(str(image_path)).with_duration(duration)
    if zoom_in:
        return base_clip.resized(lambda t: 1.0 + 0.045 * (t / max(duration, 0.1))).with_position("center")
    return base_clip.resized(lambda t: 1.045 - 0.045 * (t / max(duration, 0.1))).with_position("center")


async def build_language_video(lang_code: str, spec: dict) -> Path:
    """Synthesize audio, compose animated scenes + talking presenter + demo navigation, and export MP4."""
    lang_tmp = TMP_DIR / lang_code
    lang_tmp.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    clips = []
    intro_img = create_brand_card(spec["intro_title"], spec["intro_sub"], lang_tmp / "intro.png")
    intro_clip = (
        ImageClip(str(intro_img))
        .with_duration(3.0)
        .with_effects([vfx.FadeIn(0.6), vfx.FadeOut(0.45)])
    )
    clips.append(intro_clip)

    total_segs = len(spec["segments"])
    for idx, seg in enumerate(spec["segments"]):
        mp3_path = lang_tmp / f"{seg['id']}.mp3"
        await synthesize_voice(seg["text"], spec["voice"], mp3_path)

        audio = AudioFileClip(str(mp3_path))
        seg_dur = audio.duration + 0.45
        progress = (idx + 1) / total_segs
        is_demo = bool(seg.get("is_demo", False))

        if "talk_image" in seg and seg["talk_image"].exists():
            comp = (
                make_talking_presenter_clip(
                    seg["image"],
                    seg["talk_image"],
                    audio,
                    seg_dur,
                    seg["badge"],
                    seg["headline"],
                    seg["text"],
                    progress,
                )
                .with_audio(audio)
                .with_effects([vfx.CrossFadeIn(0.4), vfx.CrossFadeOut(0.4)])
            )
        else:
            frame_img = prepare_static_frame(
                seg["image"],
                seg["badge"],
                seg["headline"],
                seg["text"],
                progress,
                is_demo,
                lang_tmp / f"{seg['id']}.png",
            )
            kb = make_ken_burns_clip(frame_img, seg_dur, zoom_in=(idx % 2 == 0))
            comp = (
                CompositeVideoClip([kb], size=(WIDTH, HEIGHT))
                .with_duration(seg_dur)
                .with_audio(audio)
                .with_effects([vfx.CrossFadeIn(0.4), vfx.CrossFadeOut(0.4)])
            )
        clips.append(comp)

    outro_img = create_brand_card(spec["intro_title"], spec["outro_sub"], lang_tmp / "outro.png")
    outro_clip = (
        ImageClip(str(outro_img))
        .with_duration(3.5)
        .with_effects([vfx.CrossFadeIn(0.45), vfx.FadeOut(0.7)])
    )
    clips.append(outro_clip)

    final_video = concatenate_videoclips(clips, method="compose", padding=-0.35)
    out_file: Path = spec["output"]
    final_video.write_videofile(
        str(out_file),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="veryfast",
        threads=4,
        logger="bar",
    )
    final_video.close()
    return out_file


async def main() -> None:
    results = {}
    for lang_code, spec in SCENES_SPEC.items():
        print(f"=== Building {lang_code.upper()} video -> {spec['output']} ===")
        out_path = await build_language_video(lang_code, spec)
        results[lang_code] = str(out_path)
    (BASE_DIR / "scripts_summary.json").write_text(
        json.dumps(
            {
                k: {
                    "output": str(v["output"]),
                    "voice": v["voice"],
                    "segments_count": len(v["segments"]),
                    "segments": [s["text"] for s in v["segments"]],
                }
                for k, v in SCENES_SPEC.items()
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print("DONE:", results)


if __name__ == "__main__":
    asyncio.run(main())
