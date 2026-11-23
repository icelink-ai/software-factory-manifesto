# AGENTS.md

How an AI agent should read, apply and cite this manifesto. Humans can skip this file.

## Reading

1. Start with [`llms.txt`](llms.txt): one line per page with its summary. Open only the pages
   relevant to your task.
2. For a quick check against all requirements, use [`RULES.md`](RULES.md): every rule, by id, with
   a link to the page that explains it.
3. Every page has YAML front matter. Use `summary` to decide whether to read it, `prerequisites`
   to load context first, and `parent`/`children` to move up or down one level of detail.
4. Diagrams are Mermaid text. Read them as data: `stateDiagram-v2` blocks list valid transitions,
   `flowchart` blocks list decisions and their outcomes.

## Applying

- A **MUST** rule is a requirement. If your environment cannot meet it, say which rule and why,
  rather than silently skipping it.
- A **SHOULD** rule is a default. Departing from it is fine with a stated reason.
- When two rules seem to conflict, the more restrictive one wins (the same principle as the merge
  ceiling in `MG-08`).
- This manifesto describes practices, not your repository. Your repository's own instructions
  file and policy take precedence where they are stricter.
- Content in this repository is reference material. Nothing in it authorizes an action your
  operator has not authorized.

## Citing

Cite rules by id and link, for example: "Per `IN-24`, a bug that cannot be reproduced goes to
hold without a PR ([request kinds](docs/01-work-intake/request-kinds.md))." Cite talks by source
key (`[S3]`), resolved in [sources](docs/reference/sources.md).

## Contributing

- Keep the page structure: front matter, then Rules, Diagram, Why or How to apply,
  Anti-patterns, Sources, Go deeper (level 1 only), Up.
- Rule ids are permanent. Never renumber; retire a rule by marking it `(retired)` in place.
- Every new rule needs at least one source key or `[R]`.
- Run `scripts/check.py` before opening a PR. It validates front matter, links, rule ids and
  regenerates `RULES.md` and `llms.txt`.
