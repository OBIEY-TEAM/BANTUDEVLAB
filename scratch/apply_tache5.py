from pathlib import Path

# 1. Update templates/core/home.html
home_path = Path("templates/core/home.html")
home_c = home_path.read_text(encoding="utf-8")

old_hero_buttons = """    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <a href="{% url 'dashboard' %}" class="btn btn-primary">{% trans "Explorer le Tableau de Bord" %}</a>
        <a href="{% url 'zkp_auth:zkp_login_page' %}" class="btn btn-secondary">{% trans "Authentification Zero-Trust (ZKP)" %}</a>
        <a href="{% url 'faq' %}" class="btn btn-secondary">{% icon "help-circle" size=18 %} {% trans "Mode d'Emploi & FAQ" %}</a>
    </div>"""

new_hero_buttons = """    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <a href="{% url 'zkp_auth:zkp_login_page' %}?demo=cadev" class="btn btn-primary" style="background: linear-gradient(135deg, #10b981, #059669); border: none; font-weight: 600;">
            {% icon "zap" size=18 %} {% trans "Parcours Démo Évaluateur CADEV 2026 (1-Clic)" %}
        </a>
        <a href="{% url 'dashboard' %}" class="btn btn-secondary">{% trans "Explorer le Tableau de Bord" %}</a>
        <a href="{% url 'faq' %}" class="btn btn-secondary">{% icon "help-circle" size=18 %} {% trans "Mode d'Emploi & FAQ" %}</a>
    </div>"""

if old_hero_buttons in home_c:
    home_c = home_c.replace(old_hero_buttons, new_hero_buttons)
    home_path.write_text(home_c, encoding="utf-8")
    print("SUCCESS: home.html updated")
else:
    print("WARNING: home.html hero buttons not found exactly")

# 2. Update templates/zkp_auth/login.html
login_path = Path("templates/zkp_auth/login.html")
login_c = login_path.read_text(encoding="utf-8")

demo_banner = """    <!-- Banniere Parcours Evaluation CADEV 2026 (Demo 1-Clic) -->
    <div class="demo-evaluator-card" style="margin-bottom: 1.5rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(245, 158, 11, 0.08)); border: 1px solid var(--secondary-emerald); border-radius: 10px; padding: 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
        <div style="min-width: 250px; flex: 1;">
            <span class="brand-badge" style="background: rgba(16, 185, 129, 0.2); color: #10b981; font-size: 0.75rem; margin-bottom: 0.25rem;">{% trans "PARCOURS D'ÉVALUATION CADEV 2026" %}</span>
            <h4 style="margin: 0.25rem 0; color: #fff; font-size: 1.05rem;">{% icon "sparkles" size=18 %} {% trans "Compte Démo Évaluateur (Connexion en 1 Clic)" %}</h4>
            <p style="margin: 0; font-size: 0.85rem; color: var(--text-muted);">
                {% trans "Compte préconfiguré :" %} <code style="color: #10b981;">cadev_evaluator</code> | {% trans "Protocole Zero-Trust Schnorr NIZKP sans mot de passe." %}
            </p>
        </div>
        <button type="button" class="btn btn-primary" id="btnQuickDemo" onclick="quickDemoLogin()" style="padding: 0.75rem 1.4rem; font-weight: 600; white-space: nowrap; background: linear-gradient(135deg, #10b981, #059669); border: none;">
            {% icon "zap" size=18 %} {% trans "Connexion Démo 1-Clic" %}
        </button>
    </div>

    <!-- Wizard Step Navigation (UI-03) -->"""

if "<!-- Banniere Parcours Evaluation CADEV 2026" not in login_c:
    login_c = login_c.replace("<!-- Wizard Step Navigation (UI-03) -->", demo_banner)

# Add demo button in redirect section
old_redirect_btns = """        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <a id="btnGiteaSignup" href="{{ GITEA_EXTERNAL_URL|default:'https://git.cybersocle.site' }}/user/sign_up" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="padding: 0.85rem 1.6rem; font-size: 1rem; font-weight: 600;">
                {% icon "user-plus" size=18 %} {% trans "Finaliser l'inscription sur Gitea" %}
            </a>"""

