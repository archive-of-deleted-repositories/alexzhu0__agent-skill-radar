# Agent Skill Radar

A radar for high-signal Agent Skill ideas.

## Why

This repository helps builders choose **which Agent Skill topic to build next**.

It is not a huge skill pack. It is a small set of practical topic cards and starter SKILL templates for repeatable planning work.

## Who it is for

- Builders creating `SKILL.md` for Codex, Claude Code, Copilot, Cursor, and Gemini CLI.
- PM/dev teams that need clearer skill boundaries and launch-ready scope.
- Maintainers reviewing what to build next with limited bandwidth.

## Install

Clone or copy this repository, then read the topic cards directly. There is no package install step for v0.1.

## Why another skill repo is not enough

Agent Skill ecosystems are growing quickly, but many repos are broad and repetitive.

This repo gives a smaller signal: evidence-backed topics plus immediate starter shape.

- What to build
- Why it matters now
- What not to build
- What output to produce first

## Quickstart

1. Open the top 7 table and pick one card.
2. Read one full topic card.
3. Copy one starter `SKILL.md`.
4. Draft one candidate topic card in the same format and review it with the checklist.

## Top 7 topic cards

| Topic | User | Pain | Evidence status | Saturation | Starter output |
| --- | --- | --- | --- | --- | --- |
| workflow-to-skill-converter | Builders with repeated workflows | Repeated manual workflow docs never become skills | partial | medium | `SKILL.md` trigger and output shape |
| prompt-to-skill-spec | Prompt-heavy teams | Good prompts are not reusable specs | partial | medium | `SKILL.md` conversion scaffold |
| skill-example-generator | New skill contributors | Vague ideas rarely become publishable examples | partial | low | example generation starter |
| skill-quality-scorecard | Maintainers and reviewers | No shared quality lens for new skills | partial | medium | scoring rubric template |
| skill-install-doctor | Builders fixing runtime setup | Good skill fails discovery or invocation | partial | low | issue diagnosis checklist |
| skill-release-kit | Maintainers shipping skill repos | Release metadata is inconsistent | partial | medium | launch bundle checklist |
| skill-market-map | Builders doing topic choice | Popularity is confused with quality | partial | high | market and saturation notes |

## Examples

### From vague idea to a starter skill

**Before**

```text
I keep writing ad-hoc agent prompts for onboarding, but no one knows which one should be a skill.
```

**After**

1. Read `topics/skill-market-map.md` to compare saturation and demand.
2. Use `starters/workflow-to-skill-converter/SKILL.md` to convert the workflow into a triggerable `SKILL.md`.
3. Run your own first draft through `reviews/topic-card-review-checklist.md`.

## Repository layout

- `topics/` topic cards for v0.1
- `starters/` starter SKILL templates
- `data/` topic index data
- `reviews/` human checklist and review results
- `examples/` before/after references
- `releases/` release notes

## FAQ

**Is this a star farm or clone-count game?**

No. Cards must include saturation analysis and `Do Not Build` notes.

**Does this call model APIs automatically?**

Not in this repository. It is markdown-first planning.

**Can this build a full skill by itself?**

Not directly. It gives topic and structure guidance for your next implementation.

## Contributing

Use the checklist for every new card:

1. Add frontmatter with evidence IDs.
2. Keep the 13 required headings in order.
3. Add at least one source with medium or strong signal weight.
4. Add the card to `data/topic-index.yaml`.
5. Log the review result.

## API

No runtime API. The public artifact is the repository content itself.

## License

MIT
