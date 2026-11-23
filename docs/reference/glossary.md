---
id: reference/glossary
level: 2
parent: ../../README.md
children: []
summary: Definitions of every term the manifesto uses with a specific meaning.
prerequisites: []
---

# Glossary

Terms are listed alphabetically. Pages use these terms with exactly this meaning.

| Term | Definition |
|---|---|
| **Attempt** | One entry into the `building` state. The job counts attempts so loops are visible and can be bounded. |
| **Back pressure** | Any automatic signal that pushes an agent back to fix its own work: a failing check, a lint error, a reviewer finding. |
| **Briefing** | Memory retrieved for a task before the agent reads code: procedures, learnings and similar past runs. |
| **Builder** | The agent that implements a request and opens the pull request. |
| **Deterministic spine** | The non-LLM code (scripts, workflows, a state machine) that moves work between stages. LLMs make judgment calls inside stages; the spine decides what happens next. |
| **Evidence** | An artifact that proves a change does what it claims: a test that failed before and passes after, a screenshot, a video, a trace, a benchmark. |
| **Factory** | The whole system that turns requests into merged changes: intake, triage, build, gate, review, merge, memory and metrics. |
| **Factory-as-code** | The factory's definition (agents, prompts, models, policies, gates) kept in a versioned repository and changed through pull requests. |
| **Gate** | One deterministic script (lint, format, types, tests, build, repository guardrails) that must pass before a pull request exists. CI runs the same script. |
| **Hold** | A state, and a label, that stops all automation on a job until a person releases it. |
| **Job** | The record of one request moving through the factory: state, history, attempts, cost, links. |
| **Kind** | What a request is: `bug`, `feature`, `incident`, `docs`, `refactor` or `chore`. The second dimension next to risk. |
| **Merge ceiling** | The most autonomy a job may get at merge time. The effective ceiling is the most restrictive of risk, kind and protected paths. |
| **Protected path** | A path whose changes always need a human merge, whatever the risk: CI definitions, the factory's own definition, infrastructure, auth. |
| **Request** | A unit of work as a person states it (a chat message, an issue, an alert). Triage turns it into a job. |
| **Reviewer** | An agent separate from the builder, with a clean context, that reads the diff and the evidence and approves or requests changes. |
| **Risk** | How bad a wrong change could be: `low`, `medium` or `high`. Set by triage. |
| **Run** | One execution of one agent on one job, with its own id, recorded in memory. |
| **Scope** | The partition of memory an agent may read or write: its own, the project's, the domain's, or global. |
| **Slop** | Code that works today but degrades the codebase: duplicated logic, hacks justified by comments, tests that test nothing. |
| **Stack** | A large request split into ordered parts, each a small job. The next part starts only after the previous one merges. |
| **Triage** | The read-only step that classifies a request (risk, kind, size), rewrites acceptance criteria and asks questions when information is missing. |

## Up

[Manifesto](../../README.md)