new_redirect_btns = """        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <a href="{% url 'dashboard' %}#new-repo" class="btn btn-primary" style="background: linear-gradient(135deg, #10b981, #059669); border: none; padding: 0.85rem 1.6rem; font-size: 1rem; font-weight: 600;">
                {% icon "plus-circle" size=18 %} {% trans "Créer un Dépôt de Démonstration" %}
            </a>
            <a id="btnGiteaSignup" href="{{ GITEA_EXTERNAL_URL|default:'https://git.cybersocle.site' }}/user/sign_up" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="padding: 0.85rem 1.6rem; font-size: 1rem;">
                {% icon "user-plus" size=18 %} {% trans "Finaliser l'inscription sur Gitea" %}
            </a>"""

if old_redirect_btns in login_c:
    login_c = login_c.replace(old_redirect_btns, new_redirect_btns)

# Add quickDemoLogin in script
quick_demo_js = """
async function quickDemoLogin() {
    const userEl = document.getElementById('zkpUsername');
    const secretEl = document.getElementById('zkpSecret');
    if (userEl) userEl.value = 'cadev_evaluator';
    const demoMnemonic = "savanna baobab sahara kilimanjaro zambezi congo senegal niger atlas oasis unity freedom";
    if (secretEl) secretEl.value = demoMnemonic;
    if (typeof setMnemonicWords === 'function') {
        setMnemonicWords(demoMnemonic.split(' '));
    }
    switchWizardStep(3);
    const logEl = document.getElementById('zkpLog');
    if (logEl) logEl.style.display = 'block';
    log(`{% trans "Initialisation rapide du compte démo évaluateur CADEV 2026 (cadev_evaluator)..." %}`);
    await loginWithZkp();
}

window.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('demo') === 'cadev') {
        setTimeout(quickDemoLogin, 500);
    }
});
"""

if "async function quickDemoLogin" not in login_c:
    login_c = login_c.replace("function handleSuccessfulZkpAuth", quick_demo_js + "\nfunction handleSuccessfulZkpAuth")

login_path.write_text(login_c, encoding="utf-8")
print("SUCCESS: login.html updated")

# 3. Update templates/core/dashboard.html
dash_path = Path("templates/core/dashboard.html")
dash_c = dash_path.read_text(encoding="utf-8")

old_repo_header = """        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
            <h3 style="margin: 0;">{% icon "package" size=18 %} {% trans "Moteur Git Panafricain & Dépôts Souverains" %}</h3>
            <span class="brand-badge" style="font-size: 0.75rem;">{% trans "Données Réelles Gitea API" %}</span>
        </div>"""

new_repo_header = """        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
            <h3 style="margin: 0;">{% icon "package" size=18 %} {% trans "Moteur Git Panafricain & Dépôts Souverains" %}</h3>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <button type="button" class="btn btn-primary" id="btnOpenNewRepoModal" onclick="openNewRepoModal()" style="display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; padding: 0.4rem 0.85rem; background: linear-gradient(135deg, #10b981, #059669); border: none; font-weight: 600;">
                    {% icon "plus-circle" size=16 %} {% trans "Créer un Dépôt de Démonstration" %}
                </button>
                <span class="brand-badge" style="font-size: 0.75rem;">{% trans "Données Réelles Gitea API" %}</span>
            </div>
        </div>"""

if old_repo_header in dash_c:
    dash_c = dash_c.replace(old_repo_header, new_repo_header)

