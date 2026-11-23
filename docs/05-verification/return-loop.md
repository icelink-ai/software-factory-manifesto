---
id: 05-verification/return-loop
level: 2
parent: README.md
children: []
summary: Requested changes go back to the builder with the findings as input, counted by hidden markers on the PR; the third return puts the job on hold and tells a person.
prerequisites: [independent-reviewer.md]
---

# Return loop

> Back pressure is good. Infinite back pressure is a bill.

## Rules

- **VE-29** When the reviewer requests changes, the spine MUST send the PR back to the builder with
  the review findings as work material.
- **VE-30** The number of returns MUST be counted in a durable place attached to the PR (for
  example hidden markers in comments), not in the agent's memory.
- **VE-31** After a fixed number of returns (we use two), the next request for changes MUST put
  the job on `hold`, comment the reason on the PR and notify the origin thread.
- **VE-32** On each return, the builder MUST address the findings or reply why a finding is wrong.
  It MUST NOT silently ignore one.

## Diagram

```mermaid
stateDiagram-v2
    reviewing --> changes_requested: reviewer asks for changes
    state count <<choice>>
    changes_requested --> count
    count --> building: returns < 2, findings as input
    count --> hold: third request
    building --> reviewing: updated PR
    hold --> building: person resumes
    hold --> triage: person re-scopes
```

## Sources

[S3] [S8] [R]

## Up

[05. Verification](README.md)
