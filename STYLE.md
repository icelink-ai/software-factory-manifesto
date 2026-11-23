# Style guide

How we write this manifesto. It applies to people and to agents who edit it. The goal is simple:
a reader who has never built a software factory understands each page on the first read.

The guide draws on three sources:

- [Diátaxis](https://diataxis.fr/) for what kind of page to write.
- The [Google developer documentation style guide](https://developers.google.com/style/tone)
  for voice and tone.
- Google's [technical writing course](https://developers.google.com/tech-writing/two/large-docs)
  for progressive disclosure: answer first, detail later.

## 1. Pick the kind of page

Every page is one of four kinds. Don't mix them.

| Kind | Reader's question | In this manifesto |
|---|---|---|
| **Story** (tutorial) | "Show me how it works, start to finish." | [The journey of a request](docs/00-journey/README.md) |
| **Explanation** | "Why is it done this way?" | The theme pages, `docs/01-…` to `docs/09-…` |
| **How-to** | "How do I set this up?" | [Start your factory](docs/09-adoption/build-order.md) |
| **Reference** | "What exactly is the rule?" | [RULES.md](RULES.md), the glossary, the state machine |

## 2. Voice and tone

Write like a colleague who has built a factory and is explaining it to you over coffee.

- **Talk to the reader.** Use "you". Use "we" only for what our own team did.
- **Use active voice.** Say who does the action: "The triage agent sets the risk", not "the
  risk is set".
- **Lead with the answer.** The first sentence of a page or section says the point. Detail
  comes after.
- **Use plain words.** "Use" not "utilize", "start" not "initiate", "check" not "validate"
  (unless you mean schema validation).
- **Define a term the first time you use it**, in the same sentence, and link the
  [glossary](docs/reference/glossary.md).
- **Don't announce.** Skip "This section describes…" and "It is important to note that…".
  Just say the thing.
- **Don't oversell.** No "powerful", "seamless", "revolutionary". Numbers from talks are
  reported as what the speaker said, never as targets.

## 3. Sentences and paragraphs

| Measure | Target |
|---|---|
| Average sentence length | 20 words or fewer |
| Longest sentence | 35 words |
| Paragraph | One idea, at most four sentences |
| Page opening | One sentence that answers the page's question |

`scripts/check.py` reports sentence length for every page.

- Put steps that happen in order in a **numbered list**.
- Put options that you compare in a **table**.
- Put a warning or a tip in an **alert** (below), not in the middle of a paragraph.

## 4. Page layout

Explanation pages (themes and subtopics) use these sections, in this order:

1. `# Title`, then a one-line answer as a quote: `> **In short:** …`
2. `## The problem`: what goes wrong without this practice. Two or three short paragraphs.
3. `## How it works`: numbered steps, then a diagram.
4. `## Example`: the practice applied to the running example (below).
5. Alerts where they help: tip, warning, note.
6. `## Checklist`: the rules, with their ids and MUST/SHOULD/MAY.
7. `## Sources`, then `## Up` (and `## In this section` on theme pages).

Story pages (the journey) use a fixed card instead. See any page in `docs/00-journey/`.

## 5. The running example

All pages reuse one request, so the reader meets the same characters everywhere:

> Ana, a support engineer, writes in the team chat: "@factory the CSV export loses accents.
> 'São Paulo' comes out as 'SÃ£o Paulo'."

It is a `bug` of `risk:low` in the `reports` module. For features we use "add a date filter to
the CSV export"; for incidents, "the export endpoint returns 500 since the last release".

## 6. Alerts

Use GitHub alerts. They render on GitHub and on the site.

```markdown
> [!TIP]
> A shortcut or a good default.

> [!WARNING]
> An anti-pattern: what people do, and what goes wrong.

> [!NOTE]
> Context, or a point where the sources disagree.

> [!IMPORTANT]
> Something the reader must not miss.
```

At most three alerts per page. If everything is highlighted, nothing is.

## 7. Diagrams

- **One idea per diagram, at most 12 boxes.** Split a big diagram into small ones.
- **Introduce it** with one sentence ("The diagram shows what happens when the gate fails.")
  and, when it has more than four steps, explain it after with a numbered list.
- **Use the same colors everywhere**, so the reader can tell who acts:

| Color | Who or what | `class` name |
|---|---|---|
| Blue | A person | `person` |
| Gray | A deterministic script or service | `script` |
| Purple | An AI agent | `agent` |
| Green | A job state | `state` |
| Orange | A stop: hold, failure, refusal | `stop` |

Paste these lines at the end of every `flowchart` and `stateDiagram-v2`:

```text
classDef person fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
classDef script fill:#f1f5f9,stroke:#64748b,color:#0f172a
classDef agent fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
classDef state fill:#dcfce7,stroke:#16a34a,color:#14532d
classDef stop fill:#ffedd5,stroke:#ea580c,color:#7c2d12
```

In `sequenceDiagram`, use `actor` for people, and group participants with colored boxes:
`box rgb(237,233,254) Agents`, `box rgb(241,245,249) Scripts`.

## 8. Rules (the checklist)

- Rule ids never change. A retired rule stays with `(retired)`.
- A rule is one sentence when possible, two at most, with one MUST, SHOULD or MAY.
- The explanation lives in the text above the checklist, not in the rule.

## 9. Before you open a PR

```bash
python scripts/check.py --write   # structure, links, ids, readability, RULES.md and llms.txt
npm run docs:build                # site build, fails on dead links
```
