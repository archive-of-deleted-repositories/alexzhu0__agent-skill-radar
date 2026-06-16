# Example: Starter SKILL Before and After

## Input (Before)

```text
Could you make this repetitive workflow into something I can paste into my agent:
1) collect three reports
2) merge top risks
3) make owner assignments
4) list risks I still need to confirm
```

## Output (After)

Use `starters/workflow-to-skill-converter/SKILL.md`:

```markdown
---
name: weekly-risk-digest
description: Use this to turn weekly risk reports into a compact owner-backed digest.
---

## Purpose

Convert report-style input into one repeatable weekly risk output.
...
```

Then fill only the sections needed for this workflow.
