#!/usr/bin/env python3
"""Prepare the VitePress source from the repository's Markdown.

The repository stays readable on GitHub (README.md per folder, links to README.md). The site
needs index.md per folder. This script copies the pages into website/content/, renames
README.md to index.md, rewrites links accordingly, and writes the sidebar from front matter.

Usage: python scripts/build_site.py
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "website" / "content"
HOME = ROOT / "website" / "home.md"
LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")
GITHUB = "https://github.com/icelink-ai/software-factory-manifesto/blob/main/"


def front_matter(text: str) -> dict:
    meta: dict = {}
    if text.startswith("---\n"):
        for line in text[4 : text.index("\n---\n", 4)].splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta


def title_of(text: str) -> str:
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def site_path(rel: str) -> str:
    """Repository path -> site path (README.md becomes index.md; root README is the manifesto)."""
    if rel == "README.md":
        return "manifesto.md"
    if rel.endswith("README.md"):
        return rel[: -len("README.md")] + "index.md"
    return rel


def rewrite_links(text: str, src_rel: str) -> str:
    src_dir = (ROOT / src_rel).parent

    def fix(m: re.Match) -> str:
        target = m.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        path, _, anchor = target.partition("#")
        resolved = (src_dir / path).resolve()
        try:
            rel = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        if not rel.endswith(".md"):
            # Files the site does not serve (LICENSE, scripts) link to GitHub.
            return f"{m.group(1)}{GITHUB}{rel}{m.group(3)}"
        new = Path(site_path(rel))
        here = Path(site_path(src_rel)).parent
        relpath = Path(*([".."] * len(here.parts)), new) if here.parts else new
        link = relpath.as_posix() + (f"#{anchor}" if anchor else "")
        return f"{m.group(1)}{link}{m.group(3)}"

    return LINK_RE.sub(fix, text)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    pages = ["README.md", "AGENTS.md", "STYLE.md", "RULES.md"]
    pages += sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "docs").rglob("*.md"))

    for rel in pages:
        text = (ROOT / rel).read_text(encoding="utf-8")
        dest = OUT / site_path(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rewrite_links(text, rel), encoding="utf-8", newline="\n")
    shutil.copy(HOME, OUT / "index.md")

    sidebar = [
        {"text": "Start here", "items": [
            {"text": "The manifesto", "link": "/manifesto"},
            {"text": "For AI agents", "link": "/AGENTS"},
            {"text": "All rules", "link": "/RULES"},
        ]},
    ]
    for section in sorted((ROOT / "docs").iterdir()):
        if not section.is_dir():
            continue
        readme = section / "README.md"
        index_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
        meta = front_matter(index_text)
        children = [c.strip() for c in meta.get("children", "[]").strip("[]").split(",") if c.strip()]
        if not children:
            children = sorted(p.name for p in section.glob("*.md") if p.name != "README.md")
        items = []
        if readme.exists():
            items.append({"text": "Overview", "link": f"/docs/{section.name}/"})
        for child in children:
            text = (section / child).read_text(encoding="utf-8")
            items.append({"text": title_of(text), "link": f"/docs/{section.name}/{child[:-3]}"})
        heading = title_of(index_text) or section.name.replace("-", " ").capitalize()
        sidebar.append({"text": heading, "collapsed": section.name != "00-journey", "items": items})
    (ROOT / "website" / ".vitepress" / "sidebar.json").write_text(
        json.dumps(sidebar, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(pages)} pages copied to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
