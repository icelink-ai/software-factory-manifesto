---
id: 09-adoption/anti-patterns
level: 2
parent: README.md
children: []
summary: The mistakes the sources saw teams make, and the questions where the sources disagree, with the position this manifesto takes on each.
prerequisites: []
---

# Anti-patterns and disagreements

> **In short:** most factory failures aren't model failures. They come from missing
> [back pressure](../reference/glossary.md): no automatic signal that pushes the agent back to
> fix its own work.

## The problem

The talks behind this manifesto report many things that went wrong. Each one is easy to repeat,
because it looks reasonable at the start. A longer instructions file, one more reviewer model, a
few more retries: each feels like progress.

The sources also disagree on some big questions. You should know where they disagree before you
copy any one team's setup.

## How to use this page

1. Before you change how the factory works, scan the first table for your idea.
2. If your idea is there, read the "Do this instead" column and the linked page.
3. If you face one of the open questions in the second table, start from our position, then
   check it against your own metrics.

## Anti-patterns

| Anti-pattern | What goes wrong | Do this instead | Source |
|---|---|---|---|
| Lights-off factory on day one | Models that extend their own code unsupervised degrade it steadily. Benchmark pass rates on ongoing maintenance stay low. | Build guardrails and verification first. Earn autonomy per kind. | [S8] |
| Comments as justification | Agents write prose that explains a hack instead of fixing the cause. | Ban most comments. Encode the rule in lint. | [S2] |
| Reviewer weaker than the builder | Nitpicks, misread intent, and rework loops that cost more. | Use a reviewer model at least as capable as the builder. | [S3] |
| Many models arguing in review | Tens of millions of tokens, and pedantic debates that lose sight of the product. | Use one reviewer, given the product requirements. | [S2] |
| An LLM as the orchestrator | Tokens spent on routing that code could do, and a flow you can't test. | Use a [deterministic spine](../02-deterministic-spine/README.md). | [S3] [S6] |
| Local chat prompting as the main mode | Work at human speed, secrets on laptops, no governance. | Run in the cloud, under policy. | [S4] [S7] |
| A generalist agent with broad tools | Severe side effects when it hallucinates a situation. | Use small domain agents with [least privilege](../03-guardrails/least-privilege-agents.md). | [S10] |
| Redundant tests | Wasted tokens and time, and a slower gate. | Add an eval that detects redundant tests. | [S5] |
| Public benchmarks for routing | They measure someone else's code. | Build a [benchmark from your own tasks](../08-self-improvement/evals-and-benchmarks.md). | [S5] [S10] |
| Growing the instructions file | Worse model behavior and conflicting rules. | Keep the file [minimal](../03-guardrails/minimal-agent-instructions.md). Move rules into checks. | [S7] |
| Unlimited retries | Cost explodes on borderline cases. | Allow a fixed number of rounds, then hold. | [R] |
| Fixing bugs you can't reproduce | Guesswork changes and regressions. | No reproduction, no PR. | [R] |

## Where the sources disagree

| Question | What the sources say | Our position |
|---|---|---|
| Should people read agent code? | One team auto-merges most product PRs after heavy work on its environment [S2]. Another shows quality decaying without supervision, and says keep reading [S8]. | Read everything at first. Earn auto-merge per kind, with metrics ([MG-15](../06-merge-policy/human-review-and-hold.md)). |
| Cheap models for review? | A tutorial found cheap reviewers counterproductive [S3]. Domain-agent advocates favor cheap models for small tasks [S10]. | Use a strong reviewer. Use cheap models only for narrow stages that have their own eval ([VE-24](../05-verification/independent-reviewer.md)). |
| How much AI review? | Debate between several models catches bugs, but it is expensive and drifts [S2]. | Invest in lint and architecture first. Use one reviewer. |
| One general agent or many specific ones? | General agents with an orchestrator [S1][S7]. Small domain agents [S10]. | A general agent for coding. Small least-privilege agents at the edges ([GR-30](../03-guardrails/least-privilege-agents.md)). |
| Buy or build? | Several speakers sell platforms [S1][S4][S8]. Others built theirs from a coding agent and scripts [S2][S3]. | Buy the commodity parts. Build the glue ([AD-04](README.md)). |
| Orchestrate with an LLM? | It is expensive in tokens [S6]. A deterministic spine of scripts works [S3]. | A deterministic spine. LLMs only for judgment ([SP-01](../02-deterministic-spine/README.md)). |

> [!NOTE]
> Speakers reported their headline numbers after six to twelve months of work on their
> environments. Read them as direction, not as targets. See [sources](../reference/sources.md).

## Sources

[S1] [S2] [S3] [S4] [S5] [S6] [S7] [S8] [S10] [R]

## Up

[09. Adoption](README.md)
