---
name: skill-market-map
status: v0.1
confidence: medium
verification_status: partial
updated_at_utc: 2026-06-16T14:25:28Z
source_ids:
  - github-agent-skills
  - mcp-ecosystem
  - llmops-cost
  - agent-evals
starter_path: null
---

## One-Liner

Build a practical map of crowded vs under-served Agent Skill categories with clear saturation notes.

## Target User

Builders deciding next skill investments and PMs validating topic selection.

## Pain Point

Market heat is often measured by star counts only, which hides execution quality and demand shape.

## Why Now

The ecosystem has enough overlap that topic choice now needs explicit saturation and utility checks.

## Evidence

- id: github-agent-skills
  evidence_type: github-repo
  source_url: https://github.com/search?q=agent+skills+topic&type=Repositories
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Repositories cluster around a few popular automation and productivity themes.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 180
  verification_status: partial
- id: mcp-ecosystem
  evidence_type: directory
  source_url: https://github.com/topics/mcp
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: MCP and model tooling trends influence where skills remain useful and where they saturate.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 120
  verification_status: partial
- id: llmops-cost
  evidence_type: local-metric
  source_url: https://github.com/topics/llmops
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Cost pressure shifts adoption toward smaller, high-reuse skills with clear output predictability.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 60
  verification_status: speculative
- id: agent-evals
  evidence_type: directory
  source_url: https://github.com/topics/llm-evaluation
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Topics with measurable outputs are easier to evaluate and publish.
  signal_weight: weak
  confidence: low
  freshness_window_days: 180
  verification_status: partial

## Saturation Risk

High. A few popular themes are crowded; under-served topics need explicit constraints and evidence boundaries.

## Differentiation

This card focuses on practical selection guidance: where to build and what to skip next.

## Starter Scope

- Input: category list and recent evidence links.
- Output: at most 5 map entries.
- No full scoring engine in v0.1.

## Expected Output

- A ranked topic shortlist.
- Saturation notes with evidence-backed reasons.
- A one-line "do not build" callout per category.

## Demo Input

```text
Candidate categories:
- code review assistant
- release summary generator
- context summarizer
- cost-aware routing helper
```

## Launch Keywords

- saturation-analysis
- topic-mapping
- builder-prioritization

## Quality Gate

- Evidence sources are mixed and not all from one platform.
- Saturation judgments include uncertainty.
- Output stays concise enough to support next-week execution.

## Do Not Build

- Do not confuse follower metrics with practical adoption quality.
- Do not promise a full market model without sustained longitudinal data.
