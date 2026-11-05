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

        // 2. Write to localStorage
        try {
            localStorage.setItem('bantu_theme', theme);
            localStorage.setItem('bantu_lang', lang);
            localStorage.setItem('bantu_gitea_lang', giteaLang);
            localStorage.setItem('bantu_sync_ts', ts.toString());
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
            giteaThemeBtn.innerHTML = (theme === 'dark') ?
                '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg> <span>Clair</span>' :
                '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0070f3" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg> <span>Sombre</span>';
        }
    }

    function updateCrossLinks(theme, lang) {
        const giteaLang = GITEA_LANG_MAP[lang] || 'fr-FR';
        const giteaTheme = (theme === 'light') ? 'github' : 'github-dark';

        document.querySelectorAll('a').forEach(a => {
            const h = a.href || '';
            if (h.includes(':3002') || h.includes(':3001') || h.includes(':8001')) {
                try {
                    const u = new URL(h, window.location.origin);
                    u.searchParams.set('lang', (h.includes(':3002') ? giteaLang : lang));
                    u.searchParams.set('theme', (h.includes(':3002') ? giteaTheme : theme));
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
    });
})();
