---
id: 09-adoption/trust-ladder
level: 2
parent: README.md
children: []
summary: Bots climb from read-only answers to scoped actions with evidence to owning an outcome, and the merge ceiling widens one kind at a time.
prerequisites: []
---

# Trust ladder

> Treat an agent like a new colleague: it starts by answering questions, then does small things
> you can check, then owns something.

## Rules

- **AD-09** A new agent or a new repository MUST start at the read-only rung.
- **AD-10** Moving up a rung MUST be a deliberate, recorded decision based on metrics, not a
  default that happens with time.
- **AD-11** Each rung MUST be reversible: a person can move an agent or a kind back down at once.
- **AD-12** Agents SHOULD have a visible identity (name, account) and appear where the team works,
  so people know who did what.

## Diagram

```mermaid
flowchart BT
    R1["Rung 1: read-only<br/>answers questions in chat,<br/>reads code, logs and docs"]
    R2["Rung 2: scoped actions<br/>opens PRs with evidence,<br/>people merge"]
    R3["Rung 3: earned merge<br/>auto-merge for low-risk kinds"]
    R4["Rung 4: owns an outcome<br/>a goal or metric over days,<br/>reports to a person"]
    R1 --> R2 --> R3 --> R4
```

## Sources

[S1] [S9] [S10]

## Up

[09. Adoption](README.md)
