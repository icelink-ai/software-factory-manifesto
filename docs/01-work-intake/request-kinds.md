---
id: 01-work-intake/request-kinds
level: 2
parent: README.md
children: []
summary: Every request gets one of six kinds. The kind adds no states to the pipeline; it changes what the request must contain, the builder's first step, the proof in the PR and how much autonomy the merge gets.
prerequisites: [triage-and-risk.md, ../02-deterministic-spine/job-state-machine.md]
---

# Request kinds

> **In short:** one pipeline, six kinds. The kind adds no states. It changes what goes in, what
> the builder does first, what proof comes out, and how much autonomy the merge gets.

## The problem

A bug, a feature and an incident need different proof. It's tempting to build a separate
pipeline, prompt set and dashboard for each. That multiplies maintenance and hides the shared
spine.

None of the sources runs a separate pipeline per kind of work. They all use one skeleton: intake,
triage with risk, a spec or a reproduction, an isolated build, a deterministic gate, review and
merge. They vary only the evidence and the degree of autonomy [S1][S3][S7][S8][S9].

## How it works

The [kind](../reference/glossary.md) says what a request is: `bug`, `feature`, `incident`, `docs`,
`refactor` or `chore`. It acts at four points of the same pipeline.

1. **Triage picks exactly one kind.** When unsure between two, it picks the more restrictive one.
   A bug fix that needs new behavior is a `feature`. An item with no kind counts as a `feature`.
2. **Triage checks the kind's template.** If a required field is missing, the job goes to
   `needs_info`.
3. **The builder's first step depends on the kind.** A `bug` or an `incident` starts with a test
   that fails.
4. **The reviewer demands the kind's evidence**, and the merge applies the kind's ceiling.

The **merge ceiling** is the most autonomy a job may get at merge time. The effective ceiling is
the most restrictive of risk, kind and protected paths. See [Risk × kind](../06-merge-policy/risk-times-kind.md).

### What goes in

| Kind | Use it when | The request must contain | Builder's first step |
|---|---|---|---|
| `bug` | Existing behavior is wrong | Steps to reproduce, expected vs actual, where | Write a test that reproduces the failure and see it fail on main |
| `feature` | New behavior, or a change users can see | Goal, who uses it, acceptance criteria you can check | Map each criterion to a test or check |
| `incident` | Production error (alert, error tracker, urgent report) | Alert or log link, release, frequency | Write a regression test that reproduces the error, and a root-cause note |
| `docs` | Documentation, text or copy only | What changes and why | Edit |
| `refactor` | Internal improvement with no behavior change, including new lint rules | What improves and why | Run the existing tests before touching code |
| `chore` | Dependencies, CI, build, configuration | What to update, to which version | Read the release notes |

### What comes out

| Kind | Evidence in the PR | Merge ceiling | Minimum people |
|---|---|---|---|
| `bug` | Test fails on main and passes on the branch; screenshot or video if visual | Auto-merge if `risk:low` | 0 |
| `feature` | Checklist: each criterion → its test or artifact | Never auto-merge | 1 |
| `incident` | Regression test and diagnosis | Never auto-merge | 1 (on call) |
| `docs` | The diff touches documentation paths only | Auto-merge if `risk:low` | 0 |
| `refactor` | Existing tests unchanged (only additions allowed) | Auto-merge if `risk:low` | 0 |
| `chore` | Gate green; release notes in the PR | Auto-merge if `risk:low` | 0 |

Goal-oriented work, such as "bring p99 latency under 200 ms" or "keep Android at parity with
iOS", is not a kind. It is a long-running objective that spawns jobs of these kinds. It needs evals
and measurement first [S1]. See [Self-improvement](../08-self-improvement/README.md).

### Where the kind acts on the state machine

The diagram shows the shared [job state machine](../02-deterministic-spine/job-state-machine.md).
The notes mark the three places where the kind matters.

