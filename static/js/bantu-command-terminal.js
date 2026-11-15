/**
 * BANTUDEVLAB - Sovereign Command Prompt Terminal & Top-Up Analysis Interface
 * Provides:
 * 1. Pro Action Buttons ("Run Security Audit" & "Ask Gemma Review") in the Gitea headbar right after [Explore]
 *    on the exact same horizontal alignment as the logo, in the Django navbar right after the logo,
 *    and on every Gitea Repository header / Dashboard repository list item.
 * 2. Structured Command Prompt Terminal (Zero free-text input):
 *    - '+' Button (#bantu-cmd-plus-btn) to configure target options:
 *      * Repository selector (#bantu-cmd-repo-select)
 *      * Branch selector (#bantu-cmd-branch-select)
 *      * File or All Files (*) selector (#bantu-cmd-file-select)
 *    - 'Execute' Button (#bantu-cmd-exec-btn) to run SAST Security Audit or Gemma AI Review.
 * 3. Top-Up Results Interface (#bantu-cmd-results-panel) & Multi-lingual synchronization (fr, en, sw, pt).
 */
(function () {
  "use strict";

  if (window.__BANTU_CMD_TERMINAL_READY__) return;
  window.__BANTU_CMD_TERMINAL_READY__ = true;

  var TERMINAL_I18N = {
    fr: {
      btnSecurity: "Run Security Audit",
      btnGemma: "Ask Gemma Review",
      termTitleSecurity: "TERMINAL SOUVERAIN — RUN SECURITY AUDIT (SAST)",
      termTitleGemma: "TERMINAL SOUVERAIN — ASK GEMMA REVIEW (IA)",
      plusTooltip: "Configurer les options de la commande (+ Dépôt, Branche, Fichier)",
      lblRepo: "Dépôt Git",
      lblBranch: "Branche",
      lblFile: "Cible / Fichier",
      allFiles: "* (Tous les fichiers du dépôt)",
      btnExecute: "Exécuter",
      runningSecurity: "Exécution de l'audit SAST souverain sur le dépôt...",
      runningGemma: "Consultation du moteur local Gemma 2 2B sur le dépôt...",
      toastStartSecurity: "Audit de sécurité SAST lancé sur ",
      toastStartGemma: "Revue IA Gemma lancée sur ",
      toastDoneSecurity: "Audit terminé ! Score de souveraineté : ",
      toastDoneGemma: "Revue IA Gemma complétée avec succès.",
      toastError: "Erreur lors de l'exécution de la commande : ",
      scoreLabel: "Score de Souveraineté",
      criticalLabel: "Critiques",
      highLabel: "Hautes",
      mediumLabel: "Moyennes",
      filesScannedLabel: "Fichiers analysés",
      noIssues: "Aucune vulnérabilité détectée. Dépôt 100% conforme aux normes souveraines ADSS-v1.",
      recPrefix: "Recommandation Souveraine :",
      lineLabel: "Ligne",
      closeLabel: "Fermer",
    },
    en: {
      btnSecurity: "Run Security Audit",
      btnGemma: "Ask Gemma Review",
      termTitleSecurity: "SOVEREIGN TERMINAL — RUN SECURITY AUDIT (SAST)",
      termTitleGemma: "SOVEREIGN TERMINAL — ASK GEMMA REVIEW (AI)",
      plusTooltip: "Configure command options (+ Repository, Branch, File)",
      lblRepo: "Git Repository",
      lblBranch: "Branch",
      lblFile: "Target / File",
      allFiles: "* (All files in repository)",
      btnExecute: "Execute",
      runningSecurity: "Running sovereign SAST security audit on repository...",
      runningGemma: "Querying local Gemma 2 2B AI engine on repository...",
      toastStartSecurity: "SAST Security Audit started on ",
      toastStartGemma: "Gemma AI Review started on ",
      toastDoneSecurity: "Audit completed! Sovereignty score: ",
      toastDoneGemma: "Gemma AI review completed successfully.",
      toastError: "Command execution error: ",
      scoreLabel: "Sovereignty Score",
      criticalLabel: "Critical",
      highLabel: "High",
      mediumLabel: "Medium",
      filesScannedLabel: "Files analyzed",
      noIssues: "No vulnerabilities detected. Repository is 100% compliant with ADSS-v1 sovereign standards.",
      recPrefix: "Sovereign Recommendation:",
      lineLabel: "Line",
      closeLabel: "Close",
    },
    sw: {
      btnSecurity: "Tekeleza Ukaguzi wa Usalama",
      btnGemma: "Uliza Mapitio ya Gemma",
      termTitleSecurity: "KITUO HURU — RUN SECURITY AUDIT (SAST)",
      termTitleGemma: "KITUO HURU — ASK GEMMA REVIEW (AI)",
      plusTooltip: "Sanidi chaguo za amri (+ Hazina, Tawi, Faili)",
      lblRepo: "Hazina ya Git",
      lblBranch: "Tawi (Branch)",
      lblFile: "Faili Lengwa",
      allFiles: "* (Faili zote za hazina)",
      btnExecute: "Tekeleza",
      runningSecurity: "Inakagua usalama wa SAST kwenye hazina...",
      runningGemma: "Inachambua msimbo kupitia Gemma 2 2B AI...",
      toastStartSecurity: "Ukaguzi wa usalama umeanza kwenye ",
      toastStartGemma: "Ukaguzi wa Gemma AI umeanza kwenye ",
      toastDoneSecurity: "Ukaguzi umekamilika! Alama ya uhuru: ",
      toastDoneGemma: "Ukaguzi wa Gemma AI umekamilika.",
      toastError: "Hitilafu wakati wa kutekeleza amri: ",
      scoreLabel: "Alama ya Uhuru",
      criticalLabel: "Hatari Kubwa",
      highLabel: "Hatari ya Juu",
      mediumLabel: "Wastani",
      filesScannedLabel: "Faili zilizokaguliwa",
      noIssues: "Hakuna udhaifu uliogunduliwa. Hazina inazingatia viwango vya ADSS-v1 kwa 100%.",
      recPrefix: "Pendekezo Huru:",
      lineLabel: "Mstari",
      closeLabel: "Funga",
    },
    pt: {
      btnSecurity: "Executar Auditoria de Segurança",
      btnGemma: "Pedir Revisão Gemma",
      termTitleSecurity: "TERMINAL SOBERANO — RUN SECURITY AUDIT (SAST)",
      termTitleGemma: "TERMINAL SOBERANO — ASK GEMMA REVIEW (IA)",
      plusTooltip: "Configurar opções do comando (+ Repositório, Ramo, Ficheiro)",
      lblRepo: "Repositório Git",
      lblBranch: "Ramo (Branch)",
      lblFile: "Alvo / Ficheiro",
      allFiles: "* (Todos os ficheiros do repositório)",
      btnExecute: "Executar",
      runningSecurity: "A executar auditoria de segurança SAST no repositório...",
      runningGemma: "A consultar o motor local Gemma 2 2B IA no repositório...",
      toastStartSecurity: "Auditoria SAST iniciada em ",
      toastStartGemma: "Revisão Gemma IA iniciada em ",
      toastDoneSecurity: "Auditoria concluída! Pontuação de soberania: ",
      toastDoneGemma: "Revisão Gemma IA concluída com sucesso.",
      toastError: "Erro ao executar o comando: ",
      scoreLabel: "Pontuação de Soberania",
      criticalLabel: "Críticas",
      highLabel: "Altas",
      mediumLabel: "Médias",
      filesScannedLabel: "Ficheiros analisados",
      noIssues: "Nenhuma vulnerabilidade detetada. Repositório 100% conforme às normas ADSS-v1.",
      recPrefix: "Recomendação Soberana:",
      lineLabel: "Linha",
      closeLabel: "Fechar",
    },
  };

  function getCookie(name) {
    var m = document.cookie.match(new RegExp("(?:^|;\\s*)" + name + "=([^;]*)"));
    return m ? decodeURIComponent(m[1]) : null;
  }

  function getActiveLang() {
    var raw =
      getCookie("bantu_lang") ||
      getCookie("django_language") ||
      getCookie("lang") ||
      (function () {
        try {
          return localStorage.getItem("bantu_lang");
        } catch (e) {
          return null;
        }
      })() ||
      document.documentElement.lang ||
      "fr";
    var code = String(raw).toLowerCase().slice(0, 2);
    return TERMINAL_I18N[code] ? code : "fr";
  }

  function isGiteaHost() {
    var h = window.location.hostname;
    var p = window.location.port;
    return (
      h.indexOf("git.") === 0 ||
      h.indexOf("gitea.") === 0 ||
      p === "3002" ||
      !!document.querySelector("nav#navbar, .page-content.repository, meta[name='author'][content='Gitea']")
    );
  }

  function getApiBaseCandidates() {
    var list = [""];
    var host = window.location.hostname;
    if (host === "localhost" || host === "127.0.0.1") {
      list.push("http://" + host + ":8001");
      list.push("http://" + host + ":8000");
      list.push("http://127.0.0.1:8001");
    }
    if (host.indexOf("cybersocle.site") !== -1) {
      list.push("https://cybersocle.site");
    }
    return list;
  }

  async function fetchApiWithFallback(path, options) {
    var bases = getApiBaseCandidates();
    var lastErr = null;
    for (var i = 0; i < bases.length; i++) {
      var url = bases[i] + path;
      try {
        var res = await fetch(url, options);
        if (res.ok) {
          return await res.json();
        }
      } catch (err) {
        lastErr = err;
      }
    }
    throw lastErr || new Error("Service API indisponible");
  }

  function notifyToast(msg, type) {
    if (typeof window.showToast === "function") {
      window.showToast(msg, type || "info");
      return;
    }
    var toast = document.getElementById("bantu-cmd-floating-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "bantu-cmd-floating-toast";
      toast.style.cssText =
        "position:fixed;bottom:20px;left:20px;z-index:200000;padding:12px 18px;border-radius:8px;background:#070e1e;color:#f8fafc;border:1px solid #00e5ff;box-shadow:0 10px 25px rgba(0,0,0,0.6);font-size:13px;font-weight:600;transition:opacity 0.25s;";
      document.body.appendChild(toast);
    }
    toast.style.borderColor = type === "error" ? "#ef4444" : type === "success" ? "#10b981" : "#f59e0b";
    toast.textContent = msg;
    toast.style.opacity = "1";
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function () {
      toast.style.opacity = "0";
    }, 3800);
  }

  function normalizeRepoFullName(r) {
    var cleaned = String(r || "").trim().replace(/^\/+|\/+$/g, "").replace(/\.git$/, "");
    return /^[^/\s]+\/[^/\s]+$/.test(cleaned) ? cleaned : "";
  }

  function detectCurrentRepoFromUrl() {
    var path = window.location.pathname.replace(/^\/+|\/+$/g, "");
    if (!path) return "";
    var reserved = [
      "explore",
      "user",
      "admin",
      "api",
      "assets",
      "static",
      "dashboard",
      "metrics",
      "faq",
      "login",
      "notifications",
      "milestones",
      "issues",
      "pulls",
      "org",
      "repo",
      "i18n",
      "-",
    ];
    var parts = path.split("/");
    if (parts.length >= 2 && reserved.indexOf(parts[0].toLowerCase()) === -1) {
      var repoClean = parts[1].replace(/\.git$/, "");
      if (repoClean && reserved.indexOf(repoClean.toLowerCase()) === -1) {
        return parts[0] + "/" + repoClean;
      }
    }
    return "";
  }

  function detectCurrentBranchFromUrl() {
    var path = window.location.pathname.replace(/^\/+|\/+$/g, "");
    var parts = path.split("/");
    // 1. /owner/repo/src/branch/<name>/... or /owner/repo/commits/branch/<name>
    if (parts.length >= 5 && (parts[2] === "src" || parts[2] === "commits") && parts[3] === "branch") {
      return decodeURIComponent(parts[4]);
    }
    // 2. Gitea UI branch dropdown selector
    var branchEl = document.querySelector(".choose.branch .text, #branch-select .text, .branch-dropdown .text, [data-branch]");
    if (branchEl && branchEl.textContent && branchEl.textContent.trim()) {
      return branchEl.textContent.trim();
    }
    return "main";
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  var state = {
    action: "security",
    repo: "",
    branch: "main",
    file: "*",
    filesList: [],
    optionsExpanded: true,
  };

  function injectStyles() {
    if (document.getElementById("bantu-cmd-terminal-styles")) return;
    var style = document.createElement("style");
    style.id = "bantu-cmd-terminal-styles";
    style.textContent =
      ".bantu-pro-actions-group{display:inline-flex !important;align-items:center !important;align-self:center !important;gap:8px !important;margin:0 8px 0 14px !important;padding:0 !important;flex-wrap:nowrap;vertical-align:middle !important;flex-shrink:0;}" +
      "#navbar .navbar-left .bantu-pro-actions-group,nav#navbar .bantu-pro-actions-group{display:inline-flex !important;align-items:center !important;align-self:center !important;height:auto !important;margin-left:8px !important;}" +
      ".bantu-pro-action-btn{display:inline-flex !important;align-items:center !important;justify-content:center !important;gap:6px !important;padding:5px 11px !important;border-radius:6px !important;font-size:12px !important;font-weight:700 !important;cursor:pointer !important;transition:all 0.15s ease !important;text-decoration:none !important;white-space:nowrap !important;line-height:1.2 !important;font-family:system-ui,-apple-system,sans-serif !important;}" +
      ".bantu-pro-btn-security{background:rgba(245,158,11,0.16) !important;color:#f59e0b !important;border:1px solid rgba(245,158,11,0.65) !important;}" +
      ".bantu-pro-btn-security:hover{background:#f59e0b !important;color:#020617 !important;box-shadow:0 0 12px rgba(245,158,11,0.45) !important;}" +
      ".bantu-pro-btn-gemma{background:rgba(0,229,255,0.14) !important;color:#00e5ff !important;border:1px solid rgba(0,229,255,0.6) !important;}" +
      ".bantu-pro-btn-gemma:hover{background:#00e5ff !important;color:#020617 !important;box-shadow:0 0 12px rgba(0,229,255,0.45) !important;}" +
      "[data-theme='light'] .bantu-pro-btn-security{background:#fffbeb !important;color:#b45309 !important;border-color:#f59e0b !important;}" +
      "[data-theme='light'] .bantu-pro-btn-gemma{background:#eff6ff !important;color:#0051cc !important;border-color:#3b82f6 !important;}" +
      "#bantu-command-terminal-modal{display:none;position:fixed;inset:0;z-index:150000;background:rgba(2,6,23,0.78);backdrop-filter:blur(5px);align-items:flex-start;justify-content:center;padding:2.5vh 12px;overflow-y:auto;}" +
      "#bantu-command-terminal-modal.open{display:flex;}" +
      ".bantu-term-window{width:min(920px,96vw);background:#050b18;border:1px solid #00e5ff;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,0.85),0 0 25px rgba(0,229,255,0.18);color:#f8fafc;overflow:hidden;font-family:'JetBrains Mono','Fira Code',Consolas,monospace;animation:bantuSlideTopUp 0.2s ease-out;}" +
      "[data-theme='light'] .bantu-term-window{background:#0f172a;color:#f8fafc;}" +
      "@keyframes bantuSlideTopUp{from{transform:translateY(-18px);opacity:0;}to{transform:translateY(0);opacity:1;}}" +
      ".bantu-term-titlebar{display:flex;align-items:center;justify-content:space-between;padding:10px 16px;background:#020617;border-bottom:1px solid #1e293b;gap:10px;flex-wrap:wrap;}" +
      ".bantu-term-dots{display:inline-flex;align-items:center;gap:6px;}" +
      ".bantu-term-dot{width:10px;height:10px;border-radius:50%;display:inline-block;}" +
      ".bantu-term-prompt-row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 16px;background:#070e1e;border-bottom:1px solid #1e293b;flex-wrap:wrap;}" +
      ".bantu-term-prompt-display{display:flex;align-items:center;gap:8px;flex:1;min-width:240px;font-size:13px;background:#020617;border:1px solid #1e293b;border-radius:8px;padding:9px 12px;overflow-x:auto;white-space:nowrap;user-select:none;}" +
      ".bantu-term-plus-btn{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:#0b1528;border:1px solid #00e5ff;color:#00e5ff;font-size:20px;font-weight:800;cursor:pointer;transition:all 0.15s;flex-shrink:0;}" +
      ".bantu-term-plus-btn:hover,.bantu-term-plus-btn.active{background:#00e5ff;color:#020617;}" +
      ".bantu-term-exec-btn{display:inline-flex;align-items:center;gap:6px;padding:9px 18px;border-radius:8px;background:#10b981;color:#020617;border:none;font-weight:800;font-size:13px;cursor:pointer;font-family:inherit;transition:all 0.15s;flex-shrink:0;}" +
      ".bantu-term-exec-btn:hover{background:#059669;color:#fff;box-shadow:0 0 15px rgba(16,185,129,0.4);}" +
      ".bantu-term-options-bar{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:14px 16px;background:#0b1528;border-bottom:1px solid #1e293b;font-family:system-ui,-apple-system,sans-serif;}" +
      ".bantu-term-field{display:flex;flex-direction:column;gap:4px;min-width:0;}" +
      ".bantu-term-field label{font-size:11px;font-weight:700;text-transform:uppercase;color:#94a3b8;letter-spacing:0.04em;}" +
      ".bantu-term-select{width:100%;padding:8px 10px;border-radius:6px;background:#020617 !important;color:#f8fafc !important;border:1px solid #1e293b !important;font-size:13px;outline:none;cursor:pointer;}" +
      ".bantu-term-select:focus{border-color:#00e5ff !important;}" +
      ".bantu-term-results-topup{padding:16px;max-height:62vh;overflow-y:auto;background:#050b18;font-family:system-ui,-apple-system,sans-serif;}" +
      ".bantu-gitea-repo-banner{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 14px;margin:10px 0;background:rgba(7,14,30,0.9);border:1px solid rgba(0,229,255,0.35);border-radius:8px;flex-wrap:wrap;}" +
      ".bantu-pro-actions-group,.bantu-pro-action-btn{white-space:nowrap;flex-shrink:0;}" +
      "@media (max-width:1024px){#navbar .navbar-left .bantu-pro-actions-group,nav#navbar .bantu-pro-actions-group,#bantu-gitea-nav-pro-actions{display:none !important;}}" +
      "@media (max-width:992px){.navbar .bantu-pro-actions-group,#bantu-django-nav-pro-actions{display:none !important;}}" +
      "@media (max-width:768px){.bantu-term-options-bar{grid-template-columns:1fr;}}" +
      "@media (max-width:480px){.bantu-pro-action-btn{padding:4px 7px !important;font-size:11px !important;}.bantu-term-prompt-row{padding:10px;}.bantu-term-exec-btn{width:100%;justify-content:center;}}";
    document.head.appendChild(style);
  }

  function updatePromptPreview() {
    var cmdSpan = document.getElementById("bantu-cmd-preview-text");
    if (!cmdSpan) return;
    var bin = state.action === "gemma" ? "gemma-review" : "security-audit";
    var colorBin = state.action === "gemma" ? "#00e5ff" : "#f59e0b";
    var repoArg = state.repo || "sovereign-org/afri-fintech-gateway";
    var branchArg = state.branch || "main";
    var fileArg = state.file || "*";
    cmdSpan.innerHTML =
      '<span style="color:#10b981;font-weight:700;">bantu@sovereign-forge:~$</span> ' +
      '<span style="color:' +
      colorBin +
      ';font-weight:700;">' +
      bin +
      "</span> " +
      '<span style="color:#94a3b8;">--repo=</span><span style="color:#f8fafc;">' +
      escapeHtml(repoArg) +
      "</span> " +
      '<span style="color:#94a3b8;">--branch=</span><span style="color:#f59e0b;">' +
      escapeHtml(branchArg) +
      "</span> " +
      '<span style="color:#94a3b8;">--target=</span><span style="color:#00e5ff;">' +
      escapeHtml(fileArg) +
      "</span>";
  }

  function ensureModalCreated() {
    var existing = document.getElementById("bantu-command-terminal-modal");
    if (existing) return existing;

    var modal = document.createElement("div");
    modal.id = "bantu-command-terminal-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");

    modal.innerHTML =
      '<div class="bantu-term-window">' +
      '  <div class="bantu-term-titlebar">' +
      '    <div style="display:flex;align-items:center;gap:10px;">' +
      '      <span class="bantu-term-dots">' +
      '        <span class="bantu-term-dot" style="background:#ef4444;"></span>' +
      '        <span class="bantu-term-dot" style="background:#f59e0b;"></span>' +
      '        <span class="bantu-term-dot" style="background:#10b981;"></span>' +
      "      </span>" +
      '      <strong id="bantu-term-modal-title" style="font-size:12px;color:#00e5ff;letter-spacing:0.04em;"></strong>' +
      "    </div>" +
      '    <div style="display:flex;align-items:center;gap:6px;">' +
      '      <button type="button" id="bantu-switch-mode-security" class="bantu-pro-action-btn bantu-pro-btn-security" style="padding:3px 9px !important;font-size:11px !important;">Run Security Audit</button>' +
      '      <button type="button" id="bantu-switch-mode-gemma" class="bantu-pro-action-btn bantu-pro-btn-gemma" style="padding:3px 9px !important;font-size:11px !important;">Ask Gemma Review</button>' +
      '      <button type="button" id="bantu-term-close-btn" style="background:transparent;border:1px solid #334155;color:#94a3b8;border-radius:6px;padding:3px 9px;font-size:12px;cursor:pointer;">Esc</button>' +
      "    </div>" +
      "  </div>" +
      '  <div class="bantu-term-prompt-row">' +
      '    <div class="bantu-term-prompt-display" id="bantu-cmd-preview-text"></div>' +
      '    <div style="display:flex;align-items:center;gap:8px;">' +
      '      <button type="button" id="bantu-cmd-plus-btn" class="bantu-term-plus-btn active" title="+">+</button>' +
      '      <button type="button" id="bantu-cmd-exec-btn" class="bantu-term-exec-btn">' +
      '        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M4 2v12l10-6L4 2z"></path></svg>' +
      '        <span id="bantu-cmd-exec-label">Exécuter</span>' +
      "      </button>" +
      "    </div>" +
      "  </div>" +
      '  <div id="bantu-cmd-options-bar" class="bantu-term-options-bar">' +
      '    <div class="bantu-term-field">' +
      '      <label id="bantu-lbl-repo" for="bantu-cmd-repo-select">Dépôt Git</label>' +
      '      <select id="bantu-cmd-repo-select" class="bantu-term-select"></select>' +
      "    </div>" +
      '    <div class="bantu-term-field">' +
      '      <label id="bantu-lbl-branch" for="bantu-cmd-branch-select">Branche</label>' +
      '      <select id="bantu-cmd-branch-select" class="bantu-term-select"></select>' +
      "    </div>" +
      '    <div class="bantu-term-field">' +
      '      <label id="bantu-lbl-file" for="bantu-cmd-file-select">Cible / Fichier</label>' +
      '      <select id="bantu-cmd-file-select" class="bantu-term-select"></select>' +
      "    </div>" +
      "  </div>" +
      '  <div id="bantu-cmd-results-panel" class="bantu-term-results-topup" style="display:none;"></div>' +
      "</div>";

    document.body.appendChild(modal);

    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeCommandTerminal();
    });
    document.getElementById("bantu-term-close-btn").addEventListener("click", closeCommandTerminal);

    document.getElementById("bantu-switch-mode-security").addEventListener("click", function () {
      setTerminalAction("security");
    });
    document.getElementById("bantu-switch-mode-gemma").addEventListener("click", function () {
      setTerminalAction("gemma");
    });

    var plusBtn = document.getElementById("bantu-cmd-plus-btn");
    var optBar = document.getElementById("bantu-cmd-options-bar");
    plusBtn.addEventListener("click", function () {
      state.optionsExpanded = !state.optionsExpanded;
      optBar.style.display = state.optionsExpanded ? "grid" : "none";
      plusBtn.classList.toggle("active", state.optionsExpanded);
    });

    var repoSel = document.getElementById("bantu-cmd-repo-select");
    var branchSel = document.getElementById("bantu-cmd-branch-select");
    var fileSel = document.getElementById("bantu-cmd-file-select");

    repoSel.addEventListener("change", function () {
      state.repo = repoSel.value;
      state.file = "*";
      updatePromptPreview();
      loadExplorerData(state.repo, "");
    });
    branchSel.addEventListener("change", function () {
      state.branch = branchSel.value;
      state.file = "*";
      updatePromptPreview();
      loadExplorerData(state.repo, state.branch);
    });
    fileSel.addEventListener("change", function () {
      state.file = fileSel.value;
      updatePromptPreview();
    });

    document.getElementById("bantu-cmd-exec-btn").addEventListener("click", executeCommandAnalysis);

    return modal;
  }

  function applyTerminalI18n() {
    var lang = getActiveLang();
    var t = TERMINAL_I18N[lang];
    var titleEl = document.getElementById("bantu-term-modal-title");
    if (titleEl) {
      titleEl.textContent = state.action === "gemma" ? t.termTitleGemma : t.termTitleSecurity;
    }
    var plusBtn = document.getElementById("bantu-cmd-plus-btn");
    if (plusBtn) plusBtn.title = t.plusTooltip;
    var lblRepo = document.getElementById("bantu-lbl-repo");
    if (lblRepo) lblRepo.textContent = t.lblRepo;
    var lblBranch = document.getElementById("bantu-lbl-branch");
    if (lblBranch) lblBranch.textContent = t.lblBranch;
    var lblFile = document.getElementById("bantu-lbl-file");
    if (lblFile) lblFile.textContent = t.lblFile;
    var execLbl = document.getElementById("bantu-cmd-exec-label");
    if (execLbl) execLbl.textContent = t.btnExecute;

    document.querySelectorAll(".bantu-i18n-security-label").forEach(function (el) {
      el.textContent = t.btnSecurity;
    });
    document.querySelectorAll(".bantu-i18n-gemma-label").forEach(function (el) {
      el.textContent = t.btnGemma;
    });
  }

  function setTerminalAction(action) {
    state.action = action === "gemma" ? "gemma" : "security";
    applyTerminalI18n();
    updatePromptPreview();
  }

  async function fetchLiveGiteaData(preferredRepo, preferredBranch) {
    if (!isGiteaHost()) return null;
    try {
      var repoMap = {};
      var repoList = [];

      // 1. Try logged-in user repos first only when a Gitea session appears active
      var hasGiteaSession = !!document.querySelector('a[href*="/user/logout"], .user.menu, img.avatar');
      if (hasGiteaSession) {
        try {
          var rUser = await fetch("/api/v1/user/repos?limit=50", { credentials: "same-origin" });
          if (rUser.ok) {
            var uData = await rUser.json();
            if (Array.isArray(uData)) {
              uData.forEach(function (r) {
                if (r && r.full_name && !repoMap[r.full_name]) {
                  repoMap[r.full_name] = true;
                  repoList.push({
                    full_name: r.full_name,
                    name: r.name,
                    default_branch: r.default_branch || "main",
                  });
                }
              });
            }
          }
        } catch (e1) {}
      }

      // 2. Also search public/visible repos on Gitea
      try {
        var rSearch = await fetch("/api/v1/repos/search?limit=50", { credentials: "same-origin" });
        if (rSearch.ok) {
          var sData = await rSearch.json();
          var arr = (sData && sData.data) || [];
          arr.forEach(function (r) {
            if (r && r.full_name && !repoMap[r.full_name]) {
              repoMap[r.full_name] = true;
              repoList.push({
                full_name: r.full_name,
                name: r.name,
                default_branch: r.default_branch || "main",
              });
            }
          });
        }
      } catch (e2) {}

      // 3. Also scan repo links visible on current Gitea DOM (Dashboard / Explore)
      document.querySelectorAll("a[href]").forEach(function (a) {
        var href = a.getAttribute("href") || "";
        var m = href.match(/^\/([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+)$/);
        if (m) {
          var owner = m[1];
          var rname = m[2];
          var reserved = [
            "explore",
            "user",
            "admin",
            "api",
            "assets",
            "static",
            "org",
            "repo",
            "notifications",
            "milestones",
            "issues",
            "pulls",
          ];
          if (reserved.indexOf(owner.toLowerCase()) === -1 && reserved.indexOf(rname.toLowerCase()) === -1) {
            var full = owner + "/" + rname;
            if (!repoMap[full]) {
              repoMap[full] = true;
              repoList.push({ full_name: full, name: rname, default_branch: "main" });
            }
          }
        }
      });

      var selectedRepo =
        normalizeRepoFullName(preferredRepo) ||
        detectCurrentRepoFromUrl() ||
        (repoList[0] && normalizeRepoFullName(repoList[0].full_name)) ||
        "";
      if (selectedRepo && !repoMap[selectedRepo]) {
        repoList.unshift({
          full_name: selectedRepo,
          name: selectedRepo.split("/")[1] || selectedRepo,
          default_branch: "main",
        });
      }

      if (!selectedRepo) return null;

      var branches = [];
      try {
        var rBr = await fetch("/api/v1/repos/" + selectedRepo + "/branches", { credentials: "same-origin" });
        if (rBr.ok) {
          var brData = await rBr.json();
          if (Array.isArray(brData)) {
            brData.forEach(function (b) {
              if (b && b.name) branches.push(b.name);
            });
          }
        }
      } catch (e3) {}
      if (!branches.length) branches = ["main", "master", "develop"];

      var selectedBranch = preferredBranch || detectCurrentBranchFromUrl() || branches[0] || "main";
      if (branches.indexOf(selectedBranch) === -1) {
        branches.unshift(selectedBranch);
      }

      var files = [];
      try {
        var rTree = await fetch(
          "/api/v1/repos/" + selectedRepo + "/git/trees/" + encodeURIComponent(selectedBranch) + "?recursive=1",
          { credentials: "same-origin" }
        );
        if (rTree.ok) {
          var treeData = await rTree.json();
          if (treeData && Array.isArray(treeData.tree)) {
            treeData.tree.forEach(function (node) {
              if (node && node.type === "blob" && node.path) {
                files.push(node.path);
              }
            });
          }
        }
      } catch (e4) {}

      return {
        repositories: repoList,
        selected_repo: selectedRepo,
        branches: branches,
        selected_branch: selectedBranch,
        files: files,
      };
    } catch (err) {
      return null;
    }
  }

  async function loadExplorerData(preferredRepo, preferredBranch) {
    var lang = getActiveLang();
    var t = TERMINAL_I18N[lang];
    var repoSel = document.getElementById("bantu-cmd-repo-select");
    var branchSel = document.getElementById("bantu-cmd-branch-select");
    var fileSel = document.getElementById("bantu-cmd-file-select");
    if (!repoSel || !branchSel || !fileSel) return;

    var q = [];
    if (preferredRepo) q.push("repo=" + encodeURIComponent(preferredRepo));
    if (preferredBranch) q.push("branch=" + encodeURIComponent(preferredBranch));
    var qs = q.length ? "?" + q.join("&") : "";

    try {
      var liveGitea = await fetchLiveGiteaData(preferredRepo, preferredBranch);
      var backendData = null;
      try {
        backendData = await fetchApiWithFallback("/api/forge/repo-explorer/" + qs, {
          method: "GET",
          headers: { Accept: "application/json" },
        });
      } catch (beErr) {}

      var data = liveGitea || backendData;
      if (!data) throw new Error("No explorer source");

      // Merge repositories from live Gitea and backend
      var mergedRepos = [];
      var seenRepos = {};
      if (liveGitea && Array.isArray(liveGitea.repositories)) {
        liveGitea.repositories.forEach(function (r) {
          if (r && r.full_name && !seenRepos[r.full_name]) {
            seenRepos[r.full_name] = true;
            mergedRepos.push(r);
          }
        });
      }
      if (backendData && Array.isArray(backendData.repositories)) {
        backendData.repositories.forEach(function (r) {
          if (r && r.full_name && !seenRepos[r.full_name]) {
            seenRepos[r.full_name] = true;
            mergedRepos.push(r);
          }
        });
      }

      var selectedRepo =
        preferredRepo ||
        (liveGitea && liveGitea.selected_repo) ||
        (backendData && backendData.selected_repo) ||
        (mergedRepos[0] && mergedRepos[0].full_name) ||
        "sovereign-org/afri-fintech-gateway";

      repoSel.innerHTML = "";
      mergedRepos.forEach(function (r) {
        var opt = document.createElement("option");
        opt.value = r.full_name;
        opt.textContent = r.full_name;
        if (r.full_name === selectedRepo) opt.selected = true;
        repoSel.appendChild(opt);
      });
      state.repo = selectedRepo;

      var branches =
        (liveGitea && liveGitea.branches && liveGitea.branches.length ? liveGitea.branches : null) ||
        (backendData && backendData.branches) ||
        ["main"];
      var selectedBranch =
        preferredBranch ||
        (liveGitea && liveGitea.selected_branch) ||
        (backendData && backendData.selected_branch) ||
        branches[0] ||
        "main";

      branchSel.innerHTML = "";
      branches.forEach(function (b) {
        var opt = document.createElement("option");
        opt.value = b;
        opt.textContent = b;
        if (b === selectedBranch) opt.selected = true;
        branchSel.appendChild(opt);
      });
      state.branch = selectedBranch;

      var files =
        (liveGitea && liveGitea.files && liveGitea.files.length ? liveGitea.files : null) ||
        (backendData && backendData.files) ||
        [];
      state.filesList = files;

      fileSel.innerHTML = "";
      var allOpt = document.createElement("option");
      allOpt.value = "*";
      allOpt.textContent = t.allFiles;
      fileSel.appendChild(allOpt);

      files.forEach(function (f) {
        var opt = document.createElement("option");
        opt.value = f;
        opt.textContent = f;
        fileSel.appendChild(opt);
      });
      state.file = "*";
      updatePromptPreview();
    } catch (e) {
      var fallbackRepo = preferredRepo || detectCurrentRepoFromUrl() || "sovereign-org/afri-fintech-gateway";
      repoSel.innerHTML = '<option value="' + escapeHtml(fallbackRepo) + '">' + escapeHtml(fallbackRepo) + "</option>";
      branchSel.innerHTML = '<option value="main">main</option><option value="develop">develop</option>';
      fileSel.innerHTML =
        '<option value="*">' +
        escapeHtml(t.allFiles) +
        "</option>" +
        '<option value="workbench_security_audit.py">workbench_security_audit.py</option>' +
        '<option value="Dockerfile">Dockerfile</option>' +
        '<option value=".gitlab-ci.yml">.gitlab-ci.yml</option>' +
        '<option value="payment_gateway.js">payment_gateway.js</option>';
      state.repo = fallbackRepo;
      state.branch = "main";
      state.file = "*";
      updatePromptPreview();
    }
  }

  async function fetchGiteaRepoFilesContent(repo, branch, targetFile) {
    if (!isGiteaHost() || !repo) return [];
    var targets = [];
    if (targetFile && targetFile !== "*") {
      targets = [targetFile];
    } else if (Array.isArray(state.filesList) && state.filesList.length) {
      targets = state.filesList
        .filter(function (f) {
          return !/\.(png|jpg|jpeg|gif|ico|woff|woff2|ttf|pdf|zip|tar|gz)$/i.test(f);
        })
        .slice(0, 8);
    }
    repo = normalizeRepoFullName(repo);
    if (!repo) return [];
    var results = [];
    for (var i = 0; i < targets.length; i++) {
      var fp = targets[i];
      try {
        var rawUrl = "/" + repo + "/raw/branch/" + encodeURIComponent(branch) + "/" + fp;
        var res = await fetch(rawUrl, { credentials: "same-origin" });
        if (res.ok) {
          var txt = await res.text();
          if (txt && txt.indexOf("<!DOCTYPE html>") === -1) {
            results.push({ path: fp, content: txt.slice(0, 6000) });
          }
        }
      } catch (e) {}
    }
    return results;
  }

  async function executeCommandAnalysis() {
    var lang = getActiveLang();
    var t = TERMINAL_I18N[lang];
    var resultsPanel = document.getElementById("bantu-cmd-results-panel");
    if (!resultsPanel) return;

    resultsPanel.style.display = "block";
    var waitMsg = state.action === "gemma" ? t.runningGemma : t.runningSecurity;
    resultsPanel.innerHTML =
      '<div style="padding:18px;background:#020617;border:1px solid #1e293b;border-radius:8px;color:#00e5ff;font-family:monospace;font-size:13px;">' +
      "&gt; " +
      escapeHtml(waitMsg) +
      " [" +
      escapeHtml(state.repo) +
      " @ " +
      escapeHtml(state.branch) +
      " : " +
      escapeHtml(state.file) +
      "]..." +
      "</div>";

    notifyToast(
      (state.action === "gemma" ? t.toastStartGemma : t.toastStartSecurity) +
        state.repo +
        " (" +
        state.branch +
        ")",
      "info"
    );

    try {
      var liveFilesContent = await fetchGiteaRepoFilesContent(state.repo, state.branch, state.file);
      var payload = {
        action: state.action,
        repository: state.repo,
        branch: state.branch,
        file_path: state.file,
        lang: lang,
      };
      if (liveFilesContent && liveFilesContent.length) {
        payload.files_content = liveFilesContent;
      }

      var data = await fetchApiWithFallback("/api/forge/repo-analyze/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "X-Bantu-Workbench": "gitea-repo-terminal",
        },
        body: JSON.stringify(payload),
      });

      if (state.action === "gemma") {
        resultsPanel.innerHTML =
          '<div style="margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">' +
          '  <span style="font-family:monospace;font-size:12px;color:#10b981;">$ ' +
          escapeHtml(data.command || "gemma-review") +
          "</span>" +
          '  <span style="font-size:11px;padding:2px 8px;border-radius:4px;background:rgba(0,229,255,0.15);color:#00e5ff;border:1px solid #00e5ff;">' +
          escapeHtml(data.model || "Gemma 2 2B") +
          " (" +
          escapeHtml(lang.toUpperCase()) +
          ")</span>" +
          "</div>" +
          '<div style="padding:16px;background:#020617;border:1px solid #1e293b;border-radius:8px;white-space:pre-wrap;font-family:monospace;font-size:13px;line-height:1.65;color:#e2e8f0;">' +
          escapeHtml(data.response || "") +
          "</div>";
        notifyToast(t.toastDoneGemma, "success");
      } else {
        var score = typeof data.sovereignty_score === "number" ? data.sovereignty_score : 100;
        var scoreColor = score >= 80 ? "#10b981" : score >= 50 ? "#f59e0b" : "#ef4444";
        var issues = data.issues || [];
        var issuesHtml = "";
        if (!issues.length) {
          issuesHtml =
            '<div style="padding:14px;background:rgba(16,185,129,0.1);border:1px solid #10b981;border-radius:8px;color:#a7f3d0;font-weight:600;">' +
            escapeHtml(t.noIssues) +
            "</div>";
        } else {
          issues.forEach(function (iss) {
            var sev = (iss.severity || "MEDIUM").toUpperCase();
            var sevCol = sev === "CRITICAL" ? "#ef4444" : sev === "HIGH" ? "#f59e0b" : "#3b82f6";
            issuesHtml +=
              '<div style="padding:12px;margin-bottom:8px;background:#020617;border-left:4px solid ' +
              sevCol +
              ';border-radius:6px;border-top:1px solid #1e293b;border-right:1px solid #1e293b;border-bottom:1px solid #1e293b;">' +
              '  <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">' +
              '    <strong style="color:#f8fafc;font-size:13px;">' +
              escapeHtml(iss.description) +
              "</strong>" +
              '    <span style="font-size:11px;padding:2px 7px;border-radius:4px;font-weight:700;background:rgba(255,255,255,0.06);color:' +
              sevCol +
              ';">' +
              escapeHtml(sev) +
              " | " +
              escapeHtml(iss.file || "") +
              " (" +
              escapeHtml(t.lineLabel) +
              " " +
              escapeHtml(iss.line || 1) +
              ")</span>" +
              "  </div>" +
              (iss.snippet
                ? '<pre style="margin:6px 0;padding:6px 8px;background:#070e1e;border-radius:4px;color:#94a3b8;font-size:12px;overflow-x:auto;">' +
                  escapeHtml(iss.snippet) +
                  "</pre>"
                : "") +
              (iss.recommendation
                ? '<div style="font-size:12px;color:#10b981;margin-top:4px;"><strong>' +
                  escapeHtml(t.recPrefix) +
                  "</strong> " +
                  escapeHtml(iss.recommendation) +
                  "</div>"
                : "") +
              "</div>";
          });
        }

        resultsPanel.innerHTML =
          '<div style="margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">' +
          '  <span style="font-family:monospace;font-size:12px;color:#10b981;">$ ' +
          escapeHtml(data.command || "security-audit") +
          "</span>" +
          '  <span style="font-size:11px;color:#94a3b8;">' +
          escapeHtml(t.filesScannedLabel) +
          ": " +
          escapeHtml((data.files_analyzed || []).length) +
          "</span>" +
          "</div>" +
          '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:14px;">' +
          '  <div style="padding:10px;background:#020617;border:1px solid #1e293b;border-radius:8px;text-align:center;">' +
          '    <div style="font-size:22px;font-weight:800;color:' +
          scoreColor +
          ';">' +
          score +
          "%</div>" +
          '    <div style="font-size:11px;color:#94a3b8;">' +
          escapeHtml(t.scoreLabel) +
          "</div>" +
          "  </div>" +
          '  <div style="padding:10px;background:#020617;border:1px solid #1e293b;border-radius:8px;text-align:center;">' +
          '    <div style="font-size:20px;font-weight:800;color:#ef4444;">' +
          escapeHtml(data.critical || 0) +
          "</div>" +
          '    <div style="font-size:11px;color:#94a3b8;">' +
          escapeHtml(t.criticalLabel) +
          "</div>" +
          "  </div>" +
          '  <div style="padding:10px;background:#020617;border:1px solid #1e293b;border-radius:8px;text-align:center;">' +
          '    <div style="font-size:20px;font-weight:800;color:#f59e0b;">' +
          escapeHtml(data.high || 0) +
          "</div>" +
          '    <div style="font-size:11px;color:#94a3b8;">' +
          escapeHtml(t.highLabel) +
          "</div>" +
          "  </div>" +
          '  <div style="padding:10px;background:#020617;border:1px solid #1e293b;border-radius:8px;text-align:center;">' +
          '    <div style="font-size:20px;font-weight:800;color:#3b82f6;">' +
          escapeHtml(data.medium || 0) +
          "</div>" +
          '    <div style="font-size:11px;color:#94a3b8;">' +
          escapeHtml(t.mediumLabel) +
          "</div>" +
          "  </div>" +
          "</div>" +
          issuesHtml;

        notifyToast(t.toastDoneSecurity + score + "%", "success");
      }
    } catch (err) {
      resultsPanel.innerHTML =
        '<div style="padding:14px;background:rgba(239,68,68,0.12);border:1px solid #ef4444;border-radius:8px;color:#fca5a5;">' +
        escapeHtml(t.toastError + (err && err.message ? err.message : String(err))) +
        "</div>";
      notifyToast(t.toastError + (err && err.message ? err.message : String(err)), "error");
    }
  }

  function openCommandTerminal(action, preferredRepo, preferredBranch, autoExec) {
    injectStyles();
    var modal = ensureModalCreated();
    setTerminalAction(action || "security");
    modal.classList.add("open");

    var targetRepo = preferredRepo || detectCurrentRepoFromUrl() || "";
    var targetBranch = preferredBranch || detectCurrentBranchFromUrl() || "";
    loadExplorerData(targetRepo, targetBranch).then(function () {
      if (autoExec) {
        executeCommandAnalysis();
      }
    });
  }

  function closeCommandTerminal() {
    var modal = document.getElementById("bantu-command-terminal-modal");
    if (modal) modal.classList.remove("open");
  }

  function buildProButtonsHtml(t, secId, gemmaId) {
    return (
      '<button type="button" ' +
      (secId ? 'id="' + secId + '" ' : "") +
      'class="bantu-pro-action-btn bantu-pro-btn-security" title="Run Security Audit (SAST)">' +
      '  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>' +
      '  <span class="bantu-i18n-security-label">' +
      escapeHtml(t.btnSecurity) +
      "</span>" +
      "</button>" +
      '<button type="button" ' +
      (gemmaId ? 'id="' + gemmaId + '" ' : "") +
      'class="bantu-pro-action-btn bantu-pro-btn-gemma" title="Ask Gemma Review (AI)">' +
      '  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="4" y="4" width="16" height="16" rx="2"></rect><rect x="9" y="9" width="6" height="6"></rect></svg>' +
      '  <span class="bantu-i18n-gemma-label">' +
      escapeHtml(t.btnGemma) +
      "</span>" +
      "</button>"
    );
  }

  function injectNavbarButtonsAfterLogo() {
    injectStyles();
    var lang = getActiveLang();
    var t = TERMINAL_I18N[lang];

    // 1. Gitea 1.22 Headbar (nav#navbar .navbar-left) or legacy (.ui.menu.navbar)
    // Placed right after [Explore] on the exact same horizontal alignment with the logo
    var giteaLeftNav = document.querySelector(
      "nav#navbar .navbar-left, #navbar .navbar-left, .ui.menu.navbar .navbar-left, nav#navbar, #navbar, .ui.menu.navbar"
    );
    if (giteaLeftNav && !document.getElementById("bantu-gitea-nav-pro-actions")) {
      var group = document.createElement("div");
      group.id = "bantu-gitea-nav-pro-actions";
      group.className = "item bantu-pro-actions-group";
      group.innerHTML = buildProButtonsHtml(t, "bantu-nav-security-btn", "bantu-nav-gemma-btn");

      var exploreItem = giteaLeftNav.querySelector('a.item[href*="/explore"], a[href*="/explore"]');
      var brandItem = giteaLeftNav.querySelector("#navbar-logo, .item.brand, a.item[href='/']");

      if (exploreItem) {
        exploreItem.insertAdjacentElement("afterend", group);
      } else if (brandItem) {
        brandItem.insertAdjacentElement("afterend", group);
      } else {
        giteaLeftNav.appendChild(group);
      }

      group.querySelector("#bantu-nav-security-btn").addEventListener("click", function (e) {
        e.preventDefault();
        openCommandTerminal("security", detectCurrentRepoFromUrl(), detectCurrentBranchFromUrl());
      });
      group.querySelector("#bantu-nav-gemma-btn").addEventListener("click", function (e) {
        e.preventDefault();
        openCommandTerminal("gemma", detectCurrentRepoFromUrl(), detectCurrentBranchFromUrl());
      });
    }

    // 2. Django Portal Navbar (.navbar .navbar-container) right after .brand
    var djangoBrand = document.querySelector(".navbar .navbar-container > .brand");
    if (djangoBrand && !document.getElementById("bantu-django-nav-pro-actions")) {
      var dGroup = document.createElement("div");
      dGroup.id = "bantu-django-nav-pro-actions";
      dGroup.className = "bantu-pro-actions-group";
      dGroup.innerHTML = buildProButtonsHtml(t, "bantu-django-security-btn", "bantu-django-gemma-btn");
      djangoBrand.insertAdjacentElement("afterend", dGroup);

      dGroup.querySelector("#bantu-django-security-btn").addEventListener("click", function () {
        openCommandTerminal("security", "", "");
      });
      dGroup.querySelector("#bantu-django-gemma-btn").addEventListener("click", function () {
        openCommandTerminal("gemma", "", "");
      });
    }

    // 2b. Also expose pro buttons inside Mobile Nav Drawer (#navDrawer .nav-drawer-links)
    var drawerLinks = document.querySelector("#navDrawer .nav-drawer-links");
    if (drawerLinks && !document.getElementById("bantu-drawer-pro-actions")) {
      var drawerGroup = document.createElement("div");
      drawerGroup.id = "bantu-drawer-pro-actions";
      drawerGroup.style.cssText = "display:flex;flex-direction:column;gap:8px;margin-top:8px;";
      drawerGroup.innerHTML = buildProButtonsHtml(t, "bantu-drawer-security-btn", "bantu-drawer-gemma-btn");
      drawerLinks.appendChild(drawerGroup);

      drawerGroup.querySelector("#bantu-drawer-security-btn").addEventListener("click", function () {
        openCommandTerminal("security", "", "");
      });
      drawerGroup.querySelector("#bantu-drawer-gemma-btn").addEventListener("click", function () {
        openCommandTerminal("gemma", "", "");
      });
    }

    // 3. Inject into Gitea Repository Page Header & Dashboard Repo Lists
    injectGiteaRepoAndDashboardActions();
  }

  function injectGiteaRepoAndDashboardActions() {
    if (!isGiteaHost()) return;
    var lang = getActiveLang();
    var t = TERMINAL_I18N[lang];
    var currentRepo = detectCurrentRepoFromUrl();
    var currentBranch = detectCurrentBranchFromUrl();

    // A. On any Gitea Repository Page (/owner/repo), inject into repo header if not already present
    if (
      currentRepo &&
      !document.getElementById("repo-run-security-btn") &&
      !document.getElementById("bantu-gitea-repo-header-actions")
    ) {
      var repoHeaderTarget = document.querySelector(
        ".repo-button-row, .repo-header .flex-item-trailing, .repo-title-wrap, .repository .ui.container > .ui.grid"
      );
      if (repoHeaderTarget) {
        var rGroup = document.createElement("div");
        rGroup.id = "bantu-gitea-repo-header-actions";
        rGroup.className = "bantu-pro-actions-group";
        rGroup.innerHTML = buildProButtonsHtml(t, "repo-run-security-btn", "repo-ask-gemma-btn");
        repoHeaderTarget.insertBefore(rGroup, repoHeaderTarget.firstChild);

        rGroup.querySelector("#repo-run-security-btn").addEventListener("click", function (e) {
          e.preventDefault();
          openCommandTerminal("security", currentRepo, currentBranch, true);
        });
        rGroup.querySelector("#repo-ask-gemma-btn").addEventListener("click", function (e) {
          e.preventDefault();
          openCommandTerminal("gemma", currentRepo, currentBranch, true);
        });
      }
    }

    // C. On Gitea Branches List Page (/owner/repo/branches), attach action buttons to each branch item
    if (window.location.pathname.indexOf("/branches") !== -1 || document.querySelector(".branch-list, .repository.branches")) {
      var branchItems = document.querySelectorAll(
        "table tbody tr, .ui.table tbody tr, .branch-row, .flex-list .flex-item"
      );
      branchItems.forEach(function (row) {
        if (row.getAttribute("data-bantu-branch-actions") === "1") return;
        var bLink = row.querySelector("a[href*='/src/branch/'], a.branch-name, td.name a");
        if (!bLink) return;
        var bHref = bLink.getAttribute("href") || "";
        var bMatch = bHref.match(/\/src\/branch\/([^/?#]+)/);
        var branchName = bMatch ? decodeURIComponent(bMatch[1]) : bLink.textContent.trim();
        if (!branchName) return;
        row.setAttribute("data-bantu-branch-actions", "1");

        var targetCell = row.querySelector("td:last-child, .flex-item-trailing") || bLink.parentElement;
        if (!targetCell || targetCell.querySelector(".bantu-branch-actions-wrap")) return;

        var wrap = document.createElement("span");
        wrap.className = "bantu-branch-actions-wrap";
        wrap.style.cssText = "display:inline-flex;align-items:center;gap:6px;margin-left:8px;vertical-align:middle;";
        wrap.innerHTML =
          '<button type="button" class="bantu-pro-action-btn bantu-pro-btn-security" style="padding:2px 8px !important;font-size:11px !important;" title="Run Security Review sur la branche ' +
          escapeHtml(branchName) +
          '">' +
          '  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg> ' +
          '  <span>Review</span>' +
          "</button>" +
          '<button type="button" class="bantu-pro-action-btn bantu-pro-btn-gemma" style="padding:2px 8px !important;font-size:11px !important;" title="Ask Gemma Review sur la branche ' +
          escapeHtml(branchName) +
          '">' +
          '  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="4" y="4" width="16" height="16" rx="2"></rect><rect x="9" y="9" width="6" height="6"></rect></svg> ' +
          '  <span>Gemma</span>' +
          "</button>";

        var bBtns = wrap.querySelectorAll("button");
        bBtns[0].addEventListener("click", function (e) {
          e.preventDefault();
          e.stopPropagation();
          openCommandTerminal("security", currentRepo, branchName, true);
        });
        bBtns[1].addEventListener("click", function (e) {
          e.preventDefault();
          e.stopPropagation();
          openCommandTerminal("gemma", currentRepo, branchName, true);
        });
        targetCell.appendChild(wrap);
      });
    }

    // B. On Gitea Dashboard & Explore repository lists, attach quick action buttons to each repo row
    var repoLinks = document.querySelectorAll(
      ".dashboard-repos a[href], .repo-owner-name-list a[href], .flex-list .flex-item-title a[href], .ui.repository.list .item a.name[href]"
    );
    repoLinks.forEach(function (link) {
      if (link.getAttribute("data-bantu-actions-bound") === "1") return;
      var href = link.getAttribute("href") || "";
      var m = href.match(/^\/([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+)$/);
      if (!m) return;
      var fullRepo = m[1] + "/" + m[2];
      link.setAttribute("data-bantu-actions-bound", "1");

      var row = link.closest("li, .flex-item, .item") || link.parentElement;
      if (!row || row.querySelector(".bantu-inline-repo-actions")) return;

      var inlineBox = document.createElement("span");
      inlineBox.className = "bantu-inline-repo-actions";
      inlineBox.style.cssText = "display:inline-flex;align-items:center;gap:4px;margin-left:8px;vertical-align:middle;";
      inlineBox.innerHTML =
        '<button type="button" class="bantu-pro-action-btn bantu-pro-btn-security" style="padding:2px 7px !important;font-size:10px !important;" title="Run Security Audit on ' +
        escapeHtml(fullRepo) +
        '">SAST</button>' +
        '<button type="button" class="bantu-pro-action-btn bantu-pro-btn-gemma" style="padding:2px 7px !important;font-size:10px !important;" title="Ask Gemma Review on ' +
        escapeHtml(fullRepo) +
        '">Gemma</button>';

      var btns = inlineBox.querySelectorAll("button");
      btns[0].addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        openCommandTerminal("security", fullRepo, "");
      });
      btns[1].addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        openCommandTerminal("gemma", fullRepo, "");
      });

      link.insertAdjacentElement("afterend", inlineBox);
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeCommandTerminal();
  });

  window.openBantuCommandTerminal = openCommandTerminal;
  window.closeBantuCommandTerminal = closeCommandTerminal;
  window.refreshBantuTerminalLang = applyTerminalI18n;

  function boot() {
    injectNavbarButtonsAfterLogo();
    // Observe Vue/HTMX dynamic renders on Gitea Dashboard
    if (typeof MutationObserver !== "undefined" && document.body) {
      var obs = new MutationObserver(function () {
        if (!document.getElementById("bantu-gitea-nav-pro-actions")) {
          injectNavbarButtonsAfterLogo();
        } else {
          injectGiteaRepoAndDashboardActions();
        }
      });
      obs.observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
