---
id: 00-journey/feature
level: 2
parent: README.md
children: []
summary: The same journey for a feature, "add a date filter to the CSV export"; triage asks a question first, the builder maps each criterion to a test, and a person always approves.
prerequisites: [README.md]
---

# The journey of a feature

> **In short:** same nine stages. The differences are more care before the code, one test per
> criterion, and a person who always approves.

Bruno, a product manager, writes:

> **Bruno:** @factory add a date filter to the CSV export.

## Where it differs from the bug

| Stage | Bug (Ana) | Feature (Bruno) |
|---|---|---|
| 2. Triage | Ready at once | **Asks a question:** "Filter by order date or payment date?" Job → `needs_info` until Bruno answers. |
| 2. Triage | Size S | Size M. A larger request would be split into a stack: small parts built one after another. |
| 4. Build | First step: a failing test | First step: **map each criterion to a test** |
| 6. Evidence | Before/after test output | A checklist, criterion → test or screenshot |
| 8. Merge | Auto-merge | **Always a person**, even at `risk:low` |

## The flow

The diagram shows the job states for Bruno's request. Note the loop through `needs_info`.

```mermaid
stateDiagram-v2
    [*] --> triage: Bruno's message
    triage --> needs_info: which date field?
    needs_info --> triage: "payment date"
    triage --> building: criteria clear, size M
    building --> reviewing: PR with criteria checklist
    reviewing --> awaiting_human: kind feature
    awaiting_human --> merged: Bruno's team lead approves
    merged --> [*]
    class triage,building,reviewing,merged state
    class needs_info stop
    class awaiting_human state
    classDef person fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef script fill:#f1f5f9,stroke:#64748b,color:#0f172a
    classDef agent fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef state fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef stop fill:#ffedd5,stroke:#ea580c,color:#7c2d12
```

## The acceptance criteria after Bruno's answer

1. The export page has "From" and "To" fields for the payment date.
2. Only rows with a payment date inside the range are exported, both ends included.
3. Leaving both fields empty exports all rows, as today.

Each criterion gets its own test. The PR shows a screenshot of the new fields.

## Why a person always approves

A feature changes what users see. It's the kind of work where the factory most often builds the
wrong thing, even when the code is correct. A person checks the result against the intent,
starting from the evidence, not the diff. User-visible changes go out behind a flag when the
product has flags [S8][S9].

> [!TIP]
> Spend the effort before the code. A clear question in triage costs Bruno ten seconds. A wrong
> guess costs a full build and review.

## Go deeper

[Request kinds](../01-work-intake/request-kinds.md) · [Sizing and stacks](../01-work-intake/sizing-and-stacks.md) · [Risk × kind](../06-merge-policy/risk-times-kind.md)

## Up

[The journey of a request](README.md)
