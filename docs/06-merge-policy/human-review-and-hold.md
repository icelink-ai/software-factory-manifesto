---
id: 06-merge-policy/human-review-and-hold
level: 2
parent: README.md
children: []
summary: People review the evidence and the product fit rather than every line, approve where the request started, and can stop any job at any time with hold.
prerequisites: [risk-times-kind.md]
---

# Human review and hold

> **In short:** people spend their attention on judgment, and they keep the brake.

## The problem

When an agent opens many pull requests, reading every line of every diff becomes the bottleneck.
And a line-by-line read can still miss the real question: does this change do what was asked?

People also need a way to stop the factory. If stopping a bad run takes a code change or a call to
the person who set things up, the run keeps going in the meantime.

## How it works

1. **Start from the evidence.** The reviewer reads the acceptance criteria and the proof first:
   tests, screenshots, traces. Then they read the diff where the evidence is thin.
2. **Approve where the request started.** For example, a one-click approval in the chat thread
   that links to the PR.
3. **Dogfood user-visible changes.** They go through internal dogfooding before general release.
   Without it, they never auto-merge.
4. **Start with people on every PR.** Until lint, the gate and verification are mature, people
   review everything. The auto-merge list starts empty.
5. **Anyone with write access can hold.** Putting a PR or job on [hold](../reference/glossary.md)
   stops every automated action on it. A person later resumes it or sends it back to triage.

The diagram shows where a person can step in.

```mermaid
stateDiagram-v2
    reviewing --> awaiting_human: policy requires people
    awaiting_human --> merged: approvals reached
    awaiting_human --> changes_requested: person asks for changes
    awaiting_human --> hold: person stops
    reviewing --> hold: person stops
    building --> hold: person stops
    hold --> building: person resumes
    hold --> triage: person re-scopes
    class reviewing,awaiting_human,merged,changes_requested,building,triage state
    class hold stop
    classDef person fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef script fill:#f1f5f9,stroke:#64748b,color:#0f172a
    classDef agent fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef state fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef stop fill:#ffedd5,stroke:#ea580c,color:#7c2d12
```

## Example

Say the factory is new, so the auto-merge list is still empty. Ana's bug fix waits in
`awaiting_human`, even though it is `risk:low`.

A reviewer opens Ana's chat thread and follows the link to the PR. They read the test output
first: it failed with "SÃ£o Paulo" before the fix and passes after. The evidence is strong, so they
skim the diff and approve with one click in the thread.

If they had spotted a change to an unrelated module, they would put the PR on `hold`. Nothing
would move until a person released it.

> [!NOTE]
> The sources disagree on how much people should read. One team lets agents merge almost every
> product PR, after investing heavily in its environment [S2]. Another speaker shows that
> unsupervised models steadily degrade a codebase over repeated changes, and argues that teams must keep
> reading the code [S8]. Our position: earn autonomy kind by kind, starting with docs and
> refactors. Widen it only while revert and incident rates stay low.

## Checklist

- **MG-11** Human reviewers SHOULD start from the evidence and the acceptance criteria, then read
  the diff where the evidence is thin.
- **MG-12** Approval SHOULD be possible from where the request started (for example a one-click
  approval in the chat thread that links to the PR).
- **MG-13** Any person with write access MUST be able to put any PR or job on `hold`, and `hold`
  MUST stop every automated action on it.
- **MG-14** User-visible changes SHOULD go through internal dogfooding before general release;
  without it they are never auto-merged.
- **MG-15** Until lint, gate and verification are mature, people SHOULD review every PR, and the
  auto-merge list SHOULD start empty.

## Sources

[S1] [S2] [S7] [S8] [S9] [R]

## Up

[06. Merge policy](README.md)
