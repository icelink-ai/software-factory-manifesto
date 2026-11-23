---
id: 03-guardrails/deny-rules-and-protected-paths
level: 2
parent: README.md
children: []
summary: Block irreversible actions in the harness with versioned deny rules, and require a human merge for any change to paths that define the factory, CI, infrastructure or auth.
prerequisites: []
---

# Deny rules and protected paths

> Ask one question of every action: if the agent gets this wrong once, can it be undone?

Wrong code can be reverted. A leaked secret, a deleted branch, a production deploy or a rewritten
history cannot [S7].

## Rules

- **GR-22** Irreversible actions MUST be denied by the harness before any classifier or model
  judgment runs. Minimum list: reading secret files (`.env*`, keys, state files), force push,
  rewriting the main branch, deleting branches or data, deploying or applying infrastructure,
  merging one's own PR.
- **GR-23** Deny rules MUST be versioned in the repository and reviewed like code.
- **GR-24** The merge policy MUST define protected paths, and any PR touching them MUST need a
  human merge regardless of risk or kind.
- **GR-25** Protected paths MUST include at least: CI and workflow definitions, the factory's own
  definition (prompts, gate, policy), agent instruction files, infrastructure, auth and permission
  code.
- **GR-26** The factory's credentials SHOULD NOT allow changing CI definitions at all. When a job
  needs such a change, the builder MUST leave the patch for a person to apply.

## Diagram

```mermaid
flowchart TD
    A[Agent action] --> D{"Deny rule match?"}
    D -->|yes| BLK["Blocked by harness<br/>no model judgment involved"]
    D -->|no| C["Runs inside sandbox"]
    C --> PR[PR opened]
    PR --> P{"Touches protected path?"}
    P -->|yes| H["Human merge only"]
    P -->|no| POL["Normal merge policy<br/>risk x kind"]
```

## Why the factory cannot edit its own rules

If an agent can merge a change to the gate, the prompts or the merge policy, every other guardrail
is advisory. Self-improvement still happens (see [Factory-as-code](../08-self-improvement/factory-as-code.md)),
but through PRs that a person merges.

## Sources

[S7] [S9] [R]

## Up

[03. Guardrails](README.md)
