---
id: 03-guardrails/least-privilege-agents
level: 2
parent: README.md
children: []
summary: Give each stage its own agent identity with only the tools it needs; use a general agent to code and small domain agents at the edges.
prerequisites: [deny-rules-and-protected-paths.md]
---

# Least-privilege agents

> **In short:** an agent can't do what it has no tool for. Give each one only what its job needs.

## The problem

It's tempting to run one powerful agent with access to everything: the repository, email, the
cloud console, the database. When that agent gets confused, it can do broad damage.

One speaker describes an agent with email access that tried to shut down production. It had
hallucinated a security incident [S10]. Nothing stopped it, because nothing limited it.

## How it works

1. **Give each stage its own identity.** Triage, build and review run as different accounts.
2. **Take the identity from authentication**, never from a parameter the agent passes. An agent
   can't claim to be someone else.
3. **Give read-only access by default.** Triage and review only read. Only the builder pushes,
   and only to its own branch.
4. **Use small domain agents at the edges.** Sorting alerts or customer feedback doesn't need a
   coding agent. A small agent with one or two tools, and its own eval, is cheaper and safer [S10].
5. **Grow access with trust**, like a new hire: read first, then small actions, then ownership [S9].

The table shows what each agent in the factory can do.

| Agent | Can | Can't |
|---|---|---|
| Triage | Read the repo, the spec and memory | Push, label, comment |
| Builder | Read the repo, push its own branch, open a PR, write its own memory | Merge, change CI, read secrets |
| Reviewer | Read the PR and evidence, comment, set a review label | Push code, merge |
| Alert triage | Read alerts, open an issue | Touch the repository |

## Example

When Ana's request arrives, the triage agent reads the `reports` module and the spec, and returns
its verdict as data. It has no way to edit the issue. A script applies the verdict. Later, the
builder can push to `factory/issue-412`, but not to `main`.

> [!NOTE]
> The sources disagree on general versus specialized agents. Some use a general agent with an
> orchestrator [S1][S7]. Others prefer many small ones [S10]. We use a general agent for coding
> and small agents at the edges.

## Checklist

- **GR-27** Each stage (triage, build, review, edge functions) MUST run under its own identity
  with its own permissions.
- **GR-28** Identity MUST come from authentication, never from a parameter the agent passes.
- **GR-29** Triage and review MUST be read-only on the repository. Only the builder MAY push, and
  only to its own branch.
- **GR-30** Edge functions (feedback triage, alert triage, data questions) SHOULD use small domain
  agents with one or two tools and their own eval.
- **GR-31** Access SHOULD grow with demonstrated reliability: read-only first, then scoped
  actions, then ownership of an outcome.

## Sources

[S1] [S7] [S9] [S10] [R]

## Up

[03. Guardrails](README.md)