```mermaid
stateDiagram-v2
    [*] --> triage: request from chat, issue or alert
    triage --> needs_info: a field the kind requires is missing
    needs_info --> triage: requester answers
    triage --> building: kind and risk assigned
    triage --> hold: stack, parts 2 to N wait
    building --> reviewing: PR opened with the kind's evidence
    building --> hold: bug or incident not reproduced
    building --> failed: execution error
    reviewing --> changes_requested: the kind's evidence is missing
    changes_requested --> building: rounds 1 and 2
    changes_requested --> hold: third return
    reviewing --> merged: auto-merge, risk and kind allow it
    reviewing --> awaiting_human: risk or kind requires people
    awaiting_human --> merged: approvals of the stricter rule
    awaiting_human --> changes_requested: person asks for changes
    failed --> triage: retry
    hold --> triage: person unblocks
    hold --> building: person resumes
    merged --> [*]
    note right of triage
        Sets kind and risk
        Checks the kind's template
    end note
    note right of building
        First step depends on kind
        bug and incident start with a failing test
    end note
    note right of reviewing
        Reviewer demands the kind's evidence
        Merge applies the kind's ceiling
    end note
    class triage,needs_info,building,reviewing,changes_requested,awaiting_human,merged state
    class hold,failed stop
    classDef person fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef script fill:#f1f5f9,stroke:#64748b,color:#0f172a
    classDef agent fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef state fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef stop fill:#ffedd5,stroke:#ea580c,color:#7c2d12
```

### `bug`: prove it, then fix it

The builder must see the bug before it fixes it. Inside `building`, the purple steps are the
agent's work.

```mermaid
stateDiagram-v2
    [*] --> triage: kind bug
    triage --> needs_info: no steps, expected or actual
    needs_info --> triage
    triage --> building
    state building {
        [*] --> reproduce: write a new test
        reproduce --> confirm: run it on main
        confirm --> fix: fails as described
        fix --> prove: test passes, gate green
        prove --> [*]
    }
    building --> hold: not reproduced
    hold --> triage: requester adds detail
    building --> reviewing: PR with the test and before/after output
    reviewing --> changes_requested: no reproduction test, or it didn't fail before
    changes_requested --> building
    reviewing --> merged: risk low, auto-merge
    reviewing --> awaiting_human: risk medium or high
    awaiting_human --> merged
    merged --> [*]
    class triage,needs_info,reviewing,changes_requested,awaiting_human,merged state
    class reproduce,confirm,fix,prove agent
    class hold stop
    classDef person fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef script fill:#f1f5f9,stroke:#64748b,color:#0f172a
    classDef agent fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef state fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef stop fill:#ffedd5,stroke:#ea580c,color:#7c2d12
```

### `feature`: invest before the code

A feature always needs a person. Most of the work is mapping each criterion to a proof.

```mermaid
stateDiagram-v2
    [*] --> triage: kind feature
    triage --> needs_info: no goal or no checkable criteria
    needs_info --> triage
    triage --> building: size S or M
    triage --> hold: size L becomes a stack
    hold --> triage: previous part merged
    state building {
        [*] --> map_criteria: each criterion to a test
        map_criteria --> implement
        implement --> verify: tests and artifacts per criterion
        verify --> [*]
    }
    building --> reviewing: PR with the criteria checklist
    reviewing --> changes_requested: a criterion has no proof
    changes_requested --> building
    reviewing --> awaiting_human: always
    awaiting_human --> merged: at least one person
    merged --> [*]
    class triage,needs_info,reviewing,changes_requested,awaiting_human,merged state
    class map_criteria,implement,verify agent
    class hold stop
    classDef person fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef script fill:#f1f5f9,stroke:#64748b,color:#0f172a
    classDef agent fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef state fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef stop fill:#ffedd5,stroke:#ea580c,color:#7c2d12
```

User-visible changes should ship behind a flag where the product has flags. They should go
through internal dogfooding before general release [S8][S9].

### `incident`: the page arrives with a PR

An incident optimizes for speed to a candidate fix. The on-call person always merges.

