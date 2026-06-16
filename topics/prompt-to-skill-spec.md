---
name: prompt-to-skill-spec
status: v0.1
confidence: high
verification_status: partial
updated_at_utc: 2026-06-16T14:25:28Z
source_ids:
  - anthropic-skills
  - github-agent-skills
  - awesome-llm-apps
starter_path: starters/prompt-to-skill-spec/SKILL.md
---

## One-Liner

Turn instruction text or prompts into a structured skill specification with clear scope and output contracts.

## Target User

People writing prompt-heavy systems who need repeatable onboarding, ops, and support workflows.

## Pain Point

Good prompts are often ambiguous and do not encode expected inputs, outputs, and failure behavior.

## Why Now

Teams are sharing more prompt packs, but quality drops when every prompt is unique and unscored.

## Evidence

- id: anthropic-skills
  evidence_type: official-doc
  source_url: https://docs.anthropic.com/
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Tool ecosystems expose instruction-driven workflows where formal specs improve reuse.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 365
  verification_status: speculative
- id: github-agent-skills
  evidence_type: github-repo
  source_url: https://github.com/search?q=SKILL.md+agent+prompt&type=Code
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: GitHub contains active prompt-to-spec style repos with repeated conversion patterns.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 180
  verification_status: partial
- id: awesome-llm-apps
  evidence_type: directory
  source_url: https://github.com/topics/llm
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Large LLM app lists continue to collect tooling for prompts and workflows.
  signal_weight: weak
  confidence: low
  freshness_window_days: 90
  verification_status: partial

## Saturation Risk

Medium. Many repos offer prompt templates, but few enforce an explicit skill-spec boundary between prompt and workflow artifacts.

## Differentiation

This card focuses on turning prompts into stable skill inputs, with explicit validation and missing-data handling.

## Starter Scope

- Input: one prompt or instruction block.
- Output: one conversion spec with sections for fit, workflow, and validation.
- No broad LLM prompt refactoring or architecture rewrite.

## Expected Output

- Clear `SKILL.md` with input assumptions.
- Output contract and success criteria.
- Known gaps and testable edge cases.

## Demo Input

```text
Prompt text:
"For each new bug report, create a triage summary and list severity and missing data."
```

## Launch Keywords

- prompt-normalization
- skill-specification
- execution-boundaries

## Quality Gate

- Source IDs are present in list form and are unique.
- Evidence includes at least one concrete source URL.
- Spec keeps assumptions and missing evidence separate.
- Output section is directly copy-pasteable.

## Do Not Build

- Do not auto-edit prompt quality with hidden behavior.
- Do not promise one-size-fits-all LLM tuning advice.
