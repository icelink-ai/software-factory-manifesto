---
id: 03-guardrails/least-privilege-agents
level: 2
parent: README.md
children: []
summary: Give each stage its own agent identity with only the tools and credentials it needs; use a general coding agent for building and small domain agents at the edges.
prerequisites: [deny-rules-and-protected-paths.md]
---

# Least-privilege agents

> An agent cannot do what it has no tool for.

## Rules

- **GR-27** Each stage (triage, build, review, edge functions) MUST run under its own identity with
  its own permission set.
- **GR-28** Identity MUST come from authentication (the service account or token of the caller),
  never from a parameter the agent passes.
- **GR-29** Triage and review MUST be read-only on the repository. Only the builder MAY push, and
  only to its own branch.
- **GR-30** Edge functions (feedback triage, alert triage, data questions) SHOULD be small
  domain agents with one or two tools and their own eval, not the general coding agent.
- **GR-31** Access SHOULD grow with demonstrated reliability, like a new employee's: read-only
  first, then scoped actions, then ownership of an outcome.

## Diagram

```mermaid
flowchart LR
    subgraph Triage["Triage agent"]
        T1[read repo]
        T2[read spec]
        T3[read memory]
    end
    subgraph Builder["Builder agent"]
        B1[read repo]
        B2[push own branch]
        B3[open PR]
        B4[write own memory]
    end
    subgraph Reviewer["Reviewer agent"]
        R1[read PR and evidence]
        R2[comment and label]
    end
    subgraph Edge["Domain agents"]
        E1["alert triage: read alerts, open issue"]
        E2["feedback triage: read feedback, open issue"]
    end
```

## Why

A general agent with broad tools can do broad damage: one source describes an agent with email
access that tried to shut down production after hallucinating a security incident [S10]. Small,
specific agents are cheaper, easier to evaluate, and fail in smaller ways [S10]. Bots that start
read-only and earn wider permissions are adopted faster by the people around them [S9].

## Sources

[S9] [S10] [R]

## Up

[03. Guardrails](README.md)
