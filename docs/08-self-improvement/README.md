---
id: 08-self-improvement
level: 1
parent: ../../README.md
children: [record-everything.md, metrics.md, evals-and-benchmarks.md, factory-as-code.md]
summary: The factory is defined in code, records everything its agents do, measures itself with metrics and evals on its own data, and improves through pull requests against its own definition.
prerequisites: [../02-deterministic-spine/README.md, ../07-memory-and-context/README.md]
---

# 08. Self-improvement

> A factory that does not measure itself is running on vibes. A factory that measures itself can
> propose its own improvements.

## Rules

- **SI-01** The factory's definition (agents, prompts, models, triggers, tools, gate, policy) MUST
  be code in a repository, changed only through pull requests.
- **SI-02** Every session MUST be recorded: conversation, tool calls, diffs, evidence, cost,
  duration, outcome.
- **SI-03** A baseline of delivery metrics MUST be measured before the factory starts, and the same
  metrics MUST be tracked continuously.
- **SI-04** Quality MUST be measured with online evals on recorded sessions and with benchmarks
  built from the team's own past tasks, not with public benchmarks alone.
- **SI-05** Agents SHOULD aggregate failures into patterns and open pull requests against the
  factory definition; those PRs MUST be merged by people (protected paths).
- **SI-06** Goal-oriented work ("reduce p99", "keep parity") SHOULD start only after evals and
  metrics exist for the goal.

## Diagram

```mermaid
flowchart LR
    RUN["Factory runs jobs"] --> REC["Record everything<br/>sessions, evidence, cost"]
    REC --> EV["Online evals<br/>LLM-as-judge scorers"]
    REC --> MET["Metrics<br/>throughput, reverts, cost"]
    EV --> AGG["Agent aggregates failures<br/>finds patterns"]
    MET --> AGG
    AGG --> PR["PR against factory definition<br/>prompt, check, skill, routing"]
    PR --> BM{"Benchmark on own tasks<br/>better cost x quality?"}
    BM -->|yes| HM["Human merge"]
    BM -->|no| X[Discard]
    HM --> RUN
```

## Sources

[S1] [S4] [S5] [S8] [S10] [R]

## Go deeper

1. [Record everything](record-everything.md): sessions as the raw material.
2. [Metrics](metrics.md): what leadership and the factory itself should watch.
3. [Evals and benchmarks](evals-and-benchmarks.md): measuring quality on your own work.
4. [Factory-as-code](factory-as-code.md): versioning, A/B tests and rollback of the factory itself.

## Up

[Manifesto](../../README.md)
