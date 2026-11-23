---
id: 04-sandboxes/disposable-environments
level: 2
parent: README.md
children: []
summary: Build run environments from a versioned image refreshed on a schedule from the latest main; a broken image is a job for an agent, not a person.
prerequisites: []
---

# Disposable environments

> The run environment is a build artifact, versioned and rebuilt, never hand-tuned.

## Rules

- **SB-07** Run environments MUST be created from a versioned image plus a setup script kept in
  the repository.
- **SB-08** The image or snapshot SHOULD be rebuilt on a schedule from the latest main branch, so
  runs start with warm dependencies and current code.
- **SB-09** When the image build breaks, the factory SHOULD open a job to fix it, so an agent is
  the first responder.
- **SB-10** Every run MUST have a wall-clock limit and MUST be destroyed at the end, including
  on failure.
- **SB-11** Nothing a run produces MAY persist except what it explicitly publishes (branch, PR,
  artifacts, memory entries).

## Diagram

```mermaid
sequenceDiagram
    participant M as Main branch
    participant B as Image builder
    participant I as Image registry
    participant R as Run
    loop every hour
        M->>B: latest commit
        B->>I: image + warm dependencies
        alt build fails
            B->>B: open fix job for an agent
        end
    end
    R->>I: start from latest image
    R->>R: build, test, push branch
    R-->>R: destroyed at the end
```

## Sources

[S1] [S7] [R]

## Up

[04. Sandboxes](README.md)
