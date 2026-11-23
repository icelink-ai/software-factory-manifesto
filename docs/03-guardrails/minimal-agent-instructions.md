---
id: 03-guardrails/minimal-agent-instructions
level: 2
parent: README.md
children: []
summary: Keep AGENTS.md and CLAUDE.md short, factual and limited to what the code cannot show; move enforceable rules into checks and audit the file regularly.
prerequisites: [inverted-pyramid.md]
---

# Minimal agent instructions

> The instructions file is for facts an agent cannot see, not for rules a linter could enforce.

## Rules

- **GR-17** The repository instructions file (`AGENTS.md`, `CLAUDE.md` or equivalent) MUST contain
  only information an agent cannot discover by reading the code: where the spec lives, what is
  forbidden and why, how to run the gate, how to finish a task.
- **GR-18** It MUST NOT use emphatic markers ("IMPORTANT!", all caps, repeated "NEVER") as a
  substitute for enforcement. Current models perform worse with them.
- **GR-19** Every rule in the file that can be enforced by a check SHOULD be moved into the gate,
  and removed from the file.
- **GR-20** The file MUST be reviewed periodically, and stale or conflicting instructions removed.
- **GR-21** A "Never" list SHOULD exist and SHOULD match the deny rules enforced by the harness, so
  the prose explains what the harness enforces.

## What belongs, what does not

| Belongs | Does not belong |
|---|---|
| "Product spec lives in `docs/product/`; read the module before coding" | Code style the formatter already enforces |
| "Never read `.env*` or credentials" (also enforced as a deny rule) | Architecture the directory layout already shows |
| "Run `gates/checks.sh` and leave it green before opening a PR" | Long tutorials on the framework |
| "Infrastructure changes only by PR; a person applies them" | Motivational text, emphasis, repetition |

## Sources

[S2] [S7] [R]

## Up

[03. Guardrails](README.md)
