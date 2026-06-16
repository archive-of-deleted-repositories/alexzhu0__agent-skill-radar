# Contributing

Contributions are expected to be concrete, small, and easy to review.

## Good contributions

- A new topic card with plain evidence notes.
- A clearer starter skill workflow.
- Better evidence wording without hype.
- Real-world examples and a matching expected output.

## Add a topic card

1. Copy an existing topic card as a template.
2. Keep frontmatter simple and complete.
3. Keep the 13 required headings in exact order:
   - `## One-Liner`
   - `## Target User`
   - `## Pain Point`
   - `## Why Now`
   - `## Evidence`
   - `## Saturation Risk`
   - `## Differentiation`
   - `## Starter Scope`
   - `## Expected Output`
   - `## Demo Input`
   - `## Launch Keywords`
   - `## Quality Gate`
   - `## Do Not Build`
4. Use at least two unique source IDs from the hot-skill source set.
5. Add one line to `data/topic-index.yaml`.
6. Add a pass result in `reviews/topic-card-review-results.yaml`.

## Add a starter

- Add one new `SKILL.md` under `starters/<topic>/SKILL.md`.
- Keep frontmatter short and explicit:
  - `name`
  - `description`
- Include fit, inputs, workflow, output shape, and validation.

## Safety and review checks

- Do not invent safety claims.
- Do not promise cross-runtime behavior you have not validated locally.
- Keep examples realistic and anonymized.
- Avoid encouraging secrets, credential bypasses, or automated account actions.

## Before you open a PR

- Keep changes limited to documentation scope.
- Include one reviewer-visible line item in the PR summary.
- Ensure each changed topic appears in the index and review results.
