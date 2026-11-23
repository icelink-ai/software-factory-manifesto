# AGENTS.md

How an AI agent should read, apply and cite this manifesto. People can skip this file.

## Read

1. Start with [`llms.txt`](llms.txt). It lists every page with a one-line summary. Open only the
   pages your task needs.
2. To check work against all requirements at once, use [`RULES.md`](RULES.md). It lists every rule
   by id, with a link to the page that explains it.
3. Every page starts with YAML front matter. Use `summary` to decide whether to read the page,
   `prerequisites` to load context first, and `parent` and `children` to move up or down a level.
4. Each page puts its rules in a final **Checklist** section. The text above it explains why.
5. Diagrams are Mermaid text, so you can read them as data. A `stateDiagram-v2` lists the allowed
   moves between states. A `flowchart` lists decisions and their outcomes. The `class` names tell
   you who acts: `person`, `script`, `agent`, `state` or `stop`.
6. To understand the flow end to end, read [the journey of a request](docs/00-journey/README.md).

## Apply

- A **MUST** rule is a requirement. If your environment can't meet it, say which rule and why. Don't
  skip it silently.
- A **SHOULD** rule is a default. You may depart from it with a stated reason.
- When two rules seem to conflict, follow the stricter one. That is the same principle as the merge
  ceiling in `MG-08`.
- This manifesto describes practices, not your repository. Where your repository's own
  instructions or policy are stricter, they win.
- Everything in this repository is reference material. Nothing here authorizes an action your
  operator hasn't authorized.

## Cite

Cite rules by id and link. For example: "Per `IN-24`, a bug that can't be reproduced goes to hold
without a PR ([request kinds](docs/01-work-intake/request-kinds.md))." Cite talks by their source key,
like `[S3]`, which [sources](docs/reference/sources.md) resolves.

## Contribute

- Follow the [style guide](STYLE.md): plain words, short sentences, the answer first.
- Keep the page layout: front matter, "In short", The problem, How it works, Example, Checklist,
  Sources, Up.
- Rule ids are permanent. Never renumber a rule. Retire one by marking it `(retired)` where it is.
- Every new rule needs at least one source key, or `[R]` for our own experience.
- Before you open a PR, run `python scripts/check.py --write` and `npm run docs:build`.