# Modal HTML for new repo
modal_html = """
<!-- Modal Creation Depot de Demonstration (CADEV 2026) -->
<div id="modalNewRepo" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.75); z-index: 10000; align-items: center; justify-content: center; backdrop-filter: blur(4px);">
    <div style="background: #0d1117; border: 1px solid var(--dark-border); border-radius: 12px; width: 90%; max-width: 520px; padding: 1.75rem; box-shadow: 0 20px 40px rgba(0,0,0,0.6);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
            <h3 style="margin: 0; display: flex; align-items: center; gap: 0.5rem; color: #fff;">
                {% icon "package" size=20 %} {% trans "Nouveau Dépôt de Démonstration" %}
            </h3>
            <button type="button" onclick="closeNewRepoModal()" style="background: none; border: none; color: var(--text-muted); font-size: 1.25rem; cursor: pointer;">✕</button>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.25rem;">
            {% trans "Initialisez un dépôt souverain sur la forge Gitea avec branche principale par défaut et traçabilité dans l'Audit Trail immuable." %}
        </p>
        <div style="margin-bottom: 1rem;">
            <label style="display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.35rem; color: #fff;">{% trans "Nom du Dépôt :" %}</label>
            <input type="text" id="modalRepoName" value="demo-cadev-sovereign" style="width: 100%; padding: 0.65rem; background: #080c14; border: 1px solid var(--dark-border); color: #fff; border-radius: 6px; font-size: 0.95rem; box-sizing: border-box;">
        </div>
        <div style="margin-bottom: 1rem;">
            <label style="display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.35rem; color: #fff;">{% trans "Description :" %}</label>
            <input type="text" id="modalRepoDesc" value="Dépôt souverain de test créé pour l'évaluation CADEV 2026" style="width: 100%; padding: 0.65rem; background: #080c14; border: 1px solid var(--dark-border); color: #fff; border-radius: 6px; font-size: 0.95rem; box-sizing: border-box;">
        </div>
        <div style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
            <input type="checkbox" id="modalRepoPrivate">
            <label for="modalRepoPrivate" style="font-size: 0.85rem; color: var(--text-muted); cursor: pointer;">{% trans "Dépôt privé (accès restreint à l'organisation)" %}</label>
        </div>
        <div id="modalRepoFeedback" style="display: none; padding: 0.6rem; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1rem;"></div>
        <div style="display: flex; justify-content: flex-end; gap: 0.75rem;">
            <button type="button" class="btn btn-secondary" onclick="closeNewRepoModal()">{% trans "Annuler" %}</button>
            <button type="button" class="btn btn-primary" id="btnSubmitNewRepo" onclick="submitNewDemoRepo()" style="background: linear-gradient(135deg, #10b981, #059669); border: none;">
                {% icon "check" size=16 %} {% trans "Créer le Dépôt Immédiatement" %}
            </button>
        </div>
    </div>
</div>
"""

modal_js = """
function openNewRepoModal() {
    const modal = document.getElementById('modalNewRepo');
    if (modal) modal.style.display = 'flex';
}
function closeNewRepoModal() {
    const modal = document.getElementById('modalNewRepo');
    if (modal) modal.style.display = 'none';
}
async function submitNewDemoRepo() {
    const name = document.getElementById('modalRepoName').value.trim();
    const description = document.getElementById('modalRepoDesc').value.trim();
    const isPrivate = document.getElementById('modalRepoPrivate').checked;
    const feedback = document.getElementById('modalRepoFeedback');
    const submitBtn = document.getElementById('btnSubmitNewRepo');

    if (!name) {
        if (feedback) {
            feedback.style.display = 'block';
            feedback.style.background = 'rgba(239, 68, 68, 0.15)';
            feedback.style.color = '#ef4444';
            feedback.textContent = '{% trans "Veuillez renseigner un nom de dépôt." %}';
        }
        return;
    }

    if (submitBtn) submitBtn.disabled = true;
    if (feedback) {
        feedback.style.display = 'block';
        feedback.style.background = 'rgba(16, 185, 129, 0.1)';
        feedback.style.color = '#10b981';
        feedback.textContent = '{% trans "Création du dépôt sur la forge en cours..." %}';
    }

    try {
        const headers = {'Content-Type': 'application/json'};
        if (window.getCsrfToken && window.getCsrfToken()) {
            headers['X-CSRFToken'] = window.getCsrfToken();
        }
        const res = await fetch('/api/forge/repositories/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({name, description, private: isPrivate})
        });
        const data = await res.json();
        if (res.ok) {
            feedback.style.background = 'rgba(16, 185, 129, 0.2)';
            feedback.style.color = '#10b981';
            feedback.textContent = '{% trans "Dépôt créé avec succès !" %}';
            if (window.showToast) window.showToast(`Dépôt ${name} créé avec succès !`, 'success');
            setTimeout(() => {
                closeNewRepoModal();
                window.location.reload();
            }, 1000);
        } else {
            feedback.style.background = 'rgba(239, 68, 68, 0.15)';
            feedback.style.color = '#ef4444';
            feedback.textContent = data.error || '{% trans "Échec de création du dépôt." %}';
        }
    } catch (err) {
        feedback.style.background = 'rgba(239, 68, 68, 0.15)';
        feedback.style.color = '#ef4444';
        feedback.textContent = err.message || '{% trans "Erreur de connexion." %}';
    } finally {
        if (submitBtn) submitBtn.disabled = false;
    }
}

window.addEventListener('DOMContentLoaded', () => {
    if (window.location.hash === '#new-repo') {
        setTimeout(openNewRepoModal, 400);
    }
});
"""

