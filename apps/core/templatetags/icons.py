"""Icones SVG auto-hebergees (T-080/T-081/T-083) : aucun CDN, compatibles avec une CSP stricte.

Usage dans un template (tags disponibles sans `{% load %}`, voir TEMPLATES["OPTIONS"]["builtins"]) :
    {% icon "shield-check" %}
    {% icon "star" size=16 cls="text-gold" title="Favoris" %}
    {% flag "CIV" %}

Les icones sont dessinees en traits 24x24 (style outline, `currentColor`), donc themables par CSS.
Elles sont decoratives (`aria-hidden`) sauf si `title` est fourni.
"""

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

ICONS = {
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>',
    "shield-check": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "landmark": '<path d="M3 21h18M5 21V10M9 21V10M15 21V10M19 21V10M2 10l10-6 10 6z"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3M14 9l2 2"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
    "bot": '<rect x="4" y="8" width="16" height="11" rx="3"/><path d="M12 8V4M9 13v1.5M15 13v1.5"/><circle cx="12" cy="3.5" r="1"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "package": '<path d="M12 2l9 5v10l-9 5-9-5V7z"/><path d="M3 7l9 5 9-5M12 12v10"/>',
    "star": '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.3l-5.5 3 1-6.2L3 9.7l6.2-.9z"/>',
    "git-fork": '<circle cx="6" cy="5" r="2"/><circle cx="18" cy="5" r="2"/><circle cx="12" cy="19" r="2"/><path d="M6 7v2a3 3 0 003 3h6a3 3 0 003-3V7M12 12v5"/>',
    "git-branch": '<circle cx="6" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="8" r="2"/><path d="M6 7v10M18 10a6 6 0 01-6 6H8"/>',
    "zap": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "map-pin": '<path d="M12 21s7-6 7-12a7 7 0 00-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "scan": '<path d="M4 8V5a1 1 0 011-1h3M16 4h3a1 1 0 011 1v3M20 16v3a1 1 0 01-1 1h-3M8 20H5a1 1 0 01-1-1v-3"/><path d="M8 12h8"/>',
    "message-square": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "circle-check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.5"/>',
    "circle-x": '<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6M15 9l-6 6"/>',
    "triangle-alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.01"/>',
    "bell": '<path d="M6 16v-5a6 6 0 0112 0v5l2 2H4zM10 21h4"/>',
    "refresh-cw": '<path d="M20 12a8 8 0 01-14 5M4 12a8 8 0 0114-5"/><path d="M18 3v4h-4M6 21v-4h4"/>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    "save": '<path d="M5 3h11l3 3v15H5z"/><path d="M8 3v5h7V3M8 21v-7h8v7"/>',
    "sparkles": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17v4M17 19h4"/>',
    "log-in": '<path d="M15 4h4v16h-4M10 8l4 4-4 4M14 12H3"/>',
    "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    "lightbulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-4 10.5c1 1 1 2 1 3h6c0-1 0-2 1-3A6 6 0 0012 3z"/>',
    "dot": '<circle cx="12" cy="12" r="5" fill="currentColor" stroke="none"/>',
    "server": '<rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5v.01M7 16.5v.01"/>',
    "activity": '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    "sun": '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>',
    "moon": '<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>',
    "menu": '<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "external-link": '<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
    "copy": '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "user": '<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "chevron-down": '<polyline points="6 9 12 15 18 9"/>',
}

# Drapeaux simplifies (SVG 3:2), rendus en ligne : les emojis de drapeaux ne s'affichent pas sous Windows.
FLAGS = {
    "CIV": '<rect width="9" height="20" fill="#F77F00"/><rect x="9" width="9" height="20" fill="#fff"/><rect x="18" width="9" height="20" fill="#009E60"/>',
    "SEN": '<rect width="9" height="20" fill="#00853F"/><rect x="9" width="9" height="20" fill="#FDEF42"/><rect x="18" width="9" height="20" fill="#E31B23"/><path d="M13.5 7l1 3h3l-2.5 1.8 1 3-2.5-1.9-2.5 1.9 1-3L9.5 10h3z" fill="#00853F"/>',
    "NGA": '<rect width="9" height="20" fill="#008751"/><rect x="9" width="9" height="20" fill="#fff"/><rect x="18" width="9" height="20" fill="#008751"/>',
    "KEN": '<rect width="27" height="20" fill="#000"/><rect y="5" width="27" height="10" fill="#BB0000"/><path d="M0 5h27M0 15h27" stroke="#fff" stroke-width="1.5"/><rect y="6.5" width="27" height="7" fill="#BB0000"/><ellipse cx="13.5" cy="10" rx="2.6" ry="5" fill="#fff"/><ellipse cx="13.5" cy="10" rx="1.4" ry="3.6" fill="#BB0000"/><rect y="13.5" width="27" height="6.5" fill="#006600"/>',
    "RWA": '<rect width="27" height="10" fill="#00A1DE"/><rect y="10" width="27" height="5" fill="#FAD201"/><rect y="15" width="27" height="5" fill="#20603D"/><circle cx="21" cy="5" r="2.2" fill="#FAD201"/>',
}


@register.simple_tag
def icon(name, size=20, cls="", title=""):
    """Rend une icone SVG en ligne (`currentColor`). Inconnue : chaine vide (jamais d'emoji de repli)."""
    body = ICONS.get(name)
    if body is None:
        return ""
    label = f'role="img" aria-label="{escape(title)}"' if title else 'aria-hidden="true" focusable="false"'
    css = f"icon icon-{escape(name)} {escape(cls)}".strip()
    return mark_safe(
        f'<svg class="{css}" width="{int(size)}" height="{int(size)}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" {label}>{body}</svg>'
    )


@register.simple_tag
def flag(code, width=24, title=""):
    """Rend le drapeau SVG d'un pays (code ISO-3). Inconnu : chaine vide."""
    body = FLAGS.get(str(code).upper())
    if body is None:
        return ""
    width = int(width)
    height = round(width * 20 / 27)
    label = f'role="img" aria-label="{escape(title)}"' if title else 'aria-hidden="true" focusable="false"'
    return mark_safe(
        f'<svg class="flag flag-{escape(str(code).lower())}" width="{width}" height="{height}" viewBox="0 0 27 20" '
        f'{label}><g>{body}</g></svg>'
    )
