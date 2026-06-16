---
name: workflow-to-skill-converter
status: v0.1
confidence: high
verification_status: partial
updated_at_utc: 2026-06-16T14:25:28Z
source_ids:
  - github-agent-skills
  - anthropic-skills
  - prompt-engineering
starter_path: starters/workflow-to-skill-converter/SKILL.md
---

## One-Liner

Turn repeated operational workflows into a small, triggerable `SKILL.md`.

## Target User

Engineers and AI operators who repeatedly write the same runbook-like steps into prompts.

## Pain Point

Repeated workflows stay in chat history or docs. They are hard to discover, reuse, and improve over time.

## Why Now

Multi-agent runtimes now include local skill concepts, but many teams still keep stable processes in plain notes. Converting one workflow at a time to a skill gives immediate reuse.

## Evidence

- id: github-agent-skills
  evidence_type: github-repo
  source_url: https://github.com/search?q=SKILL.md&type=Repositories
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Skill-like folders and `SKILL.md` files are commonly used for repeatable instructions across repositories.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 365
  verification_status: partial
- id: anthropic-skills
  evidence_type: official-doc
  source_url: https://docs.anthropic.com/
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Claude and adjacent tool ecosystems document instruction bundles and invoke-style automation patterns.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 365
  verification_status: speculative
- id: prompt-engineering
  evidence_type: directory
  source_url: https://github.com/topics/prompt-engineering
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Prompt repositories contain repeated workflow-to-instruction transformations that suit skill conversion.
  signal_weight: weak
  confidence: low
  freshness_window_days: 180
  verification_status: partial

## Saturation Risk

Medium. Many repos publish skill ideas, but fewer focus on a strict workflow-to-skill conversion checklist.

## Differentiation

This card does not promise a generic library. It gives a practical entry point for one workflow conversion with a concrete starter.

## Starter Scope

- Input: one repeatable workflow.
- Output: one `SKILL.md` with trigger, fit, inputs, workflow, and output shape.
- Limit: one scope slice, no runtime-specific claim expansion.

## Expected Output

- A copy-pasteable `SKILL.md`.
- Clear non-goals.
- Ordered, testable workflow steps.
- Explicit missing-data list.

## Demo Input

```text
Input pattern: "Every Friday I manually:
1) pull incidents from support,
2) sort by urgency,
3) draft handoff notes,
4) assign owners."
```

## Launch Keywords

- workflow-to-skill
- runbook-converter
- instruction-standardization

## Quality Gate

- Frontmatter exists and uses valid YAML list source IDs.
- At least one evidence source has medium or strong weight.
- No false claim of cross-runtime validation.
- Starter output is minimal and verifiable.

## Do Not Build

- Do not auto-convert every document at once.
- Do not claim this replaces implementation or execution tooling.
