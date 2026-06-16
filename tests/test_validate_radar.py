from __future__ import annotations

import datetime as dt
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_radar.py"
TOPIC_HEADERS = """## One-Liner
## Target User
## Pain Point
## Why Now
## Evidence
## Saturation Risk
## Differentiation
## Starter Scope
## Expected Output
## Demo Input
## Launch Keywords
## Quality Gate
## Do Not Build
"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fresh_collect(days: int = 1) -> str:
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ValidateRadarTests(unittest.TestCase):
    def run_validator(self, repo: Path, expect_success: bool = True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(repo)],
            capture_output=True,
            text=True,
            check=False,
        )
        if expect_success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def build_common_files(self, repo: Path) -> None:
        write_text(repo / "README.md", "\n".join([
            "# Agent Skill Radar",
            "",
            "## Why",
            "## Install",
            "## Quickstart",
            "",
            "| Topic | User | Pain | Evidence Status | Saturation | Starter |",
            "| --- | --- | --- | --- | --- | --- |",
            "| workflow-to-skill-converter | Skill builders | Topic churn | partial | medium | starter |",
            "",
            "## Examples",
            "",
            "## API",
            "## FAQ",
            "## Contributing",
            "## License",
        ]))
        write_text(repo / "LICENSE", "license")
        write_text(repo / "CONTRIBUTING.md", "contributing")
        write_text(repo / "SECURITY.md", "security")
        write_text(repo / "CODE_OF_CONDUCT.md", "code of conduct")
        write_text(repo / "releases/v0.1.0.md", "release")
        write_text(repo / "reviews/topic-card-review-checklist.md", "checklist")
        write_text(repo / "highstar.yaml", "name: agent-skill-radar\n")

    def build_signal_sources(self, repo: Path, fresh_source: bool = True, with_url: bool = True) -> None:
        fresh = fresh_collect(1 if fresh_source else 90)
        write_text(
            repo / "data/signal-sources.yaml",
            "\n".join(
                [
                    "sources:",
                    "  - id: source-official",
                    "    evidence_type: official-doc",
                    *( ["    source_url: https://docs.example.com/openai"] if with_url else [] ),
                    "    signal_summary: official docs",
                    "    signal_weight: strong",
                    "    confidence: high",
                    "    freshness_window_days: 7",
                    f"    collected_at: {fresh}",
                    "  - id: source-inference",
                    "    evidence_type: inference",
                    "    signal_summary: inferred demand",
                    "    signal_weight: medium",
                    "    confidence: medium",
                    "    freshness_window_days: 7",
                    f"    collected_at: {fresh}",
                ]
            ),
        )

    def build_topic(
        self,
        repo: Path,
        name: str,
        source_ids_line: str = "  - source-official\n  - source-inference",
        starter_path: str | None = None,
    ) -> None:
        starter_line = f"starter_path: {starter_path}" if starter_path else "starter_path: null"
        write_text(
            repo / "topics" / f"{name}.md",
            "\n".join(
                [
                    "---",
                    f"name: {name}",
                    "status: v0.1",
                    "confidence: high",
                    "verification_status: partial",
                    f"updated_at_utc: {now_utc()}",
                    "source_ids:",
                    source_ids_line,
                    starter_line,
                    "---",
                    TOPIC_HEADERS,
                ]
            ),
        )

    def build_starter(self, repo: Path, name: str) -> None:
        write_text(
            repo / "starters" / name / "SKILL.md",
            "\n".join(
                [
                    "---",
                    "name: starter",
                    "description: starter description",
                    "---",
                    "body",
                ]
            ),
        )

    def build_review_results(self, repo: Path, names) -> None:
        cards = "\n".join([f"  {name}: pass" for name in names])
        write_text(
            repo / "reviews/topic-card-review-results.yaml",
            "\n".join(
                [
                    "reviewed_at_utc: " + now_utc(),
                    "reviewer: local",
                    "blocking_findings: 0",
                    "cards:",
                    cards,
                ]
            ),
        )

    def build_topic_index(self, repo: Path, names) -> None:
        lines = ["topics:"]
        for name in names:
            starter_path = (
                f"starters/{name}/SKILL.md"
                if name.endswith("-0") or name.endswith("-1")
                else "null"
            )
            lines.append(f"  - name: {name}")
            lines.append(f"    path: topics/{name}.md")
            lines.append("    status: v0.1")
            lines.append("    confidence: high")
            lines.append("    verification_status: partial")
            lines.append("    source_ids:")
            lines.append("      - source-official")
            lines.append("      - source-inference")
            lines.append(f"    starter_path: {starter_path}")
        write_text(repo / "data/topic-index.yaml", "\n".join(lines))

    def build_valid_repo(self, fresh: bool = True, source_url: bool = True, topic_count: int = 7):
        repo = Path(tempfile.mkdtemp(prefix="radar-valid-"))
        self.build_common_files(repo)
        self.build_signal_sources(repo, fresh_source=fresh, with_url=source_url)
        names = [f"topic-{idx}" for idx in range(topic_count)]
        for name in names:
            if name.endswith("-0") or name.endswith("-1"):
                self.build_topic(repo, name, starter_path=f"starters/{name}/SKILL.md")
                self.build_starter(repo, name)
            else:
                self.build_topic(repo, name)
        self.build_topic_index(repo, names)
        self.build_review_results(repo, names)
        return repo, names

    def test_validator_passes_on_good_fixtures(self):
        repo, names = self.build_valid_repo()
        self.build_topic(
            repo,
            names[0],
            "  - source-official\n  - source-inference",
            starter_path=f"starters/{names[0]}/SKILL.md",
        )
        self.build_review_results(repo, names)
        result = self.run_validator(repo)
        self.assertIn("Radar contract validation passed.", result.stdout)

    def test_validator_fails_when_under_min_topic_count(self):
        repo, _ = self.build_valid_repo(topic_count=6)
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("Expected at least 7 topic cards", result.stderr)

    def test_validator_fails_when_source_ids_is_not_list(self):
        repo, names = self.build_valid_repo()
        self.build_topic(repo, names[0], "source_ids: source-official, source-inference")
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("source_ids must be a YAML list", result.stderr)

    def test_validator_fails_without_non_inference_source_url(self):
        repo, _ = self.build_valid_repo(source_url=False)
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("non-inference source 'source-official' missing source_url", result.stderr)

    def test_validator_fails_when_volatile_source_is_stale(self):
        repo, _ = self.build_valid_repo(fresh=False)
        write_text(
            repo / "data/signal-sources.yaml",
            "\n".join(
                [
                    "sources:",
                    "  - id: source-official",
                    "    evidence_type: local-metric",
                    "    source_url: https://docs.example.com/openai",
                    "    signal_summary: official docs",
                    "    signal_weight: strong",
                    "    confidence: high",
                    "    freshness_window_days: 7",
                    f"    collected_at: {fresh_collect(90)}",
                    "  - id: source-inference",
                    "    evidence_type: inference",
                    "    signal_summary: inferred demand",
                    "    signal_weight: medium",
                    "    confidence: medium",
                    "    freshness_window_days: 7",
                    f"    collected_at: {fresh_collect(90)}",
                ]
            ),
        )
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("is stale", result.stderr)

    def test_validator_fails_with_review_blocking_findings(self):
        repo, names = self.build_valid_repo()
        self.build_review_results(repo, names)
        # replace review to introduce blocking finding
        write_text(
            repo / "reviews/topic-card-review-results.yaml",
            "\n".join(
                [
                    "reviewed_at_utc: " + now_utc(),
                    "reviewer: local",
                    "blocking_findings: 2",
                    "cards:",
                    *(f"  {name}: pass" for name in names),
                ]
            ),
        )
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("blocking_findings must be 0", result.stderr)

    def test_validator_fails_when_readme_has_missing_top_table_before_api(self):
        repo, names = self.build_valid_repo()
        write_text(
            repo / "README.md",
            "\n".join(
                [
                    "# Agent Skill Radar",
                    "## Why",
                    "## Install",
                    "## Quickstart",
                    "## Examples",
                    "## API",
                    "## FAQ",
                    "## Contributing",
                    "## License",
                ]
            ),
        )
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("top topic table before API section", result.stderr)

    def test_validator_fails_when_topic_index_path_leaves_topics(self):
        repo, names = self.build_valid_repo()
        lines = ["topics:"]
        for idx, name in enumerate(names):
            lines.append(f"  - name: {name}")
            if idx == 0:
                lines.append("    path: ../outside.md")
            else:
                lines.append(f"    path: topics/{name}.md")
            lines.append("    status: v0.1")
            lines.append("    confidence: high")
            lines.append("    verification_status: partial")
            lines.append("    source_ids:")
            lines.append("      - source-official")
            lines.append("      - source-inference")
            lines.append("    starter_path: null")
        write_text(repo / "data/topic-index.yaml", "\n".join(lines))
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("topic path must stay under topics/", result.stderr)

    def test_validator_fails_when_starter_path_is_missing(self):
        repo, names = self.build_valid_repo()
        self.build_topic(
            repo,
            names[0],
            starter_path="starters/missing/SKILL.md",
        )
        self.build_review_results(repo, names)
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("starter_path does not exist", result.stderr)

    def test_validator_fails_when_starter_path_leaves_starters(self):
        repo, names = self.build_valid_repo()
        self.build_topic(
            repo,
            names[0],
            starter_path="topics/topic-0.md",
        )
        self.build_review_results(repo, names)
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("starter_path must stay under starters/", result.stderr)

    def test_validator_fails_when_topic_index_metadata_drifts(self):
        repo, names = self.build_valid_repo()
        lines = ["topics:"]
        for idx, name in enumerate(names):
            lines.append(f"  - name: {name}")
            lines.append(f"    path: topics/{name}.md")
            lines.append("    status: draft" if idx == 0 else "    status: v0.1")
            lines.append("    confidence: high")
            lines.append("    verification_status: partial")
            lines.append("    source_ids:")
            lines.append("      - source-official")
            lines.append("      - source-inference")
            lines.append("    starter_path: null")
        write_text(repo / "data/topic-index.yaml", "\n".join(lines))
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("status does not match frontmatter", result.stderr)

    def test_validator_fails_when_topic_file_is_not_indexed(self):
        repo, _ = self.build_valid_repo()
        self.build_topic(repo, "unlisted-topic")
        self.build_review_results(repo, [f"topic-{idx}" for idx in range(7)])
        result = self.run_validator(repo, expect_success=False)
        self.assertIn("Topic file not listed in data/topic-index.yaml", result.stderr)


if __name__ == "__main__":
    unittest.main()
