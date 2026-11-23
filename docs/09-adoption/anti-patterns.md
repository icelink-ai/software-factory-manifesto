---
id: 09-adoption/anti-patterns
level: 2
parent: README.md
children: []
summary: The failure modes the sources observed, and the questions where they disagree, with the position this manifesto takes on each.
prerequisites: []
---

# Anti-patterns and disagreements

> Most factory failures are not model failures. They are missing back pressure.

## Anti-patterns

| Anti-pattern | What happens | Instead | Source |
|---|---|---|---|
| Lights-off factory on day one | Models extending their own code without supervision degrade it steadily; benchmark pass rates on iterative maintenance stay low | Build guardrails and verification first; earn autonomy per kind | [S8] |
| Comments as justification | Agents write prose explaining hacks instead of fixing the cause | Ban most comments; encode the rule in lint | [S2] |
| Weaker reviewer than builder | Nitpicks, misread intent, rework loops that cost more | Reviewer model at least as capable as the builder | [S3] |
| Multi-model adversarial review | Tens of millions of tokens, pedantic arguments detached from product intent | One reviewer fed with product requirements | [S2] |
| LLM as orchestrator | Tokens spent on routing that code could do; untestable flow | Deterministic spine | [S3] [S6] |
| Interactive local prompting as the main mode | Human-speed throughput, secrets on laptops, no governance | Cloud runs with policy | [S4] [S7] |
| Generalist agent with broad tools | Catastrophic side effects from hallucinated situations | Small domain agents, least privilege | [S10] |
| Redundant tests | Token and time waste; slower gate | Eval that detects redundant tests | [S5] |
| Public benchmarks for routing | Measures someone else's code | Benchmark from your own tasks | [S5] [S10] |
| Growing the instructions file | Worse model behavior, conflicting rules | Minimal file; move rules into checks | [S7] |
| Unbounded retries | Cost explodes on borderline cases | Fixed rounds, then hold | [R] |
| Fixing unreproduced bugs | Speculative changes, regressions | No reproduction, no PR | [R] |

## Where sources disagree

| Question | Positions | This manifesto |
|---|---|---|
| Should people read agent code? | One team auto-merges most product PRs after heavy environment work [S2]; another shows unsupervised quality decay and says keep reading [S8] | Read everything at first; earn auto-merge per kind with metrics ([MG-15](../06-merge-policy/human-review-and-hold.md)) |
| Cheap models for review? | A tutorial found cheap reviewers counterproductive [S3]; domain-agent advocates favor cheap models for small tasks [S10] | Strong reviewer; cheap models only for narrow stages with their own eval ([VE-24](../05-verification/independent-reviewer.md)) |
| How much AI review? | Multi-model debate catches bugs but is expensive and drifts [S2] | Invest in lint and architecture first; one reviewer |
| One general agent or many specific ones? | General agents with an orchestrator [S1][S7]; small domain agents [S10] | General agent for coding; small least-privilege agents at the edges ([GR-30](../03-guardrails/least-privilege-agents.md)) |
| Buy or build? | Several speakers sell platforms [S1][S4][S8]; others assembled theirs from a coding agent and scripts [S2][S3] | Buy commodity parts; build the glue ([AD-04](README.md)) |
| Orchestrate with an LLM? | Expensive in tokens [S6]; a deterministic spine of scripts works [S3] | Deterministic spine; LLMs only for judgment ([SP-01](../02-deterministic-spine/README.md)) |

## Sources

[S2] [S3] [S4] [S5] [S6] [S7] [S8] [S10] [R]

## Up

[09. Adoption](README.md)
