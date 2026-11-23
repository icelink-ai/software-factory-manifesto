---
id: 09-adoption
level: 1
parent: ../../README.md
children: [build-order.md, trust-ladder.md, human-roles.md, anti-patterns.md]
summary: Build guardrails and verification before autonomy, earn trust in steps, change what engineers do, and avoid the failure modes the sources observed.
prerequisites: []
---

# 09. Adoption

> Guardrails and verification first, isolated environments second, end-to-end automation third,
> measured self-improvement last.

Every source that reports high volume got there after six to twelve months of investment in the
environment, not by switching on a smarter model [S1][S2][S9]. The order matters more than the
tools.

## Rules

- **AD-01** The build order MUST be: guardrails and gate → isolated environments → end-to-end
  pipeline with human merge → auto-merge for low-risk kinds → self-improvement loop.
- **AD-02** Autonomy MUST grow one step at a time, per kind and per repository, driven by metrics.
- **AD-03** The factory SHOULD build itself: once the spine exists, new factory features are
  requested through the factory, one small module at a time.
- **AD-04** Buy commodity parts (the coding agent, sandboxes, previews); build only the glue
  (intake, gate, job state, merge policy, metrics).
- **AD-05** Engineers MUST own outcomes (a product area, a metric), not a queue of tickets handed
  to agents.

## Diagram

```mermaid
flowchart LR
    P0["Phase 0<br/>gate, lint rules, deny rules,<br/>minimal AGENTS.md, baseline metrics"] --> P1["Phase 1<br/>isolated cloud runs,<br/>local system with mocks"]
    P1 --> P2["Phase 2<br/>intake, triage, build, review;<br/>human merges everything"]
    P2 --> P3["Phase 3<br/>auto-merge docs, refactor, chore,<br/>low-risk bugs"]
    P3 --> P4["Phase 4<br/>evals, benchmarks,<br/>PRs against the factory,<br/>goal-oriented work"]
```

## Sources

[S1] [S2] [S4] [S5] [S7] [S8] [S9] [R]

## Go deeper

1. [Build order](build-order.md): what each phase delivers and its exit criteria.
2. [Trust ladder](trust-ladder.md): read-only, then action, then ownership.
3. [Human roles](human-roles.md): what engineers do in a factory.
4. [Anti-patterns and disagreements](anti-patterns.md): what failed, and where sources disagree.

## Up

[Manifesto](../../README.md)
