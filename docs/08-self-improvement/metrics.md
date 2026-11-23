---
id: 08-self-improvement/metrics
level: 2
parent: README.md
children: []
summary: Measure throughput, quality, flow, automation, cost and evidence from week one, with a baseline taken before the factory starts.
prerequisites: [record-everything.md]
---

# Metrics

> Without a baseline, a factory pilot becomes an opinion.

## Rules

- **SI-12** The baseline MUST be taken before the factory starts building for a team.
- **SI-13** The metrics below MUST be tracked per week, and SHOULD be split by risk and kind.
- **SI-14** Throughput MUST NOT be reported without a quality metric next to it.
- **SI-15** Budget limits (daily and monthly cost) MUST exist and MUST stop new dispatches when
  reached.

## The metric set

| Metric | Why it matters |
|---|---|
| Merged PRs per engineer per week | Throughput leadership understands |
| Share of merged PRs made by the factory | How much work moved to the factory |
| Revert rate and incidents per PR | Whether speed is producing slop |
| Lead time from request to production | The whole flow, not just coding |
| Human interactions per PR | Real degree of automation |
| Cost per PR, and share of cost spent on verification | Spend control, and whether verification is funded |
| Share of PRs with evidence | Whether review is moving to artifacts |
| Checks created from corrections | Whether the team tends the garden |
| Eval scores by failure type | Input to the improvement loop |
| Jobs in `hold` and `failed` per week, by reason | Where the factory gets stuck |

## Diagram

```mermaid
flowchart TB
    subgraph Speed
        M1[Merged PRs per engineer]
        M2[Lead time]
    end
    subgraph Quality
        M3[Revert rate]
        M4[Incidents per PR]
        M5[Eval scores]
    end
    subgraph Autonomy
        M6[Human interactions per PR]
        M7[Share made by factory]
    end
    subgraph Cost
        M8[Cost per PR]
        M9[Verification share]
    end
    Speed --- Quality
    Quality --- Autonomy
    Autonomy --- Cost
```

## Sources

[S1] [S2] [S4] [S5] [S8] [R]

## Up

[08. Self-improvement](README.md)
