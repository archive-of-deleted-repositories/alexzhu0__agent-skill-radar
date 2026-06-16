---
name: skill-quality-scorecard
status: v0.1
confidence: high
verification_status: partial
updated_at_utc: 2026-06-16T14:25:28Z
source_ids:
  - github-agent-skills
  - agent-evals
  - anthropic-skills
starter_path: null
---

## One-Liner

Score a candidate skill draft for trigger clarity, evidence handling, safety, and output reliability.

## Target User

Maintainers and contributors reviewing pull requests that add new `SKILL.md` content.

## Pain Point

Quality checks are inconsistent, and low-quality skills are merged with vague promises.

## Why Now

As skill ecosystems scale, reviewers need quick, repeatable checks that are cheaper than full implementation review.

## Evidence

- id: github-agent-skills
  evidence_type: github-repo
  source_url: https://github.com/search?q=SKILL.md+review&type=Repositories
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: GitHub skill sets already encode recurring checks such as scope, validation, and examples.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 365
  verification_status: partial
- id: agent-evals
  evidence_type: directory
  source_url: https://github.com/topics/llm-evaluation
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Evaluation culture has moved toward rubric and score-based review workflows.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 180
  verification_status: partial
- id: anthropic-skills
  evidence_type: official-doc
  source_url: https://docs.anthropic.com/
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Agent workflow guidance increasingly emphasizes explicit constraints and structured outputs.
  signal_weight: weak
  confidence: low
  freshness_window_days: 365
  verification_status: speculative

## Saturation Risk

Medium. Many repos mention quality checks, but few treat quality scoring as a shared first-class skill topic.

## Differentiation

Provides one small scoring card with a concrete output shape, not a full static lint engine.

## Starter Scope

- Input: a draft skill file.
- Output: a concise scorecard with acceptance gates.
- No automation or CI integration in v0.1.

## Expected Output

- Trigger clarity score.
- Evidence and safety score.
- Missing-data, non-goal, and uncertainty notes.

## Demo Input

```text
Draft skill: A prompt-only file that says "help users debug workflows" with no constraints.
```

## Launch Keywords

- quality-gates
- skill-lint
- review-checklist

## Quality Gate

- Every score item is measurable.
- Missing assumptions are explicit.
- The card is useful for human review before merge.

## Do Not Build

- Do not automate subjective judgments without human review.
- Do not replace maintainers with rigid grading that blocks all creative work.
