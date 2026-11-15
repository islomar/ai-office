import datetime as dt
from pathlib import Path

import pytest

from ai_office import records


@pytest.fixture
def root(tmp_path: Path) -> Path:
    for spec in records.KINDS.values():
        (tmp_path / spec["folder"]).mkdir()
    return tmp_path


@pytest.mark.parametrize("kind", sorted(records.KINDS))
def test_created_record_passes_the_check(root: Path, kind: str) -> None:
    records.create(root, kind, "Try the dial", today=dt.date(2026, 11, 15))

    assert records.check(root) == []


def test_created_task_has_id_slug_and_initial_status(root: Path) -> None:
    path = records.create(root, "task", "Move my skills here!", today=dt.date(2026, 11, 15))

    meta = records.read_front_matter(path)
    assert meta["status"] == "open"
    assert meta["created"] == dt.date(2026, 11, 15)
    assert records.ID_PATTERN.match(meta["id"])
    assert path.name == f"{meta['id']}-move-my-skills-here.md"


def test_long_title_stays_on_one_line_and_slug_ends_on_a_word(root: Path) -> None:
    title = "Keep the workspace in one public repository with skills installable one by one"
    path = records.create(root, "decision", title, today=dt.date(2026, 11, 15))

    assert f"title: {title}\n" in path.read_text()
    assert "date: 2026-11-15\n" in path.read_text()
    assert path.name.endswith("-keep-the-workspace-in-one-public-repository-with-skills.md")


def test_two_records_get_different_ids(root: Path) -> None:
    first = records.create(root, "decision", "Same title")
    second = records.create(root, "decision", "Same title")

    assert first != second


def test_missing_front_matter_is_reported(root: Path) -> None:
    (root / "tasks" / "T-abcdef-no-meta.md").write_text("# No meta\n")

    assert [p.message for p in records.check(root)] == ["missing YAML front matter"]


def test_readme_files_are_not_records(root: Path) -> None:
    (root / "tasks" / "README.md").write_text("# Tasks\n")

    assert records.check(root) == []


def test_unknown_status_and_missing_field_are_reported(root: Path) -> None:
    (root / "tasks" / "T-abcdef-x.md").write_text("---\nid: T-abcdef\ntitle: X\nstatus: waiting\n---\n")

    messages = [p.message for p in records.check(root)]
    assert "missing field 'created'" in messages
    assert any(m.startswith("status 'waiting'") for m in messages)


def test_wrong_prefix_and_file_name_are_reported(root: Path) -> None:
    (root / "decisions" / "other-name.md").write_text(
        "---\nid: T-abcdef\ntitle: X\nstatus: accepted\ndate: 2026-11-15\n---\n"
    )

    messages = [p.message for p in records.check(root)]
    assert "id 'T-abcdef' must start with 'DR-'" in messages
    assert "file name must start with 'T-abcdef-'" in messages


def test_malformed_id_is_reported(root: Path) -> None:
    (root / "knowledge" / "K-12-x.md").write_text("---\nid: K-12\ntitle: X\nupdated: 2026-11-15\n---\n")

    assert "id 'K-12' must be <prefix>-<6 hex chars>" in [p.message for p in records.check(root)]


def test_duplicate_ids_are_reported(root: Path) -> None:
    body = "---\nid: K-abcdef\ntitle: X\nupdated: 2026-11-15\n---\n"
    (root / "knowledge" / "K-abcdef-a.md").write_text(body)
    (root / "knowledge" / "K-abcdef-b.md").write_text(body)

    messages = [p.message for p in records.check(root)]
    assert len(messages) == 1
    assert messages[0].startswith("duplicate id 'K-abcdef'")


def test_pointer_to_private_memory_is_reported(root: Path) -> None:
    (root / "AGENTS.md").write_text("Read ~/.claude/projects/-home-me/memory/MEMORY.md first.\n")

    problems = records.check(root)
    assert len(problems) == 1
    assert "per-user harness memory" in problems[0].message


def test_private_memory_check_skips_tool_sources(root: Path) -> None:
    (root / "tools").mkdir()
    (root / "tools" / "notes.md").write_text("pattern: .claude/projects/x/memory\n")

    assert records.check(root) == []