if "id=\"modalNewRepo\"" not in dash_c:
    dash_c = dash_c.replace("{% endblock %}", modal_html + "\n{% endblock %}")
    dash_c = dash_c.replace("</script>", modal_js + "\n</script>")
    dash_path.write_text(dash_c, encoding="utf-8")
    print("SUCCESS: dashboard.html updated with repo creation modal")

# 4. Update templates/core/faq.html
faq_path = Path("templates/core/faq.html")
faq_c = faq_path.read_text(encoding="utf-8")

faq_demo_card = """        <!-- Q-DEMO : Parcours Démo Évaluateur CADEV 2026 -->
        <details class="faq-item" id="faq-cadev-demo" open>
            <summary class="faq-summary" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(245, 158, 11, 0.08)); border-left: 4px solid #10b981;">
                <span class="faq-summary-title">
                    <span class="faq-badge" style="background: #10b981; color: #000; font-weight: bold;">DEMO</span>
                    <strong>{% trans "Évaluateur CADEV 2026 : Comment tester l'ensemble du parcours sans friction ?" %}</strong>
                </span>
                <span class="faq-chevron">{% icon "chevron-down" size=18 %}</span>
            </summary>
            <div class="faq-content">
                <p>
                    {% trans "Bienvenue au jury et aux évaluateurs du concours CADEV 2026 (Systalink Cloud). Voici le parcours pas-à-pas pour évaluer BantuDevLab en toute autonomie :" %}
                </p>
                <div class="faq-steps-list">
                    <div class="faq-step-item">
                        <strong>{% trans "1. Connexion Zero-Trust immédiate :" %}</strong>
                        <p>{% trans "Ouvrez la page de connexion ZKP et cliquez sur le bouton « Connexion Démo 1-Clic ». Le compte " %}<code>cadev_evaluator</code>{% trans " s'authentifie instantanément via la preuve mathématique de Schnorr (RFC 3526 MODP 2048 bits) sans transmettre aucun mot de passe." %}</p>
                    </div>
                    <div class="faq-step-item" style="margin-top: 0.75rem;">
                        <strong>{% trans "2. Consultation de la FAQ et conformité :" %}</strong>
                        <p>{% trans "Cette section détaille les principes Zero-Trust, l'absence de dépendance aux CDN tiers, la politique Zéro-Emoji et la bascule vers le cache permissif Valkey 7.2 (BSD-3-Clause) en remplacement de Redis." %}</p>
                    </div>
                    <div class="faq-step-item" style="margin-top: 0.75rem;">
                        <strong>{% trans "3. Création d'un dépôt de démonstration :" %}</strong>
                        <p>{% trans "Sur le Tableau de Bord, cliquez sur « Créer un Dépôt de Démonstration ». Renseignez le nom (ex: demo-cadev-2026) et validez. Le dépôt est créé sur la forge souveraine et apparaît immédiatement avec ses actions de sécurité." %}</p>
                    </div>
                    <div class="faq-step-item" style="margin-top: 0.75rem;">
                        <strong>{% trans "4. Audit SAST et Revue IA Locale Gemma 2 2B :" %}</strong>
                        <p>{% trans "Sur n'importe quel dépôt, cliquez sur « Run Security Audit » pour calculer l'entropie de Shannon ($H \ge 3.8$) ou « Ask Gemma Review » pour invoquer le modèle compact local exécuté sur conteneur Ollama." %}</p>
                    </div>
                </div>
            </div>
        </details>
"""

if "id=\"faq-cadev-demo\"" not in faq_c:
    faq_c = faq_c.replace('<div class="faq-accordion-group">', '<div class="faq-accordion-group">\n' + faq_demo_card)
    faq_path.write_text(faq_c, encoding="utf-8")
    print("SUCCESS: faq.html updated with CADEV demo guide")
