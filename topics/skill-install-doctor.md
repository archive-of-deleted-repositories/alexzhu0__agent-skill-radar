---
name: skill-install-doctor
status: v0.1
confidence: medium
verification_status: partial
updated_at_utc: 2026-06-16T14:25:28Z
source_ids:
  - anthropic-skills
  - github-agent-skills
  - mcp-ecosystem
starter_path: null
---

## One-Liner

Diagnose why a skill is not discovered or invoked by a local agent runtime and list likely causes.

## Target User

Developers trying to run skills locally and seeing no activation, wrong triggers, or silent failures.

## Pain Point

Most failures are environment setup, location, and permission confusion, not the skill content itself.

## Why Now

As installations spread across tools and OS shells, install and invocation mismatches are common.

## Evidence

- id: anthropic-skills
  evidence_type: official-doc
  source_url: https://docs.anthropic.com/
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Tool ecosystems document local instruction discovery and runtime paths with recurring troubleshooting pain points.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 365
  verification_status: speculative
- id: github-agent-skills
  evidence_type: community-signal
  source_url: https://github.com/search?q=agent+skill+not+found&type=Issues
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: Community issue threads frequently report discovery and activation problems.
  signal_weight: medium
  confidence: medium
  freshness_window_days: 180
  verification_status: partial
- id: mcp-ecosystem
  evidence_type: directory
  source_url: https://github.com/topics/mcp
  observed_at_utc: 2026-06-16T12:00:00Z
  signal_summary: MCP and local tooling configurations are often sensitive to file-path and install ordering.
  signal_weight: weak
  confidence: low
  freshness_window_days: 120
  verification_status: partial

## Saturation Risk

Low. The symptom pattern is common, but few repositories package a focused first-pass diagnostic flow.

## Differentiation

This card separates content quality checks from runtime discovery checks and keeps remediation steps explicit.

## Starter Scope

- Input: one symptom set (expected skill, observed behavior, environment).
- Output: ranked hypothesis list and one recovery checklist.
- No runtime-level introspection code in v0.1.

## Expected Output

- Why the skill is not found/triggered.
- Top 5 likely fixes in priority order.
- A safe fallback workflow.

## Demo Input

```text
Symptom:
- Skill file exists.
- Skill placed at runtime path.
- Trigger phrase did not fire on exact input.
```

## Launch Keywords

- skill-discovery
- runtime-doctor
- install-check

## Quality Gate

- Distinguishes local path/permission issues from spec quality issues.
- Avoids unsafe remediation steps.
- Provides a practical next check for the operator.

## Do Not Build

- Do not promise compatibility checks across runtimes not tested.
- Do not add invasive scripts that change system state.
