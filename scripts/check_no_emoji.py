#!/usr/bin/env python
"""T-084 : echoue si un emoji est present dans les templates, le CSS/JS statique ou la documentation.

Usage : python scripts/check_no_emoji.py            (code retour 1 si un emoji est trouve)
Les puces typographiques (U+2022, U+00B7) et les fleches simples ne sont pas des emojis.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF"  # pictogrammes, drapeaux, emoticones
    "\u2600-\u27BF"  # symboles divers et dingbats (check, croix, etoile...)
    "\u2B00-\u2BFF"  # fleches et etoiles diverses
    "\u231A\u231B\u23E9-\u23FF"
    "\uFE0F\u200D]"
)
TARGETS = ["templates", "static", "docs", "README.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"]
SUFFIXES = {".html", ".css", ".js", ".md", ".svg"}


def iter_files():
    for target in TARGETS:
        path = ROOT / target
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from (p for p in path.rglob("*") if p.is_file() and p.suffix in SUFFIXES)


def find_emojis(paths):
    found = []
    for path in paths:
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if EMOJI.search(line):
                found.append((path.relative_to(ROOT), number, line.strip()[:100]))
    return found


def main() -> int:
    found = find_emojis(iter_files())
    for path, number, line in found:
        print(f"{path}:{number}: emoji interdit -> {line}")
    if found:
        print(f"\n{len(found)} emoji(s) detecte(s). Utilisez {{% icon %}} / {{% flag %}} (apps/core/templatetags/icons.py).")
        return 1
    print("OK : aucun emoji.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
