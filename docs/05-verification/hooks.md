---
id: 05-verification/hooks
level: 2
parent: README.md
children: []
summary: Harness hooks run fast checks inside the agent loop, so problems are fixed while the context is fresh; a hook must signal failure in the way the harness treats as "go back".
prerequisites: [single-gate.md]
---

# Hooks

> Hooks guarantee what a prompt can only ask for.

## Rules

- **VE-19** The agent harness SHOULD run the fast gate (lint, format) after each edit.
- **VE-20** It SHOULD run the tests for the affected area when the agent marks a task done, and
  the full gate when the session ends.
- **VE-21** A hook that finds a problem MUST exit with the code the harness interprets as "send the
  agent back" (in some harnesses that is exit code 2; other non-zero codes may be treated as
  informational). Check your harness documentation; a wrong exit code silently disables the hook.
- **VE-22** Hooks MUST call the same gate script, in fast or full mode, not a separate set of
  commands.

## Diagram

```mermaid
sequenceDiagram
    participant A as Agent
    participant H as Harness
    participant G as Gate script
    A->>H: edit file
    H->>G: fast mode
    G-->>H: lint error
    H-->>A: blocking feedback
    A->>H: fix
    H->>G: fast mode
    G-->>H: ok
    A->>H: task done
    H->>G: area tests
    G-->>H: ok
    A->>H: end session
    H->>G: full gate
    G-->>H: ok
```

## Sources

[S3] [S7]

## Up

[05. Verification](README.md)
