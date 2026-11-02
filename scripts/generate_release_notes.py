#!/usr/bin/env python3
"""
Sovereign Release Notes Generator (GitHub Standard Format)
Classifies merged pull requests and commits into semantic categories:
- Exciting New Features
- Bug Fixes
- Documentation Updates
- Security & Hardening
- Maintenance & Performance
"""

import argparse
import json
import re
import sys
from typing import Any, Dict, List


CATEGORIES = [
    {
        "title": "Exciting New Features",
        "patterns": [r"^feat(\(.*\))?:", r"feature"],
        "key": "features",
    },
    {
        "title": "Bug Fixes",
        "patterns": [r"^fix(\(.*\))?:", r"bugfix", r"patch"],
        "key": "fixes",
    },
    {
        "title": "Security & Hardening",
        "patterns": [r"^sec(\(.*\))?:", r"^security(\(.*\))?:", r"vulnerability"],
        "key": "security",
    },
    {
        "title": "Documentation Updates",
        "patterns": [r"^docs(\(.*\))?:", r"doc"],
        "key": "docs",
    },
    {
        "title": "Maintenance & Testing",
        "patterns": [r"^test(\(.*\))?:", r"^refactor(\(.*\))?:", r"^chore(\(.*\))?:", r"^ci(\(.*\))?:"],
        "key": "maintenance",
    },
]


def classify_entry(title: str) -> str:
    lower_title = title.lower()
    for cat in CATEGORIES:
        for pat in cat["patterns"]:
            if re.search(pat, lower_title):
                return cat["key"]
    return "other"


def generate_release_notes(
    entries: List[Dict[str, Any]],
    previous_tag: str = "v1.0.0",
    current_tag: str = "v1.1.0",
    repo_url: str = "https://forge.bantudevlab.local/bantudev/bantudevlab",
) -> str:
    classified: Dict[str, List[Dict[str, Any]]] = {cat["key"]: [] for cat in CATEGORIES}
    classified["other"] = []
    contributors = set()

    for entry in entries:
        title = entry.get("title", "").strip()
        author = entry.get("author", "contributor").lstrip("@")
        pr_number = entry.get("number")
        cat_key = classify_entry(title)
        classified[cat_key].append({
            "title": title,
            "author": author,
            "number": pr_number,
        })
        if author:
            contributors.add(author)

    lines = ["## What's Changed", ""]

    for cat in CATEGORIES:
        items = classified.get(cat["key"], [])
        if items:
            lines.append(f"### {cat['title']}")
            for item in items:
                pr_ref = f" in #{item['number']}" if item["number"] else ""
                lines.append(f"* {item['title']} by @{item['author']}{pr_ref}")
            lines.append("")

    other_items = classified.get("other", [])
    if other_items:
        lines.append("### Other Changes")
        for item in other_items:
            pr_ref = f" in #{item['number']}" if item["number"] else ""
            lines.append(f"* {item['title']} by @{item['author']}{pr_ref}")
        lines.append("")

    if contributors:
        lines.append("## Contributors")
        for contributor in sorted(contributors):
            lines.append(f"* @{contributor}")
        lines.append("")

    if previous_tag and current_tag and repo_url:
        lines.append(f"**Full Changelog**: {repo_url}/compare/{previous_tag}...{current_tag}")
        lines.append("")

    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser(description="Generate modern GitHub style release notes")
    parser.add_argument("--input", help="Path to JSON file containing PR or commit list", default=None)
    parser.add_argument("--prev", help="Previous tag", default="v1.0.0")
    parser.add_argument("--current", help="Current tag", default="v1.1.0")
    parser.add_argument("--repo-url", help="Repository URL", default="https://forge.bantudevlab.local/bantudev/bantudevlab")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            entries = json.load(f)
    else:
        # Default sample entries for standalone invocation
        entries = [
            {"title": "feat(copilot): sovereign AI code explanation and completion", "author": "kwame", "number": 101},
            {"title": "fix(auth): secure session token invalidation", "author": "amina", "number": 102},
            {"title": "docs(rulesets): add sovereign branch protection guide", "author": "chidi", "number": 103},
        ]

    notes = generate_release_notes(entries, args.prev, args.current, args.repo_url)
    print(notes)


if __name__ == "__main__":
    main()
