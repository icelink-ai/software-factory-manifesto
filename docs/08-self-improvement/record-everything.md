---
id: 08-self-improvement/record-everything
level: 2
parent: README.md
children: []
summary: Keep a central record of every agent session (conversation, tools, diffs, evidence, cost) linked to its job; it is the raw material for evals, memory and improvement.
prerequisites: []
---

# Record everything

> You cannot improve what you did not keep.

## Rules

- **SI-07** Each run MUST store, linked to its job and run id: the conversation, tool calls and
  outputs, the diff, evidence artifacts, cost, duration and outcome.
- **SI-08** The record MUST be centralized (one system of record across agents and teams), not
  scattered across CI logs and laptops.
- **SI-09** Cost and duration MUST be attributed per stage (triage, build, each review round).
- **SI-10** Raw artifacts SHOULD expire on a schedule; summaries and learnings MAY be kept longer.
- **SI-11** Records MUST NOT contain secrets. Redaction MUST happen before storage.

## Diagram

```mermaid
flowchart LR
    T[Triage run] --> SOR
    B[Build run] --> SOR
    R1[Review round 1] --> SOR
    R2[Review round 2] --> SOR
    SOR[("System of record<br/>by job and run id")] --> EV[Evals]
    SOR --> MEM[Memory learnings]
    SOR --> MET[Metrics]
    SOR --> BM[Benchmark task set]
```

## Sources

[S4] [S5] [S8] [R]

## Up

[08. Self-improvement](README.md)