```mermaid
stateDiagram-v2
    [*] --> triage: kind incident, from an alert
    triage --> building: alert link and release present
    triage --> needs_info: no link or log
    needs_info --> triage
    state building {
        [*] --> reproduce: regression test from the error
        reproduce --> diagnose: root-cause note
        diagnose --> fix
        fix --> [*]
    }
    building --> hold: not reproduced, on call decides
    building --> reviewing: PR with regression test and diagnosis
    reviewing --> awaiting_human: always
    awaiting_human --> merged: on-call person merges
    merged --> [*]
    class triage,needs_info,reviewing,awaiting_human,merged state
    class reproduce,diagnose,fix agent
    class hold stop
    classDef person fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef script fill:#f1f5f9,stroke:#64748b,color:#0f172a
    classDef agent fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef state fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef stop fill:#ffedd5,stroke:#ea580c,color:#7c2d12
```

The value is speed, not autonomy. One speaker says even a fix that is right half the time changes
the on-call experience [S8]. No source argues for merging incident fixes without a person. See
[Incidents](../06-merge-policy/incidents.md) for the alert on stuck incident jobs.

### `docs`, `refactor` and `chore`: autonomy earned by static checks

These kinds can merge on their own at `risk:low`, because the gate can check most of what matters.

```mermaid
stateDiagram-v2
    [*] --> triage: kind docs, refactor or chore
    triage --> building
    state building {
        [*] --> baseline: run the gate before changes
        baseline --> change
        change --> check: gate green, tests intact
        check --> [*]
    }
    building --> reviewing
    reviewing --> changes_requested: docs touched code, refactor changed tests, chore lacks notes
    changes_requested --> building
    reviewing --> merged: risk low and no protected path
    reviewing --> awaiting_human: otherwise
    awaiting_human --> merged
    merged --> [*]
    class triage,reviewing,changes_requested,awaiting_human,merged state
    class baseline,change,check agent
    classDef person fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef script fill:#f1f5f9,stroke:#64748b,color:#0f172a
    classDef agent fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef state fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef stop fill:#ffedd5,stroke:#ea580c,color:#7c2d12
```

Small text changes need no person after the checks pass [S7]. A pattern fixed by hand twice
should become a lint rule through a `refactor` job [S2]. See
[Lint rules that teach](../03-guardrails/teaching-lint-rules.md).

## Example

Triage gives Ana's request the kind `bug`. Her message already has the steps, the expected result
and the actual result, so the template is complete.

The builder's first step is a test. It exports a row with "São Paulo" and checks the text that a
spreadsheet app reads back. On main, the test fails with "SÃ£o Paulo", exactly as Ana described.
The builder fixes the encoding, and the test passes. The PR shows the test output before and
after. The risk is `low` and the kind allows it, so the PR can auto-merge.

> [!IMPORTANT]
> Protected paths force a human merge for **every** kind, not only `docs` (`GR-24`, `MG-09`).

> [!WARNING]
> **Treating the source as the kind.** "It came from the error tracker, so it's an incident" is
> wrong. Source says where a request came from; kind says what it is.

> [!WARNING]
> **Fixing a bug nobody reproduced.** Without a failing test, you can't tell whether the fix fixes
> anything. Stop and put the job on hold instead.

## Checklist

- **IN-19** Triage MUST assign exactly one kind: `bug`, `feature`, `incident`, `docs`, `refactor`
  or `chore`.
- **IN-20** When unsure between two kinds, triage MUST pick the more restrictive one. A bug fix
  that needs new behavior is a `feature`.
- **IN-21** An item with no kind MUST be treated as `feature`.
- **IN-22** Kind MUST NOT add states to the job state machine. It sets parameters on the existing
  stages.
- **IN-23** The effective merge ceiling MUST be the most restrictive of risk, kind and protected
  paths (see [Risk × kind](../06-merge-policy/risk-times-kind.md)).
- **IN-24** A `bug` or `incident` that the builder can't reproduce MUST stop with no PR and go to
  `hold` with a "not reproduced" note. The requester (for an incident, the on-call person) MUST be
  told.

## Sources

[S1] [S2] [S3] [S7] [S8] [S9] [R]

## Up

[01. Work intake](README.md)
