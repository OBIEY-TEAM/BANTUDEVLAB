import pathlib

root = pathlib.Path(r"c:/Users/User/Desktop/AGENT/BANTUDEVLAB")
css_path = root / "static/css/style.css"
css_text = css_path.read_bytes().decode("utf-8").replace("\r\n", "\n")

extra_css = """
/* ==========================================================================
   PHASE 1: DESIGN SYSTEM - TOKENS CLAIR / SOMBRE (DES-01, DES-02)
   ========================================================================== */

/* Thème Clair - Surcharges des variables système */
[data-theme="light"] {
  --dark-bg: #f8fafc;
  --dark-surface: #ffffff;
  --dark-border: #e2e8f0;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --nav-bg: rgba(255, 255, 255, 0.96);
  --card-bg: #ffffff;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
}

[data-theme="light"] .navbar {
  background: var(--nav-bg);
  box-shadow: var(--shadow-sm);
}

[data-theme="light"] .brand {
  color: var(--text-main);
}

[data-theme="light"] .card,
[data-theme="light"] .zkp-wizard-card,
[data-theme="light"] .africa-map-wrapper,
[data-theme="light"] .node-card {
  background: var(--card-bg);
  border-color: var(--dark-border);
  box-shadow: var(--shadow-md);
}

[data-theme="light"] .card h3,
[data-theme="light"] .card h4,
[data-theme="light"] .zkp-wizard-card h2,
[data-theme="light"] .africa-map-wrapper h3 {
  color: var(--text-main);
}

[data-theme="light"] input[type="text"],
[data-theme="light"] select,
[data-theme="light"] textarea,
[data-theme="light"] .input-field {
  background: #f1f5f9 !important;
  color: #0f172a !important;
  border-color: #cbd5e1 !important;
}

[data-theme="light"] .btn-secondary {
  background: #e2e8f0;
  color: #1e293b;
  border-color: #cbd5e1;
}

[data-theme="light"] .btn-secondary:hover {
  background: #cbd5e1;
}

[data-theme="light"] footer {
  border-top-color: var(--dark-border);
  color: var(--text-muted);
}

[data-theme="light"] .CodeMirror {
  border-color: var(--dark-border);
}

/* ==========================================================================
   PHASE 2: NAVIGATION RESPONSIVE & TOOLBAR (NAV-01 à NAV-05)
   ========================================================================== */

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Theme Switch Button */
.theme-switch-btn,
.lang-toggle-btn {
  background: transparent;
  border: 1px solid var(--dark-border);
  color: var(--text-main);
  padding: 0.45rem 0.65rem;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.theme-switch-btn:hover,
.lang-toggle-btn:hover {
  border-color: var(--primary-african-gold);
  color: var(--primary-african-gold);
  background: rgba(245, 158, 11, 0.08);
}

/* User Profile Badge */
.user-session-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  font-size: 0.85rem;
  color: var(--secondary-emerald);
  font-weight: 600;
}

/* Mobile Hamburger Toggle */
.navbar-toggle {
  display: none;
  background: transparent;
  border: 1px solid var(--dark-border);
  color: var(--text-main);
  padding: 0.45rem 0.65rem;
  border-radius: 8px;
  cursor: pointer;
}

/* Mobile Drawer Overlay & Panel */
.nav-drawer-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.nav-drawer {
  position: fixed;
  top: 0;
  right: -320px;
  width: 300px;
  height: 100%;
  background: var(--dark-surface);
  border-left: 1px solid var(--dark-border);
  z-index: 1001;
  padding: 1.5rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: -5px 0 25px rgba(0, 0, 0, 0.4);
}

.nav-drawer.open {
  right: 0;
}

.nav-drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--dark-border);
  padding-bottom: 1rem;
}

.nav-drawer-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.nav-drawer-links a {
  color: var(--text-main);
  text-decoration: none;
  font-size: 1.05rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
}

.nav-drawer-links a:hover,
.nav-drawer-links a.active {
  color: var(--primary-african-gold);
}

/* Breadcrumbs (NAV-04) */
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.breadcrumbs a {
  color: var(--text-muted);
  text-decoration: none;
}

.breadcrumbs a:hover {
  color: var(--primary-african-gold);
}

.breadcrumbs-separator {
  color: var(--dark-border);
}

.breadcrumbs-current {
  color: var(--primary-african-gold);
  font-weight: 600;
}

/* ==========================================================================
   PHASE 3 & 4: COMPOSANTS D'INTERFACE & MICRO-INTERACTIONS
   ========================================================================== */

/* Language Selector Dropdown */
.lang-dropdown {
  position: relative;
  display: inline-block;
}

.lang-menu {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: var(--dark-surface);
  border: 1px solid var(--dark-border);
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  z-index: 100;
  min-width: 150px;
  overflow: hidden;
}

.lang-menu.show {
  display: block;
}

.lang-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.6rem 1rem;
  border: none;
  background: transparent;
  color: var(--text-main);
  text-align: left;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.15s;
}

.lang-item:hover {
  background: rgba(245, 158, 11, 0.12);
  color: var(--primary-african-gold);
}

/* Stepper & Copy Action Feedback (UI-01) */
.copy-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  padding: 0.35rem 0.65rem;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--dark-border);
  border-radius: 6px;
  color: var(--text-main);
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:hover {
  border-color: var(--secondary-emerald);
  color: var(--secondary-emerald);
}

.copy-btn.copied {
  background: rgba(16, 185, 129, 0.2) !important;
  color: var(--secondary-emerald) !important;
  border-color: var(--secondary-emerald) !important;
}

/* Editor Language Header Bar (UI-02) */
.editor-lang-select {
  background: #080c14;
  color: #fff;
  border: 1px solid var(--dark-border);
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
}

[data-theme="light"] .editor-lang-select {
  background: #ffffff;
  color: #0f172a;
}

/* Responsive Breakpoints */
@media (max-width: 900px) {
  .nav-links {
    display: none;
  }
  .navbar-toggle {
    display: block;
  }
}
"""

if "PHASE 1: DESIGN SYSTEM - TOKENS CLAIR / SOMBRE" not in css_text:
    css_text += "\n" + extra_css
    css_path.write_bytes(css_text.replace("\n", "\r\n").encode("utf-8"))
    print("style.css enhanced successfully")
else:
    print("style.css already has design system tokens")
