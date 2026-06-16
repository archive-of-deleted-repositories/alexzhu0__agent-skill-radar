---
name: workflow-to-skill-converter
description: Use this when a stable workflow exists and should become a triggerable `SKILL.md`.
---

# Workflow To Skill Converter

## Purpose

Convert one clear workflow into a compact, reusable `SKILL.md` with trigger, inputs, and output shape.

## Fit

- Use when a workflow happens repeatedly and is currently only in chat notes or docs.
- Do not use when the request is one-off advice with no repeat value.

## Inputs

- A stable workflow or playbook.
- Trigger phrase, scope boundaries, and expected outcome.
- Examples of failure cases or missing details.

## Workflow

1. Capture the core objective in one sentence.
2. List required inputs and optional inputs.
3. Define trigger phrase and anti-trigger conditions.
4. Write required output sections from this repo's card style.
5. Add a short missing-data and validation section.

## Output

Produce:

- `SKILL.md` with frontmatter fields: `name`, `description`.
- `Purpose`, `Fit`, `Inputs`, `Workflow`, `Output`, and `Validation`.
- Clear do-not-use boundaries.

## Validation

- Output is short enough to paste into an agent instruction file.
- Scope is one workflow, not a full platform migration.
- At least one concrete missing-data item is included.
