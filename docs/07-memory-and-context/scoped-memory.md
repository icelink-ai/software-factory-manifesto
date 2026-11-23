---
id: 07-memory-and-context/scoped-memory
level: 2
parent: README.md
children: []
summary: A memory service partitions everything by scope, derives identity from authentication, filters every query by scope, and allows writes to shared scopes only by promotion.
prerequisites: []
---

# Scoped memory

> Memory without isolation is a shared whiteboard that any agent can be tricked into reading or
> writing.

## Rules

- **MC-07** The memory service MUST derive the caller's identity from authentication (service
  account, token), never from a tool parameter.
- **MC-08** Every read MUST pass through one scope filter function; tests MUST try to read another
  scope and fail.
- **MC-09** Scopes SHOULD be: `agent` (free writes), `project` (agents of one repository),
  `domain` (a group of projects), `global` (read-only for agents).
- **MC-10** Writes to shared scopes MUST go through a proposal that a person or a policy promotes.
- **MC-11** Entries MUST carry provenance (run id), confidence and validity, and MUST be
  invalidatable when proved wrong.
- **MC-12** The service SHOULD be stateless and expose its tools through a standard protocol
  (for example MCP) so any agent harness can use it.

## Diagram

```mermaid
flowchart TB
    subgraph Callers
        A1["Builder<br/>identity from token"]
        A2["Reviewer<br/>identity from token"]
    end
    A1 & A2 --> AUTH["Authenticate<br/>derive agent, domain, projects"]
    AUTH --> F["Scope filter<br/>mandatory on every query"]
    F --> S1[("agent scope<br/>read + write")]
    F --> S2[("project scope<br/>read + write")]
    F --> S3[("domain scope<br/>read")]
    F --> S4[("global scope<br/>read only")]
    A1 -->|propose| PR["Promotion queue"]
    PR -->|approved| S3
    PR -->|approved| S4
```

## Sources

[S5] [R]

## Up

[07. Memory and context](README.md)
