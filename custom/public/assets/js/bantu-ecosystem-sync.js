(function () {
    const CHANNEL_NAME = 'bantu_ecosystem_sync';
    const GITEA_LANG_MAP = {
        'fr': 'fr-FR',
        'en': 'en-US',
        'sw': 'sw-KE',
        'pt': 'pt-PT'
    };
    const BANTU_LANG_MAP = {
        'fr-FR': 'fr',
        'en-US': 'en',
        'sw-KE': 'sw',
        'pt-PT': 'pt',
        'fr': 'fr',
        'en': 'en',
        'sw': 'sw',
        'pt': 'pt'
    };
    const SYNC_TOAST_I18N = {
        'fr': {
            langChanged: 'Langue activee : Francais',
            themeDark: 'Theme sombre active',
            themeLight: 'Theme clair active',
            btnDark: 'Sombre',
            btnLight: 'Clair'
        },
        'en': {
            langChanged: 'Language activated: English',
            themeDark: 'Dark theme activated',
            themeLight: 'Light theme activated',
            btnDark: 'Dark',
            btnLight: 'Light'
        },
        'sw': {
            langChanged: 'Lugha imewashwa: Kiswahili',
            themeDark: 'Mandhari meusi yamewashwa',
            themeLight: 'Mandhari meupe yamewashwa',
            btnDark: 'Giza',
            btnLight: 'Mwanga'
        },
        'pt': {
            langChanged: 'Idioma ativado: Portugues',
            themeDark: 'Tema escuro ativado',
            themeLight: 'Tema claro ativado',
            btnDark: 'Escuro',
            btnLight: 'Claro'
        }
    };

    function showEcosystemNotification(message, type) {
        if (typeof window.showToast === 'function') {
            window.showToast(message, type || 'info', 2500);
            return;
        }
        try {
            let box = document.getElementById('bantu-floating-toast-box');
            if (!box) {
                box = document.createElement('div');
                box.id = 'bantu-floating-toast-box';
                box.style.position = 'fixed';
                box.style.top = '68px';
                box.style.right = '20px';
                box.style.zIndex = '100005';
                box.style.display = 'flex';
                box.style.flexDirection = 'column';
                box.style.gap = '8px';
                document.body.appendChild(box);
            }
            const item = document.createElement('div');
            const isDark = getCurrentTheme() === 'dark';
            item.style.background = isDark ? '#070e1e' : '#ffffff';
            item.style.color = isDark ? '#f8fafc' : '#0f172a';
            item.style.border = '1px solid ' + (type === 'success' ? '#10b981' : '#00e5ff');
            item.style.borderLeft = '4px solid ' + (type === 'success' ? '#10b981' : '#00e5ff');
            item.style.borderRadius = '8px';
            item.style.padding = '10px 16px';
            item.style.fontSize = '13px';
            item.style.fontWeight = '600';
            item.style.boxShadow = '0 10px 25px rgba(0,0,0,0.45)';
            item.textContent = message;
            box.appendChild(item);
            setTimeout(function () {
                if (item.parentElement) item.remove();
            }, 2500);
        } catch (e) {}
    }

    let channel = null;
    try {
        if (typeof BroadcastChannel !== 'undefined') {
            channel = new BroadcastChannel(CHANNEL_NAME);
        }
    } catch (e) {}

    function getCookie(name) {
        const m = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'));
        return m ? decodeURIComponent(m[2]) : null;
    }

    function setCookie(name, val) {
        document.cookie = name + '=' + encodeURIComponent(val) + ';path=/;max-age=31536000';
        if (window.location.hostname && window.location.hostname.endsWith('cybersocle.site')) {
            document.cookie = name + '=' + encodeURIComponent(val) + ';domain=.cybersocle.site;path=/;max-age=31536000;SameSite=Lax';
        }
    }

    function getCurrentTheme() {
        const docTheme = document.documentElement.getAttribute('data-theme');
        if (docTheme) return docTheme;
        let lsTheme = null;
        try {
            lsTheme = localStorage.getItem('bantu_theme');
        } catch(e) {}
        if (lsTheme) return lsTheme;
        const bCookie = getCookie('bantu_theme');
        if (bCookie) return bCookie;
        const gCookie = getCookie('theme') || getCookie('gitea_theme');
        if (gCookie) {
            return (gCookie.includes('dark') || gCookie === 'github-dark') ? 'dark' : 'light';
        }
        return 'dark';
    }

    function getCurrentLang() {
        const fromCookie = getCookie('bantu_lang') || getCookie('django_language');
        if (fromCookie) return fromCookie;
        const giteaCookie = getCookie('lang');
        if (giteaCookie && BANTU_LANG_MAP[giteaCookie]) return BANTU_LANG_MAP[giteaCookie];
        return 'fr';
    }

    // Publish theme/lang change to all ecosystems
    window.syncEcosystemChange = function (newTheme, newLang) {
        const theme = newTheme || getCurrentTheme();
        const lang = newLang || getCurrentLang();
        const giteaLang = GITEA_LANG_MAP[lang] || 'fr-FR';
        const giteaTheme = (theme === 'light') ? 'github' : 'github-dark';
        const ts = Date.now();

        // 1. Write shared cookies across localhost (accessible to ports 8001, 3001, 3002)
        setCookie('bantu_theme', theme);
        setCookie('theme', giteaTheme);
        setCookie('gitea_theme', giteaTheme);
        setCookie('bantu_lang', lang);
        setCookie('django_language', lang);
        setCookie('lang', giteaLang);
        setCookie('bantu_sync_ts', ts.toString());

        // 2. Write to localStorage and sessionStorage for post-reload notification
        try {
            localStorage.setItem('bantu_theme', theme);
            localStorage.setItem('bantu_lang', lang);
            localStorage.setItem('bantu_gitea_lang', giteaLang);
            localStorage.setItem('bantu_sync_ts', ts.toString());
            if (newLang) {
                sessionStorage.setItem('bantu_lang_toast', lang);
            }
        } catch (e) {}

        // 3. Broadcast channel message
        if (channel) {
            try {
                channel.postMessage({ type: 'ECOSYSTEM_SYNC', theme, lang, giteaLang, giteaTheme, ts });
            } catch (e) {}
        }

        // 4. Update current page DOM immediately
        applyThemeLocally(theme);
        updateCrossLinks(theme, lang);

        if (newTheme && !newLang) {
            const tDict = SYNC_TOAST_I18N[lang] || SYNC_TOAST_I18N.fr;
            showEcosystemNotification(newTheme === 'light' ? tDict.themeLight : tDict.themeDark, 'info');
        }
    };

    function applyThemeLocally(theme) {
        document.documentElement.setAttribute('data-theme', theme);

        // Update Anti-FOUC critical styling immediately
        const antiFouc = document.getElementById('bantu-anti-fouc-critical');
        if (antiFouc) {
            const bgBody = (theme === 'dark') ? '#020617' : '#ffffff';
            const colorBody = (theme === 'dark') ? '#f8fafc' : '#0f172a';
            antiFouc.innerHTML = 'html, body, .full.height, #wrapper, .page-content { background-color: ' + bgBody + ' !important; color: ' + colorBody + ' !important; }';
        }

        // Gitea stylesheet live swap
        document.querySelectorAll('link[rel="stylesheet"]').forEach(l => {
            if (l.href && l.href.includes('theme-github')) {
                const targetHref = (theme === 'light') ? 
                    l.href.replace('theme-github-dark.css', 'theme-github.css') : 
                    l.href.replace('theme-github.css', 'theme-github-dark.css');
                if (l.href !== targetHref) l.href = targetHref;
            }
        });

        // BantuDevLab theme icon toggle
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) {
            themeIcon.innerHTML = (theme === 'light') ? 
                '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>' :
                '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
        }

        // Gitea theme toggle button text & icon update
        const giteaThemeBtn = document.getElementById('gitea-theme-toggle-btn');
        if (giteaThemeBtn) {
            const curLang = getCurrentLang();
            const tDict = SYNC_TOAST_I18N[curLang] || SYNC_TOAST_I18N.fr;
            giteaThemeBtn.innerHTML = (theme === 'dark') ?
                '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg> <span>' + tDict.btnLight + '</span>' :
                '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0070f3" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg> <span>' + tDict.btnDark + '</span>';
        }
    }

    function updateCrossLinks(theme, lang) {
        const giteaLang = GITEA_LANG_MAP[lang] || 'fr-FR';
        const giteaTheme = (theme === 'light') ? 'github' : 'github-dark';

        document.querySelectorAll('a').forEach(a => {
            const h = a.href || '';
            const isGitea = h.includes(':3002') || h.includes('git.cybersocle.site') || h.includes('gitea.cybersocle.site') || h.includes('/user/login') || h.includes('/user/sign_up');
            if (isGitea || h.includes(':3001') || h.includes(':8001') || h.includes(':8002') || h.includes('cybersocle.site')) {
                try {
                    const u = new URL(h, window.location.origin);
                    u.searchParams.set('lang', (isGitea ? giteaLang : lang));
                    u.searchParams.set('theme', (isGitea ? giteaTheme : theme));
                    a.href = u.toString();
                } catch (e) {}
            }
        });
    }

    let lastKnownTheme = getCurrentTheme();
    let lastKnownLang = getCurrentLang();

    function checkRemoteState() {
        const cookieTheme = getCookie('bantu_theme') || (getCookie('theme') && getCookie('theme').includes('light') ? 'light' : 'dark');
        let cookieLang = getCookie('bantu_lang') || getCookie('django_language');
        if (!cookieLang && getCookie('lang')) {
            cookieLang = BANTU_LANG_MAP[getCookie('lang')] || 'fr';
        }

        let needsLangReload = false;
        if (cookieTheme && cookieTheme !== lastKnownTheme) {
            lastKnownTheme = cookieTheme;
            applyThemeLocally(cookieTheme);
        }

        if (cookieLang && cookieLang !== lastKnownLang) {
            lastKnownLang = cookieLang;
            try { sessionStorage.setItem('bantu_lang_toast', cookieLang); } catch (e) {}
            needsLangReload = true;
        }

        if (needsLangReload) {
            window.location.reload();
        }
    }

    if (channel) {
        channel.onmessage = function (ev) {
            if (ev.data && ev.data.type === 'ECOSYSTEM_SYNC') {
                const { theme, lang } = ev.data;
                if (theme && theme !== lastKnownTheme) {
                    lastKnownTheme = theme;
                    applyThemeLocally(theme);
                }
                if (lang && lang !== lastKnownLang) {
                    lastKnownLang = lang;
                    try { sessionStorage.setItem('bantu_lang_toast', lang); } catch (e) {}
                    window.location.reload();
                }
            }
        };
    }

    document.addEventListener('visibilitychange', function () {
        if (!document.hidden) {
            checkRemoteState();
        }
    });

    window.addEventListener('focus', checkRemoteState);
    setInterval(checkRemoteState, 1500);

    document.addEventListener('DOMContentLoaded', function () {
        applyThemeLocally(lastKnownTheme);
        updateCrossLinks(lastKnownTheme, lastKnownLang);
        try {
            const pendingToastLang = sessionStorage.getItem('bantu_lang_toast');
            if (pendingToastLang) {
                sessionStorage.removeItem('bantu_lang_toast');
                const tDict = SYNC_TOAST_I18N[pendingToastLang] || SYNC_TOAST_I18N.fr;
                setTimeout(function () {
                    showEcosystemNotification(tDict.langChanged, 'success');
                }, 150);
            }
        } catch (e) {}
    });
})();
