---
name: prompt-to-skill-spec
description: Use this to convert prompts, playbook text, or policy text into a structured `SKILL.md` specification.
---

# Prompt To Skill Spec

## Purpose

Convert prompt-style instructions into a structured skill spec with clear fit and validation.

## Fit

- Use when a team prompt has repeated structure but no stable reuse format.
- Do not use for one-off drafting tasks or raw creative writing requests.

## Inputs

- Source prompt text.
- Intended user and context.
- Known success criteria and hard constraints.

## Workflow

1. Extract purpose and non-goals.
2. Define explicit required inputs and optional inputs.
3. Define trigger phrase and boundaries.
4. Add failure handling and missing data.
5. Write output shape with expected sections and validation points.

## Output

Produce:

- `SKILL.md` with frontmatter fields: `name`, `description`.
- `Purpose`, `Fit`, `Inputs`, `Workflow`, `Output`, `Validation`.
- Sections that separate facts from assumptions.

## Validation

- Assumptions are labeled, not hidden.
- Output is deterministic enough for reuse.
- Safety and policy guardrails are preserved.
