# Verification Plan — agent-skill-radar

## Scope
Target repository: `/Users/alex/HighStarRepo/repos/agent-skill-radar`

## Required Evidence Before Final Verification
- `data/signal-sources.yaml` exists
- `data/topic-index.yaml` exists
- `topics/` contains at least 7 topic cards
- `starters/` contains at least 2 SKILL starter files
- `scripts/validate_radar.py` exists
- `tests/` and `reviews/topic-card-review-results.yaml` exist

## Verification Checklist

1. Validate radar schema and cross-file consistency
   - Run: `python3 scripts/validate_radar.py .`
   - Pass criteria:
     - command exits 0
     - all topic cards parse
     - every `source_id` in cards resolves to an entry in `data/signal-sources.yaml`
     - every v0.1 topic card includes `topics/*.md` with required frontmatter and heading order
     - `reviews/topic-card-review-results.yaml` required by validator is present if enforced

2. Run unit tests
   - Run: `python3 -m unittest discover -s tests`
   - Pass criteria:
     - command exits 0
     - no failures or errors in output

3. Run HighStar review
   - Run: `python3 /Users/alex/HighStarRepo/tools/highstar.py review .`
   - Pass criteria:
     - command exits 0
     - HighStar review has no policy or quality gate failures

4. Run launch-copy smoke check
   - Run: `python3 /Users/alex/HighStarRepo/tools/highstar.py launch-copy . .`
   - Pass criteria:
     - command exits 0
     - no obvious path/metadata copy blockages

5. Final publish gate (not part of local verification unless explicitly requested)
   - Use only if steps 1–4 pass:
     - `python3 /Users/alex/HighStarRepo/tools/highstar.py publish --owner alexzhu0 .`
     - review publish output and repo metadata before merge

## Acceptance Criteria Mapping
- Required command sequence: 1 → 2 → 3 → 4
- Any non-zero exit code in steps 1–4 is a hard gate stop.
- Verification is complete only when all acceptance items in the RALPLAN (README layout, 7 topic cards, 2 starters, strict card schema, evidence constraints, zero blocking findings) are true and consistent with command outputs.

## Integration Risks (Likely)
- `data/signal-sources.yaml` drift vs topic cards
  - Risk: stale or renamed source IDs break validator and weaken evidence freshness claims.
  - Control: enforce source-id resolution checks and periodic evidence refresh review.
- Topic cards and topic index mismatch
  - Risk: missing cards in index or index entries without files cause discoverability and review failures.
  - Control: assert bijection between `data/topic-index.yaml` and `topics/*.md` in validation/review.
- Starter path/reference breakage
  - Risk: frontmatter `starter_path` points to non-existent `starters/` SKILL.md, causing broken onboarding.
  - Control: strict checker for existing starter paths and required starter metadata (`name`, `description`).
- Validator vs HighStar policy gap
  - Risk: deterministic pass from script but fail in HighStar review due policy wording or anti-engagement rules.
  - Control: include policy check items (no spam/auto-engagement claims) in manual HighStar review before merge.
- Release-readiness mismatch
  - Risk: repo passes structural checks but missing human review signals (`blocking_findings`) or README/API section placement violates HighStar conventions.
  - Control: verify `reviews/topic-card-review-results.yaml` and README section ordering before final sign-off.
