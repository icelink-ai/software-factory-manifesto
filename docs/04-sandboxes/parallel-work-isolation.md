---
id: 04-sandboxes/parallel-work-isolation
level: 2
parent: README.md
children: []
summary: When several agents share a repository, each works on its own branch in its own worktree or environment and never switches the shared checkout.
prerequisites: []
---

# Parallel work isolation

> Two agents in one working tree is one corrupted working tree.

## Rules

- **SB-22** Each job MUST work on its own branch, named after the job (for example
  `factory/issue-<n>`).
- **SB-23** In the cloud, each job MUST get its own environment, which makes this automatic.
- **SB-24** When agents run locally in a shared clone, each MUST use its own git worktree created
  from an up-to-date main, and MUST NOT switch branches in the shared checkout.
- **SB-25** A worktree MUST be removed after its branch is pushed.
- **SB-26** A concurrency limit MUST cap how many jobs run at once.

## Diagram

```mermaid
flowchart TB
    MAIN[("Shared clone<br/>stays on main")]
    MAIN --> W1["worktree: factory/issue-101<br/>agent A"]
    MAIN --> W2["worktree: factory/issue-102<br/>agent B"]
    MAIN --> W3["worktree: docs/update<br/>person or local agent"]
    W1 -->|push| R[(Remote)]
    W2 -->|push| R
    W3 -->|push| R
```

## Sources

[S3] [S6] [S7] [R]

## Up

[04. Sandboxes](README.md)
