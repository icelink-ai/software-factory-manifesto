---
id: 03-guardrails/minimal-agent-instructions
level: 2
parent: README.md
children: []
summary: Keep AGENTS.md short and factual, limited to what the code can't show; move every enforceable rule into a check.
prerequisites: [inverted-pyramid.md]
---

# Minimal agent instructions

> **In short:** the instructions file is for facts an agent can't see in the code. It isn't for
> rules a linter could enforce.

## The problem

`AGENTS.md` (or `CLAUDE.md`) is the file an agent reads first in a repository. Teams tend to fill
it with style rules, tutorials and warnings in capital letters.

That backfires. Current models perform worse when the file is long and full of emphasis like
"IMPORTANT!" or "NEVER" [S7]. Worse, rules that live only in prose aren't enforced. They are
suggestions.

## How it works

For every line in the file, ask two questions:

1. **Can the agent learn this by reading the code?** If yes, delete the line. The code already
   says it.
2. **Can a check enforce this?** If yes, write the check and delete the line.

What's left is short and useful. Review it every few months, because tooling improves and some
lines become checks.

| Keep | Remove |
|---|---|
| "The product spec is in `docs/product/`. Read the module before coding." | Code style the formatter already enforces |
| "Never read `.env*` files or credentials." (also a deny rule) | Architecture the folder layout already shows |
| "Run `gates/checks.sh` and leave it green before opening a PR." | Long framework tutorials |
| "Infrastructure changes only by PR. A person applies them." | Emphasis, repetition, motivational text |

## Example

Our own instructions file fits on one screen. It says where the spec lives, what the gate is, a
short "never" list and how to finish a task. Every item on the "never" list is also a deny rule
in the harness. The file explains the rule; the harness enforces it.

> [!TIP]
> Some agent tools can audit the instructions file for stale or conflicting lines. Run the audit
> when you upgrade the model.

## Checklist

- **GR-17** The repository instructions file MUST contain only what an agent can't learn by
  reading the code. Typically: where the spec lives, what is forbidden and why, how to run the
  gate, and how to finish a task.
- **GR-18** It MUST NOT use emphasis (capitals, "IMPORTANT!", repeated "NEVER") as a substitute
  for enforcement.
- **GR-19** Every rule in the file that a check can enforce SHOULD move into the gate and leave
  the file.
- **GR-20** The file MUST be reviewed periodically, and stale or conflicting lines removed.
- **GR-21** A "never" list SHOULD exist and SHOULD match the deny rules the harness enforces.

## Sources

[S2] [S7] [R]

## Up

[03. Guardrails](README.md)
