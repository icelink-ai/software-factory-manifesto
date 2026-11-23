---
id: 04-sandboxes/secrets-and-network
level: 2
parent: README.md
children: []
summary: Credentials are injected outside the model's reach and scoped per run; network egress is deny-by-default with an allowlist.
prerequisites: [disposable-environments.md]
---

# Secrets and network

> The safest secret is one the model never sees.

## Rules

- **SB-17** Credentials MUST be injected outside the model's context (network-level injection,
  short-lived tokens in the tool layer), never as files or environment variables the agent can
  print.
- **SB-18** Tokens MUST be short-lived and scoped to one repository and the minimum permissions.
- **SB-19** Cloud access from runs MUST use workload identity federation or equivalent. Long-lived
  key files MUST NOT exist.
- **SB-20** Network egress MUST be deny-by-default, with an allowlist (package registries, the code
  host, the memory server).
- **SB-21** If an agent finds a secret in the repository or in output, it MUST stop and report it,
  not use it.

## Diagram

```mermaid
flowchart LR
    subgraph Run["Run sandbox"]
        M["Model context"]
        T["Tool layer"]
    end
    V[("Secret store")] -->|short-lived token| T
    M -->|"calls tool"| T
    T -->|"authenticated request"| GH["Code host"]
    T -->|allowlisted| REG["Registries"]
    M -. "cannot read" .-x V
    T -. "default deny" .-x NET["Any other host"]
```

## Sources

[S1] [S7] [R]

## Up

[04. Sandboxes](README.md)
