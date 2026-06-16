#!/usr/bin/env python3
"""Validation script for the agent-skill-radar repository contract."""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


README_REQUIRED_SECTIONS = [
    "Why",
    "Install",
    "Quickstart",
    "Examples",
    "API",
    "FAQ",
    "Contributing",
    "License",
]

TOPIC_REQUIRED_SECTIONS = [
    "One-Liner",
    "Target User",
    "Pain Point",
    "Why Now",
    "Evidence",
    "Saturation Risk",
    "Differentiation",
    "Starter Scope",
    "Expected Output",
    "Demo Input",
    "Launch Keywords",
    "Quality Gate",
    "Do Not Build",
]

VOLATILE_SOURCE_TYPES = {
    "github-repo",
    "directory",
    "community-signal",
    "local-metric",
}

ROOT_REQUIRED_FILES = [
    "highstar.yaml",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "data/signal-sources.yaml",
    "data/topic-index.yaml",
    "reviews/topic-card-review-checklist.md",
    "reviews/topic-card-review-results.yaml",
    "releases/v0.1.0.md",
]


_keyval_re = re.compile(r"^([A-Za-z0-9_.-]+)\s*:\s*(.*)$")


def _strip_comment(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("#"):
        return ""
    return line


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value == "":
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    lower = value.lower()
    if lower in {"true", "yes", "on"}:
        return True
    if lower in {"false", "no", "off"}:
        return False
    if lower in {"null", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def _next_non_empty(lines: List[str], index: int) -> Tuple[int, str]:
    i = index
    while i < len(lines):
        line = _strip_comment(lines[i]).rstrip()
        if line.strip():
            return i, line
        i += 1
    return i, ""


def parse_yaml(text: str) -> Any:
    lines = text.splitlines()
    value, _ = _parse_yaml_block(lines, 0, 0)
    return value


def _parse_yaml_block(lines: List[str], start: int, base_indent: int) -> Tuple[Any, int]:
    i = start
    while True:
        i, raw = _next_non_empty(lines, i)
        if i >= len(lines):
            return None, i
        if _indent(raw) < base_indent:
            return None, i
        break

    first = _strip_comment(raw).strip()
    current_indent = _indent(raw)
    if current_indent != base_indent:
        # Should never happen if the caller computed child indentation correctly.
        base_indent = current_indent
    is_list = first.startswith("- ")

    if is_list:
        parsed: List[Any] = []
        while i < len(lines):
            i, raw = _next_non_empty(lines, i)
            if i >= len(lines):
                break
            if _indent(raw) < base_indent:
                break
            if _indent(raw) > base_indent:
                raise ValueError(f"Unexpected nested line at depth {i + 1}: {raw}")
            if not raw.lstrip().startswith("- "):
                break

            content = raw.strip()[2:].strip()
            next_i, _ = _next_non_empty(lines, i + 1)
            nested_indent = _indent(lines[next_i]) if next_i < len(lines) else base_indent
            nested_present = next_i < len(lines) and nested_indent > base_indent

            if content == "":
                if nested_indent <= base_indent:
                    raise ValueError(f"List item missing value at line {i + 1}")
                item, i = _parse_yaml_block(lines, i + 1, nested_indent)
                parsed.append(item)
                continue

            key_match = _keyval_re.match(content)
            if key_match:
                key = key_match.group(1)
                value_raw = key_match.group(2)
                item: Dict[str, Any] = {}
                if value_raw == "":
                    item[key] = None
                    if nested_present:
                        nested, i = _parse_yaml_block(lines, i + 1, nested_indent)
                        if isinstance(nested, dict):
                            item.update(nested)
                        else:
                            raise ValueError(f"Unexpected list item nested value at line {i + 1}")
                else:
                    item = {key: _parse_scalar(value_raw)}
                if nested_present:
                    nested, new_i = _parse_yaml_block(lines, i + 1, nested_indent)
                    if isinstance(nested, dict):
                        item.update(nested)
                    elif nested is not None:
                        raise ValueError(f"Unexpected list item nested value at line {i + 1}")
                    i = new_i
                else:
                    i += 1
            else:
                item = _parse_scalar(content)
                i += 1
            parsed.append(item)
        return parsed, i

    parsed_map: Dict[str, Any] = {}
    while i < len(lines):
        i, raw = _next_non_empty(lines, i)
        if i >= len(lines):
            break
        if _indent(raw) < base_indent:
            break
        if _indent(raw) > base_indent:
            # Nested block for previous key.
            break
        if raw.lstrip().startswith("- "):
            break
        key_match = _keyval_re.match(raw.strip())
        if not key_match:
            raise ValueError(f"Invalid YAML mapping entry at line: {raw}")
        key = key_match.group(1)
        value_raw = key_match.group(2)
        if value_raw == "":
            if i + 1 >= len(lines):
                parsed_map[key] = None
                i += 1
                continue
            next_i, _ = _next_non_empty(lines, i + 1)
            nested_indent = _indent(lines[next_i])
            if nested_indent <= base_indent:
                parsed_map[key] = None
                i += 1
            else:
                nested, i = _parse_yaml_block(lines, i + 1, nested_indent)
                parsed_map[key] = nested
        else:
            parsed_map[key] = _parse_scalar(value_raw)
            i += 1

    return parsed_map, i


def _parse_front_matter(markdown: str) -> Dict[str, Any]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("Missing frontmatter closing ---")
    return parse_yaml("\n".join(lines[1:end]))


def _extract_headings(markdown: str) -> List[str]:
    headings: List[str] = []
    in_frontmatter = False
    seen_frontmatter = False
    for line in markdown.splitlines():
        if line.strip() == "---":
            if not seen_frontmatter:
                seen_frontmatter = True
                in_frontmatter = True
                continue
            if in_frontmatter:
                in_frontmatter = False
                continue
        if in_frontmatter:
            continue
        match = re.match(r"^##\s+(.*)\s*$", line)
        if match:
            headings.append(match.group(1).strip())
    return headings


def _parse_utc(value: str) -> _dt.datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = _dt.datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError("Datetime missing timezone information")
    return dt.astimezone(_dt.timezone.utc)


def _collect_source_map(signal_sources: Any) -> Dict[str, Dict[str, Any]]:
    if isinstance(signal_sources, dict):
        if "sources" in signal_sources and isinstance(signal_sources["sources"], list):
            source_entries = signal_sources["sources"]
        else:
            raise ValueError("signal-sources.yaml missing top-level sources list")
    elif isinstance(signal_sources, list):
        source_entries = signal_sources
    else:
        raise ValueError("signal-sources.yaml root must be a list or sources key")

    source_map: Dict[str, Dict[str, Any]] = {}
    for entry in source_entries:
        if not isinstance(entry, dict):
            raise ValueError("signal source entry must be a mapping")
        source_id = entry.get("id")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError("every signal source requires a non-empty id")
        if source_id in source_map:
            raise ValueError(f"duplicate signal source id: {source_id}")
        source_map[source_id] = entry
    return source_map


def _read_yaml(path: Path) -> Any:
    return parse_yaml(path.read_text(encoding="utf-8"))


def _read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _get_v01_topics(topic_front: Dict[str, Any]) -> bool:
    status = topic_front.get("status")
    return isinstance(status, str) and status.startswith("v0.1")


def _check_readme(path: Path, errors: List[str]) -> None:
    text = _read_markdown(path)
    headings = _extract_headings(text)
    heading_set = {h.lower() for h in headings}

    for required in README_REQUIRED_SECTIONS:
        if required.lower() not in heading_set:
            errors.append(f"README missing required section: {required}")

    api_index = None
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip().lower() == "## api":
            api_index = idx
            break

    if api_index is None:
        errors.append("README missing API section")
        return

    before_api = "\n".join(lines[:api_index])
    table_found = bool(
        re.search(
            r"(?im)^\|\s*topic\s*\|.*\n\|[ \-\:\|]+\|",
            before_api,
        )
    )
    if not table_found:
        errors.append("README missing top topic table before API section")


def _topic_entries_from_index(topic_index: Any) -> List[Dict[str, Any]]:
    if isinstance(topic_index, dict):
        if "topics" not in topic_index or not isinstance(topic_index["topics"], list):
            raise ValueError("topic-index.yaml requires top-level topics list")
        entries = topic_index["topics"]
    elif isinstance(topic_index, list):
        entries = topic_index
    else:
        raise ValueError("topic-index.yaml root must be a list or topics key")

    if not all(isinstance(item, dict) for item in entries):
        raise ValueError("Each topic index item must be a mapping")
    return entries


def _topic_path(topic_repo_root: Path, topic_entry: Dict[str, Any]) -> Path:
    for key in ("file", "path", "topic_file"):
        value = topic_entry.get(key)
        if isinstance(value, str) and value:
            return topic_repo_root / value
    raise ValueError("topic index entry missing file/path/topic_file")


def _topic_name(topic_entry: Dict[str, Any], topic_meta: Dict[str, Any]) -> str:
    return (
        str(topic_entry.get("name"))
        if isinstance(topic_entry.get("name"), str)
        else str(topic_entry.get("id"))
        if isinstance(topic_entry.get("id"), str)
        else str(topic_meta.get("name", ""))
    )


def _display_path(repo: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo))
    except ValueError:
        return str(path)


def _is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _normalize_optional_path(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if isinstance(value, str):
        return value.strip() or None
    return None


def _normalize_source_ids(value: Any) -> List[str] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        return None
    return [str(v).strip() for v in value if str(v).strip()]


def _check_index_frontmatter_parity(
    repo: Path,
    topic_path: Path,
    entry: Dict[str, Any],
    frontmatter: Dict[str, Any],
    errors: List[str],
) -> None:
    topic_label = _display_path(repo, topic_path)
    entry_name = _topic_name(entry, frontmatter).strip()
    front_name = str(frontmatter.get("name", "")).strip()
    if entry_name and front_name and entry_name != front_name:
        errors.append(
            f"{topic_label}: data/topic-index.yaml name/id '{entry_name}' does not match frontmatter name '{front_name}'"
        )

    for key in ("status", "confidence", "verification_status"):
        if key in entry and entry.get(key) != frontmatter.get(key):
            errors.append(
                f"{topic_label}: data/topic-index.yaml {key} does not match frontmatter"
            )

    entry_sources = _normalize_source_ids(entry.get("source_ids"))
    front_sources = _normalize_source_ids(frontmatter.get("source_ids"))
    if (
        entry_sources is not None
        and front_sources is not None
        and set(entry_sources) != set(front_sources)
    ):
        errors.append(
            f"{topic_label}: data/topic-index.yaml source_ids do not match frontmatter"
        )

    if "starter_path" in entry:
        entry_starter = _normalize_optional_path(entry.get("starter_path"))
        front_starter = _normalize_optional_path(frontmatter.get("starter_path"))
        if entry_starter != front_starter:
            errors.append(
                f"{topic_label}: data/topic-index.yaml starter_path does not match frontmatter"
            )


def _check_topic_path(
    repo: Path,
    topics_root: Path,
    entry: Dict[str, Any],
    errors: List[str],
) -> Path | None:
    try:
        topic_path = _topic_path(repo, entry)
    except ValueError as exc:
        errors.append(f"Invalid topic index entry: {exc}")
        return None

    topic_file_value = next(
        (
            entry.get(key)
            for key in ("file", "path", "topic_file")
            if isinstance(entry.get(key), str) and entry.get(key)
        ),
        "",
    )
    topic_label = _topic_name(entry, {})
    if Path(topic_file_value).is_absolute():
        errors.append(
            f"data/topic-index.yaml topic path must be relative: {topic_file_value}"
        )
        return None
    if not _is_inside(topic_path, topics_root):
        errors.append(
            f"data/topic-index.yaml topic path must stay under topics/: {topic_label or topic_file_value}"
        )
        return None
    return topic_path


def _check_starter_path(
    repo: Path,
    topic_path: Path,
    starter_path: Any,
    errors: List[str],
) -> None:
    topic_label = _display_path(repo, topic_path)
    if starter_path in (None, ""):
        return
    if not isinstance(starter_path, str):
        errors.append(f"{topic_label}: starter_path must be a string or null")
        return

    starter_rel = starter_path.strip()
    starter = repo / starter_rel
    if Path(starter_rel).is_absolute():
        errors.append(f"{topic_label}: starter_path must be relative")
        return
    if not _is_inside(starter, repo / "starters"):
        errors.append(f"{topic_label}: starter_path must stay under starters/")
        return
    if starter.name != "SKILL.md":
        errors.append(f"{topic_label}: starter_path must point to a SKILL.md file")
        return
    if not starter.exists():
        errors.append(f"{topic_label}: starter_path does not exist: {starter_rel}")


def validate_repo(repo_dir: Path) -> List[str]:
    repo = repo_dir.resolve()
    errors: List[str] = []

    for rel in ROOT_REQUIRED_FILES:
        if not (repo / rel).exists():
            errors.append(f"Missing required file: {rel}")

    readme_path = repo / "README.md"
    if readme_path.exists():
        _check_readme(readme_path, errors)

    if errors:
        return errors

    signal_sources_path = repo / "data/signal-sources.yaml"
    topic_index_path = repo / "data/topic-index.yaml"
    try:
        signal_sources = _read_yaml(signal_sources_path)
        source_map = _collect_source_map(signal_sources)
    except Exception as exc:
        errors.append(f"Invalid signal source file: {exc}")
        return errors

    try:
        topic_index = _read_yaml(topic_index_path)
        topic_index_entries = _topic_entries_from_index(topic_index)
    except Exception as exc:
        errors.append(f"Invalid topic index file: {exc}")
        return errors

    topics_root = repo / "topics"
    topic_paths: List[Tuple[Path, str, str]] = []
    indexed_paths: Dict[Path, str] = {}
    v01_topic_names: List[str] = []
    for entry in topic_index_entries:
        topic_path = _check_topic_path(repo, topics_root, entry, errors)
        if topic_path is None:
            continue
        topic_label = _display_path(repo, topic_path)
        resolved_topic_path = topic_path.resolve()
        if resolved_topic_path in indexed_paths:
            errors.append(
                f"data/topic-index.yaml lists topic file more than once: {topic_label}"
            )
            continue
        indexed_paths[resolved_topic_path] = topic_label
        if not topic_path.exists():
            errors.append(f"Topic file missing: {topic_label}")
            continue
        if topic_path.suffix.lower() != ".md":
            errors.append(f"Topic file has unexpected extension: {topic_label}")
            continue
        topic_text = _read_markdown(topic_path)
        try:
            frontmatter = _parse_front_matter(topic_text)
        except ValueError as exc:
            errors.append(f"{topic_label}: {exc}")
            continue

        if not isinstance(frontmatter, dict):
            errors.append(f"{topic_label}: frontmatter is not a mapping")
            continue

        _check_index_frontmatter_parity(repo, topic_path, entry, frontmatter, errors)

        source_ids = frontmatter.get("source_ids")
        if not isinstance(source_ids, list):
            errors.append(
                f"{topic_label}: source_ids must be a YAML list, not {type(source_ids).__name__}"
            )
            continue

        source_ids_norm = [str(v).strip() for v in source_ids if str(v).strip()]
        if len(source_ids_norm) != len(set(source_ids_norm)):
            errors.append(f"{topic_label}: source_ids contains duplicates")
        if len(set(source_ids_norm)) < 2:
            errors.append(f"{topic_label}: expected at least two unique source_ids")

        front_name = str(frontmatter.get("name", "")).strip()
        if not front_name:
            errors.append(f"{topic_label}: missing name in frontmatter")
        starter_path = frontmatter.get("starter_path")
        _check_starter_path(repo, topic_path, starter_path, errors)

        headings = _extract_headings(topic_text)
        if [h.strip() for h in headings] != TOPIC_REQUIRED_SECTIONS:
            errors.append(f"{topic_label}: required H2 sections are missing or out of order")

        if source_ids_norm:
            source_weights = []
            for source_id in source_ids_norm:
                source = source_map.get(source_id)
                if source is None:
                    errors.append(
                        f"{topic_label}: source_id '{source_id}' not found in data/signal-sources.yaml"
                    )
                    continue

                evidence_type = source.get("evidence_type")
                source_url = source.get("source_url")
                signal_weight = source.get("signal_weight")
                if signal_weight in ("strong", "medium", "weak"):
                    source_weights.append(signal_weight)
                if evidence_type != "inference" and not source_url:
                    errors.append(
                        f"{topic_label}: non-inference source '{source_id}' missing source_url"
                    )

                if evidence_type in VOLATILE_SOURCE_TYPES:
                    collected_raw = source.get("collected_at") or source.get(
                        "observed_at_utc"
                    )
                    if collected_raw is None:
                        errors.append(
                            f"{topic_label}: volatile source '{source_id}' missing collected_at"
                        )
                    else:
                        try:
                            collected = _parse_utc(str(collected_raw))
                        except Exception:
                            errors.append(
                                f"{topic_label}: volatile source '{source_id}' has invalid collected_at"
                            )
                        else:
                            window_days = source.get("freshness_window_days")
                            try:
                                window_days_int = int(window_days)
                            except (TypeError, ValueError):
                                errors.append(
                                    f"{topic_label}: volatile source '{source_id}' missing freshness_window_days"
                                )
                            else:
                                now = _dt.datetime.now(_dt.timezone.utc)
                                age = now - collected
                                if age.days > window_days_int:
                                    errors.append(
                                        f"{topic_label}: volatile source '{source_id}' is stale"
                                    )

            if not any(w in {"strong", "medium"} for w in source_weights):
                errors.append(
                    f"{topic_label}: at least one source_id must be strong or medium"
                )

        if _get_v01_topics(frontmatter):
            v01_topic_names.append(front_name or str(topic_path.name))

        topic_paths.append((topic_path, front_name, topic_path.name))

    if len(topic_paths) < 7:
        errors.append(f"Expected at least 7 topic cards, found {len(topic_paths)}")

    if topics_root.exists():
        actual_topic_paths = {path.resolve() for path in topics_root.glob("*.md")}
        for path in sorted(actual_topic_paths - set(indexed_paths)):
            errors.append(
                f"Topic file not listed in data/topic-index.yaml: {_display_path(repo, path)}"
            )

    for rel_entry in ("starters",):
        starters = (repo / rel_entry).glob("*/SKILL.md")
        starter_cards = list(starters)
        if len(starter_cards) < 2:
            errors.append("Expected at least 2 starter SKILL.md files")
        for path in starter_cards:
            try:
                fm = _parse_front_matter(_read_markdown(path))
            except ValueError as exc:
                errors.append(f"{path}: invalid frontmatter ({exc})")
                continue
            if not isinstance(fm, dict):
                errors.append(f"{path}: frontmatter is not a mapping")
                continue
            if not fm.get("name"):
                errors.append(f"{path}: missing name")
            if not fm.get("description"):
                errors.append(f"{path}: missing description")

    try:
        review_path = repo / "reviews/topic-card-review-results.yaml"
        review = _read_yaml(review_path)
        if not isinstance(review, dict):
            raise ValueError("review results must be a mapping")
        blocking = review.get("blocking_findings")
        if str(blocking) != "0":
            errors.append("reviews/topic-card-review-results.yaml: blocking_findings must be 0")
        cards = review.get("cards")
        if not isinstance(cards, dict):
            raise ValueError("review results cards must be a mapping")
        for topic_name in v01_topic_names:
            card = cards.get(topic_name)
            if card != "pass":
                errors.append(
                    f"reviews/topic-card-review-results.yaml: topic {topic_name} is not pass"
                )
    except Exception as exc:
        errors.append(f"Invalid review results file: {exc}")

    return errors


def validate(repo_dir: str) -> int:
    root = Path(repo_dir)
    if not root.exists():
        print(f"ERROR: directory not found: {root}", file=sys.stderr)
        return 2
    errors = validate_repo(root)
    if not errors:
        print("Radar contract validation passed.")
        return 0
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)
    return 1


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    args = parser.parse_args(list(argv) if argv is not None else None)
    return validate(args.repo)


if __name__ == "__main__":
    sys.exit(main())
