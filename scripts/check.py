#!/usr/bin/env python3
"""Validate the manifesto and regenerate RULES.md and llms.txt.

Checks: front matter fields, parent/children consistency, relative links, rule id format and
uniqueness, forbidden strings. Extracts Mermaid blocks to build/mermaid/ for rendering checks.

Usage: python scripts/check.py [--write]
  --write  regenerate RULES.md and llms.txt (otherwise fail if they are out of date)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REQUIRED = ("id", "level", "parent", "children", "summary", "prerequisites")
RULE_RE = re.compile(r"^- \*\*([A-Z]{2}-\d{2})\*\* (.+?)(?=^- \*\*|^\s*$|\Z)", re.M | re.S)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FORBIDDEN = [
    re.compile(p, re.I)
    for p in (r"icelink-prod", r"\bcf-[a-z]", r"#factory-", r"@[\w.]+\.(com|io)\b",
              r"\bissue #\d+", r"\bPR #\d+", r"samuk", r"C0[A-Z0-9]{8,}")
]
THEME_PREFIX = {
    "00-journey": "--", "01-work-intake": "IN", "02-deterministic-spine": "SP", "03-guardrails": "GR",
    "04-sandboxes": "SB", "05-verification": "VE", "06-merge-policy": "MG",
    "07-memory-and-context": "MC", "08-self-improvement": "SI", "09-adoption": "AD",
}


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.index("\n---\n", 4)
    meta: dict = {}
    for line in text[4:end].splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key.strip()] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            meta[key.strip()] = value
    return meta, text[end + 5 :]


def main() -> int:
    write = "--write" in sys.argv
    errors: list[str] = []
    pages = sorted(DOCS.rglob("*.md"))
    metas: dict[Path, dict] = {}
    rules: list[tuple[str, str, Path]] = []
    mermaid_dir = ROOT / "build" / "mermaid"
    mermaid_dir.mkdir(parents=True, exist_ok=True)
    for old in mermaid_dir.glob("*.mmd"):
        old.unlink()
    n_mermaid = 0

    for page in [ROOT / "README.md", ROOT / "AGENTS.md", *pages]:
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)
        if page.parent != ROOT:
            missing = [k for k in REQUIRED if k not in meta]
            if missing:
                errors.append(f"{rel}: front matter missing {missing}")
            metas[page] = meta
        for target in LINK_RE.findall(body):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = (page.parent / target.split("#")[0]).resolve()
            if not path.exists():
                errors.append(f"{rel}: broken link {target}")
        for m in RULE_RE.finditer(body):
            rules.append((m.group(1), " ".join(m.group(2).split()), page))
        for block in re.findall(r"```mermaid\n(.*?)```", body, re.S):
            n_mermaid += 1
            name = rel.replace("/", "__").removesuffix(".md")
            (mermaid_dir / f"{name}__{n_mermaid:03d}.mmd").write_text(block, encoding="utf-8")
        for pat in FORBIDDEN:
            hit = pat.search(text)
            if hit:
                errors.append(f"{rel}: forbidden internal identifier {hit.group(0)!r}")

    for page, meta in metas.items():
        rel = page.relative_to(ROOT).as_posix()
        for child in meta.get("children", []):
            cpath = (page.parent / child).resolve()
            if not cpath.exists():
                errors.append(f"{rel}: child {child} does not exist")
                continue
            cparent = metas.get(cpath, {}).get("parent", "")
            if cparent and (cpath.parent / cparent).resolve() != page.resolve():
                errors.append(f"{rel}: child {child} has parent {cparent}")
        for pre in meta.get("prerequisites", []):
            if not (page.parent / pre).resolve().exists():
                errors.append(f"{rel}: prerequisite {pre} does not exist")
        theme = page.relative_to(DOCS).parts[0]
        if page.name == "README.md" and theme in THEME_PREFIX:
            listed = {(page.parent / c).resolve() for c in meta.get("children", [])}
            actual = {p.resolve() for p in page.parent.glob("*.md") if p.name != "README.md"}
            if listed != actual:
                errors.append(f"{rel}: children do not match files in folder")

    seen: dict[str, Path] = {}
    for rid, _, page in rules:
        rel = page.relative_to(ROOT).as_posix()
        if rid in seen:
            errors.append(f"{rel}: duplicate rule id {rid} (also in {seen[rid].relative_to(ROOT)})")
        seen[rid] = page
        theme = page.relative_to(DOCS).parts[0]
        if THEME_PREFIX.get(theme) != rid[:2]:
            errors.append(f"{rel}: rule {rid} has the wrong prefix for {theme}")

    rules_md = render_rules(rules)
    llms = render_llms(metas)
    for name, content in (("RULES.md", rules_md), ("llms.txt", llms)):
        target = ROOT / name
        if write:
            target.write_text(content, encoding="utf-8", newline="\n")
        elif not target.exists() or target.read_text(encoding="utf-8") != content:
            errors.append(f"{name} is out of date; run with --write")

    errors += readability([ROOT / "README.md", *pages])
    for e in errors:
        print("ERROR", e)
    print(f"{len(pages) + 2} pages, {len(rules)} rules, {n_mermaid} mermaid diagrams, "
          f"{len(errors)} errors")
    return 1 if errors else 0


def prose_sentences(text: str) -> list[str]:
    """Sentences from prose only: no front matter, code, tables, headings or link targets."""
    _, body = parse_front_matter(text)
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    keep = []
    for line in body.splitlines():
        s = re.sub(r"^(> ?)+", "", line.strip())
        if not s or s.startswith(("|", "#", "<", "[!")):
            keep.append("")
            continue
        s = re.sub(r"^(> ?)+", "", s)
        if re.match(r"^(\d+\.|[-*])\s", s):
            keep.append("")  # each list item is its own unit
        s = re.sub(r"^(\d+\.|[-*]|- \[ \])\s+", "", s)
        # A bold label ("**Start the run.**") ends a sentence of its own.
        s = re.sub(r"^\*\*([^*]+?)\*\*", r"\1", s)
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"`[^`]*`", "x", s)
        keep.append(s)
    paragraphs = " ".join(line if line else "\n" for line in keep).split("\n")
    out = []
    for para in paragraphs:
        for sent in re.split(r"(?<=[.!?:])\s+(?=[A-Z\"(])", para.strip()):
            if len(sent.split()) >= 3:
                out.append(sent)
    return out


MAX_AVG, MAX_LEN = 20, 35


def readability(pages: list[Path]) -> list[str]:
    """Report pages whose average sentence is too long, and sentences over the limit."""
    errors, total, count = [], 0, 0
    for page in pages:
        sents = prose_sentences(page.read_text(encoding="utf-8"))
        if not sents:
            continue
        lengths = [len(s.split()) for s in sents]
        total += sum(lengths)
        count += len(lengths)
        avg = sum(lengths) / len(lengths)
        rel = page.relative_to(ROOT).as_posix()
        if avg > MAX_AVG:
            errors.append(f"{rel}: average sentence {avg:.1f} words (max {MAX_AVG})")
        for s, n in zip(sents, lengths):
            if n > MAX_LEN:
                errors.append(f"{rel}: sentence of {n} words: {s[:70]}...")
    if count:
        print(f"readability: {count} sentences, average {total / count:.1f} words")
    return errors


def rebase_link(m: re.Match, page: Path) -> str:
    """Rewrite a link found in a page so it works from the repository root."""
    target = m.group(1)
    if target.startswith(("http://", "https://", "#", "mailto:")):
        return m.group(0)
    path, _, anchor = target.partition("#")
    rel = (page.parent / path).resolve().relative_to(ROOT).as_posix()
    return m.group(0).replace(f"({target})", f"({rel}{'#' + anchor if anchor else ''})")


def render_rules(rules: list[tuple[str, str, Path]]) -> str:
    out = [
        "# Rules",
        "",
        "Every rule in the manifesto, by id. Generated by `scripts/check.py --write`; do not edit.",
        "Each id links to the page that explains it. MUST, SHOULD and MAY follow RFC 2119.",
        "",
    ]
    current = None
    for rid, text, page in sorted(rules, key=lambda r: (r[2].relative_to(DOCS).parts[0], r[0])):
        theme = page.relative_to(DOCS).parts[0]
        if theme != current:
            current = theme
            title = theme.split("-", 1)[1].replace("-", " ").capitalize()
            out += ["", f"## {theme[:2]}. {title}", ""]
        rel = page.relative_to(ROOT).as_posix()
        text = LINK_RE.sub(lambda m: rebase_link(m, page), text)
        out.append(f"- [{rid}]({rel}) {text}")
    return "\n".join(out) + "\n"


def render_llms(metas: dict[Path, dict]) -> str:
    out = [
        "# The Software Factory Manifesto",
        "",
        "> Best practices for a fully automated software factory where AI agents turn requests "
        "into merged, verified changes. Three levels: README (overview), docs/NN-theme/README.md "
        "(theme), docs/NN-theme/*.md (subtopic). All rules by id: RULES.md. How to use: AGENTS.md.",
        "",
        "## Start",
        "",
        "- [README.md](README.md): thesis, nine principles, factory map, reading paths",
        "- [AGENTS.md](AGENTS.md): how agents should read, apply and cite this manifesto",
        "- [RULES.md](RULES.md): every rule by id with links",
    ]
    by_theme: dict[str, list[Path]] = {}
    for page in metas:
        by_theme.setdefault(page.relative_to(DOCS).parts[0], []).append(page)
    for theme in sorted(by_theme):
        pages = sorted(by_theme[theme], key=lambda p: (p.name != "README.md", p.name))
        out += ["", f"## {theme}", ""]
        for page in pages:
            rel = page.relative_to(ROOT).as_posix()
            out.append(f"- [{rel}]({rel}): {metas[page].get('summary', '')}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.exit(main())
