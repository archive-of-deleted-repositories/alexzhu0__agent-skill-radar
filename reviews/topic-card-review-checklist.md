# Topic Card Review Checklist

Use this checklist before adding any card to `v0.1` index.

## 1) Evidence

- `source_ids` has at least 2 unique entries.
- At least one source has `medium` or `strong` signal weight.
- `source_url` exists for non-inference evidence.

## 2) Quality

- All 13 required headings are present and in order.
- `One-Liner` is one short sentence.
- `Do Not Build` includes at least one explicit boundary.

## 3) Saturation and differentiation

- Saturation risk is realistic and not overconfident.
- The card does not duplicate existing public skill collections.

## 4) Starter and output fit

- `Starter Scope` is small enough for one contributor.
- `Expected Output` is concrete and short.
- `Demo Input` is realistic but anonymized.

## 5) Reviewer result

- If any item fails, set `blocking_findings` above 0 in results file.
- For v0.1, every card must be `pass`.
