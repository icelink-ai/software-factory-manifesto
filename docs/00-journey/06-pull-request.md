---
id: 00-journey/06-pull-request
level: 2
parent: README.md
children: []
summary: Stage 6. The builder opens a pull request whose description proves the fix (test output before and after, a screenshot) criterion by criterion; scripts label it and the job moves to reviewing.
prerequisites: [05-gate.md]
---

# Stage 6. Pull request with evidence

> **In short:** the pull request doesn't say "fixed". It shows the proof, one acceptance
> criterion at a time.

| | |
|---|---|
| **Who acts** | Builder agent (AI), PR script (script) |
| **Goes in** | A branch that passed the gate, plus the evidence the builder collected |
| **Comes out** | A pull request with labels `factory-made` and `risk:low` |
| **Job state** | `building` → `reviewing` |
| **Takes** | A minute |

## What happens

1. The builder opens the pull request. The description links issue 412 and has a
   **Verification** section, organized by acceptance criterion.
2. A script adds the label `factory-made` and copies `risk:low` and `kind:bug` from the issue.
3. The job script records the PR number and moves the job to `reviewing`.
4. CI starts. It runs the same gate script. When CI passes, the review workflow starts the
   reviewer (stage 7).

## What the pull request says

> **Fix: CSV export keeps accented characters**
>
> Closes issue 412. Writes CSV files as UTF-8 with a byte-order mark, so spreadsheet apps detect
> the encoding.
>
> **Verification**
>
> | Criterion | Evidence |
> |---|---|
> | Test reproduces the bug on main | `test_export_keeps_accents` on `main`: **FAILED**, got `S\xc3\x83\xc2\xa3o Paulo` |
> | Export shows "São Paulo" in a spreadsheet app | Same test on this branch: **PASSED**. Screenshot of the file opened in a spreadsheet app attached. |
>
> **Out of scope:** PDF and XLSX exports.

## Why it works this way

- **Review proof, not prose.** A test that failed before and passes now is evidence. "I fixed
  it" is a claim [S2].
- **Evidence by kind.** A bug needs a reproduction test. A feature needs one check per
  criterion. A docs change needs a diff limited to documentation. The kind, set in triage,
  tells the builder what to collect.
- **Screenshots and videos come from the sandbox.** The builder drives the app like a user,
  so a person can check the result without opening an editor [S1][S9].

## What can go wrong

| Problem | What the factory does |
|---|---|
| The verification section is missing | The reviewer requests changes in stage 7. |
| The PR changes after CI passed | The merge script waits for CI on the latest commit. |

## Go deeper

[Evidence artifacts](../05-verification/evidence-artifacts.md) · [Verification](../05-verification/README.md)

## Next

[Stage 7. Review](07-review.md)

## Up

[The journey of a request](README.md)
