---
id: 06-merge-policy
level: 1
parent: ../../README.md
children: [risk-times-kind.md, human-review-and-hold.md, incidents.md]
summary: A deterministic script decides merges; auto-merge only when risk, kind and paths all allow it, people review in proportion to risk, and nothing but the policy script can merge a factory PR.
prerequisites: [../05-verification/README.md]
---

# 06. Merge policy

> Autonomy is a ceiling set by policy, not a feeling. The strictest dimension wins.

## Rules

- **MG-01** A deterministic script MUST make every merge decision from the PR's labels, paths, CI
  status and review verdict. No agent decides to merge.
- **MG-02** Auto-merge MUST require all of: factory-made PR, risk in the auto-merge list, kind that
  allows it, reviewer approval, no protected path, no `hold`, CI green on the latest commit.
- **MG-03** Human approvals MUST scale with risk (for example low 0, medium 1, high 2), and the
  kind's minimum MUST apply when it is higher.
- **MG-04** A PR without a risk label MUST be treated as high risk.
- **MG-05** The factory MUST NOT merge its own PR by any path other than the policy script.
- **MG-06** The reason a PR was not auto-merged MUST be visible on the PR or in the job.
- **MG-07** The merge notice MUST be posted to the origin thread.

## Diagram

```mermaid
flowchart TD
    A[CI finished green] --> B{"Factory-made PR?"}
    B -->|no| H[Human process]
    B -->|yes| C{"Reviewer approved,<br/>no changes label?"}
    C -->|no| H
    C -->|yes| D{"Protected path touched?"}
    D -->|yes| H
    D -->|no| E{"hold label?"}
    E -->|yes| H
    E -->|no| F{"Risk in auto list<br/>AND kind allows?"}
    F -->|no| H
    F -->|yes| G{"PR unchanged since CI?"}
    G -->|no| A
    G -->|yes| M[Auto-merge squash]
    H --> HA["awaiting_human<br/>approvals = max of risk, kind"]
    M --> N[Notify origin thread]
    HA --> N
```

## Sources

[S3] [S7] [S9] [R]

## Go deeper

1. [Risk × kind](risk-times-kind.md): the full matrix and how the ceiling is computed.
2. [Human review and hold](human-review-and-hold.md): what people review and how they stop the line.
3. [Incidents](incidents.md): fast to a candidate fix, never merged without a person.

## Up

[Manifesto](../../README.md)
