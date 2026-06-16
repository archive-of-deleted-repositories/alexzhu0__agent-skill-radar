---
name: skill-example-generator
status: v0.1
confidence: medium
verification_status: partial
updated_at_utc: 2026-06-16T14:25:28Z
source_ids:
  - awesome-llm-apps
  - prompt-engineering
  - github-agent-skills
starter_path: null
---

## One-Liner

Create a concrete before/after example block for a candidate skill to make value and boundaries obvious.

## Target User

Skill authors who need to show what output should change with one real input.

## Pain Point

Most draft skills describe intent, but not a realistic before-and-after transformation.

## Why Now

Increased competition among skill repos means practical examples are now a gating factor for adoption.

## Evidence

- id: awesome-llm-apps
  evidence_type: directory
  source_url: https://github.com/topics/llm-apps
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Example-driven repos gain clearer contributor adoption than abstract lists.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 120
  verification_status: partial
- id: prompt-engineering
  evidence_type: community-signal
  source_url: https://github.com/topics/prompt-engineering
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Prompt communities emphasize before/after comparisons to reduce interpretation risk.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 180
  verification_status: partial
- id: github-agent-skills
  evidence_type: github-repo
  source_url: https://github.com/search?q=SKILL.md+before+after&type=Code
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Many skill repos use before/after patterns to reduce misinterpretation.
  signal_weight: weak
  confidence: low
  freshness_window_days: 180
  verification_status: partial

## Saturation Risk

Low. Many repos include examples, but few require before/after in a consistent card format.

## Differentiation

This topic is explicit about one example artifact and how to test it quickly.

## Starter Scope

- Input: one rough use case and one desired skill output.
- Output: one short before/after pair with assumptions.
- No full generator tooling in v0.1.

## Expected Output

- A minimal demo scenario.
- A predictable output template.
- A short check list for quality and missing data.

## Demo Input

```text
Rough idea: "Help me summarize long handoff notes and mark open risks."
```

## Launch Keywords

- before-after
- example-quality
- reproducible-output

## Quality Gate

- Includes both a before input and an expected after artifact.
- Keeps privacy-safe and realistic sample data.
- Specifies scope for one small example only.

## Do Not Build

- Do not create a general-purpose example generator runtime in v0.1.
- Do not make fake or synthetic claims without source context.
