/**
 * BANTUDEVLAB - Sovereign Command Prompt Terminal & Top-Up Analysis Interface
 * Provides:
 * 1. Pro Action Buttons ("Run Security Audit" & "Ask Gemma Review") right after the Logo in the top navbar
 *    and on every Gitea Repository header / Dashboard repo row.
 * 2. Structured Command Prompt Terminal (Zero free-text input):
 *    - '+' Button to configure target options:
 *      * Repository selector (--repo)
 *      * Branch selector (--branch)
 *      * File or All Files (*) selector (--target)
 *    - 'Execute' Button to run SAST Security Audit or Gemma 2 2B / 5B AI Review on the selected repo/branch/files.
 * 3. Top-Up Results Interface & Multi-lingual synchronization (fr, en, sw, pt).
 */
(function () {
  "use strict";

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
      runningGemma: "Consultation du moteur local Gemma 5B sur le dépôt...",
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
      runningGemma: "Querying local Gemma 5B AI engine on repository...",
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
      btnSecurity: "Run Security Audit",
      btnGemma: "Ask Gemma Review",
      termTitleSecurity: "KITUO HURU — RUN SECURITY AUDIT (SAST)",
      termTitleGemma: "KITUO HURU — ASK GEMMA REVIEW (AI)",
      plusTooltip: "Sanidi chaguo za amri (+ Hazina, Tawi, Faili)",
      lblRepo: "Hazina ya Git",
      lblBranch: "Tawi (Branch)",
      lblFile: "Faili Lengwa",
      allFiles: "* (Faili zote za hazina)",
      btnExecute: "Tekeleza",
      runningSecurity: "Inakagua usalama wa SAST kwenye hazina...",
      runningGemma: "Inachambua msimbo kupitia Gemma 5B AI...",
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
      btnSecurity: "Run Security Audit",
      btnGemma: "Ask Gemma Review",
      termTitleSecurity: "TERMINAL SOBERANO — RUN SECURITY AUDIT (SAST)",
      termTitleGemma: "TERMINAL SOBERANO — ASK GEMMA REVIEW (IA)",
      plusTooltip: "Configurar opções do comando (+ Repositório, Ramo, Ficheiro)",
      lblRepo: "Repositório Git",
      lblBranch: "Ramo (Branch)",
      lblFile: "Alvo / Ficheiro",
      allFiles: "* (Todos os ficheiros do repositório)",
      btnExecute: "Executar",
      runningSecurity: "A executar auditoria de segurança SAST no repositório...",
      runningGemma: "A consultar o motor local Gemma 5B IA no repositório...",
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
    ];
    var parts = path.split("/");
    if (parts.length >= 2 && reserved.indexOf(parts[0].toLowerCase()) === -1) {
      var repoClean = parts[1].replace(/\.git$/, "");
      return parts[0] + "/" + repoClean;
    }
    return "";
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
    optionsExpanded: true,
  };

  function injectStyles() {
    if (document.getElementById("bantu-cmd-terminal-styles")) return;
    var style = document.createElement("style");
    style.id = "bantu-cmd-terminal-styles";
    style.textContent =
      ".bantu-pro-actions-group{display:inline-flex;align-items:center;gap:6px;margin-left:10px;margin-right:8px;flex-wrap:wrap;}" +
      ".bantu-pro-action-btn{display:inline-flex;align-items:center;gap:6px;padding:5px 11px;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer;transition:all 0.15s ease;text-decoration:none;white-space:nowrap;line-height:1.2;font-family:inherit;}" +
      ".bantu-pro-btn-security{background:rgba(245,158,11,0.14);color:#f59e0b !important;border:1px solid rgba(245,158,11,0.55);}" +
      ".bantu-pro-btn-security:hover{background:#f59e0b;color:#020617 !important;box-shadow:0 0 12px rgba(245,158,11,0.45);}" +
      ".bantu-pro-btn-gemma{background:rgba(0,229,255,0.12);color:#00e5ff !important;border:1px solid rgba(0,229,255,0.5);}" +
      ".bantu-pro-btn-gemma:hover{background:#00e5ff;color:#020617 !important;box-shadow:0 0 12px rgba(0,229,255,0.45);}" +
      "[data-theme='light'] .bantu-pro-btn-security{background:#fffbeb;color:#b45309 !important;border-color:#f59e0b;}" +
      "[data-theme='light'] .bantu-pro-btn-gemma{background:#eff6ff;color:#0051cc !important;border-color:#3b82f6;}" +
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
      "@media (max-width:768px){.bantu-term-options-bar{grid-template-columns:1fr;}.bantu-pro-actions-group{margin-left:4px;}}" +
      "@media (max-width:480px){.bantu-pro-action-btn span.bantu-btn-text-short{display:inline;}.bantu-term-prompt-row{padding:10px;}.bantu-term-exec-btn{width:100%;justify-content:center;}}";
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
      '      <button type="button" id="bantu-switch-mode-security" class="bantu-pro-action-btn bantu-pro-btn-security" style="padding:3px 9px;font-size:11px;">Run Security Audit</button>' +
      '      <button type="button" id="bantu-switch-mode-gemma" class="bantu-pro-action-btn bantu-pro-btn-gemma" style="padding:3px 9px;font-size:11px;">Ask Gemma Review</button>' +
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
      var data = await fetchApiWithFallback("/api/forge/repo-explorer/" + qs, {
        method: "GET",
        headers: { Accept: "application/json" },
      });

      var repos = data.repositories || [];
      repoSel.innerHTML = "";
      repos.forEach(function (r) {
        var opt = document.createElement("option");
        opt.value = r.full_name;
        opt.textContent = r.full_name;
        if (r.full_name === data.selected_repo) opt.selected = true;
        repoSel.appendChild(opt);
      });
      state.repo = data.selected_repo || (repos[0] && repos[0].full_name) || "sovereign-org/afri-fintech-gateway";

      var branches = data.branches || ["main"];
      branchSel.innerHTML = "";
      branches.forEach(function (b) {
        var opt = document.createElement("option");
        opt.value = b;
        opt.textContent = b;
        if (b === data.selected_branch) opt.selected = true;
        branchSel.appendChild(opt);
      });
      state.branch = data.selected_branch || branches[0] || "main";

      var files = data.files || [];
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
      var payload = {
        action: state.action,
        repository: state.repo,
        branch: state.branch,
        file_path: state.file,
        lang: lang,
      };
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
    loadExplorerData(targetRepo, preferredBranch || "").then(function () {
      if (autoExec) {
        executeCommandAnalysis();
      }
    });
  }

  function closeCommandTerminal() {
    var modal = document.getElementById("bantu-command-terminal-modal");
    if (modal) modal.classList.remove("open");
  }

  function injectNavbarButtonsAfterLogo() {
    injectStyles();
    var lang = getActiveLang();
    var t = TERMINAL_I18N[lang];

    // 1. Gitea Top Navbar (.ui.menu.navbar) right after the brand/logo
    var giteaNav = document.querySelector(".ui.menu.navbar");
    if (giteaNav && !document.getElementById("bantu-gitea-nav-pro-actions")) {
      var group = document.createElement("div");
      group.id = "bantu-gitea-nav-pro-actions";
      group.className = "bantu-pro-actions-group";
      group.innerHTML =
        '<button type="button" id="bantu-nav-security-btn" class="bantu-pro-action-btn bantu-pro-btn-security" title="Run Security Audit (SAST)">' +
        '  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>' +
        '  <span class="bantu-i18n-security-label">' +
        escapeHtml(t.btnSecurity) +
        "</span>" +
        "</button>" +
        '<button type="button" id="bantu-nav-gemma-btn" class="bantu-pro-action-btn bantu-pro-btn-gemma" title="Ask Gemma Review (AI)">' +
        '  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="4" y="4" width="16" height="16" rx="2"></rect><rect x="9" y="9" width="6" height="6"></rect></svg>' +
        '  <span class="bantu-i18n-gemma-label">' +
        escapeHtml(t.btnGemma) +
        "</span>" +
        "</button>";

      var brandItem = giteaNav.querySelector(".item.brand, a.item[href='/']");
      if (brandItem && brandItem.nextSibling) {
        brandItem.parentNode.insertBefore(group, brandItem.nextSibling);
      } else {
        giteaNav.insertBefore(group, giteaNav.firstChild);
      }

      group.querySelector("#bantu-nav-security-btn").addEventListener("click", function () {
        openCommandTerminal("security", detectCurrentRepoFromUrl(), "");
      });
      group.querySelector("#bantu-nav-gemma-btn").addEventListener("click", function () {
        openCommandTerminal("gemma", detectCurrentRepoFromUrl(), "");
      });
    }

    // 2. Django Portal Navbar (.navbar .navbar-container) right after .brand
    var djangoBrand = document.querySelector(".navbar .navbar-container > .brand");
    if (djangoBrand && !document.getElementById("bantu-django-nav-pro-actions")) {
      var dGroup = document.createElement("div");
      dGroup.id = "bantu-django-nav-pro-actions";
      dGroup.className = "bantu-pro-actions-group";
      dGroup.innerHTML =
        '<button type="button" class="bantu-pro-action-btn bantu-pro-btn-security" onclick="window.openBantuCommandTerminal(\'security\')">' +
        '  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>' +
        '  <span class="bantu-i18n-security-label">' +
        escapeHtml(t.btnSecurity) +
        "</span>" +
        "</button>" +
        '<button type="button" class="bantu-pro-action-btn bantu-pro-btn-gemma" onclick="window.openBantuCommandTerminal(\'gemma\')">' +
        '  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="4" y="4" width="16" height="16" rx="2"></rect><rect x="9" y="9" width="6" height="6"></rect></svg>' +
        '  <span class="bantu-i18n-gemma-label">' +
        escapeHtml(t.btnGemma) +
        "</span>" +
        "</button>";
      djangoBrand.parentNode.insertBefore(dGroup, djangoBrand.nextSibling);
    }
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeCommandTerminal();
  });

  window.openBantuCommandTerminal = openCommandTerminal;
  window.closeBantuCommandTerminal = closeCommandTerminal;
  window.refreshBantuTerminalLang = applyTerminalI18n;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectNavbarButtonsAfterLogo);
  } else {
    injectNavbarButtonsAfterLogo();
  }
})();
