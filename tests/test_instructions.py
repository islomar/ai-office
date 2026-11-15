import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INSTRUCTIONS = REPO_ROOT / "instructions"
EXPECTED_LINKS = {
    ".claude/CLAUDE.md": "CLAUDE.md",
    ".claude/AGENTS.md": "AGENTS.md",
    ".claude/RTK.md": "RTK.md",
    ".codex/AGENTS.md": "AGENTS.md",
    ".config/opencode/AGENTS.md": "AGENTS.md",
    ".pi/agent/AGENTS.md": "AGENTS.md",
    ".copilot/copilot-instructions.md": "AGENTS.md",
    ".gemini/GEMINI.md": "AGENTS.md",
}


def link_instructions(home: Path) -> str:
    result = subprocess.run(
        ["make", "-s", "-C", str(REPO_ROOT), "link-instructions", f"HOME={home}"],
        capture_output=True, text=True, check=True,
    )  # fmt: skip
    return result.stdout


def test_files_read_by_agents_without_imports_have_no_import_lines() -> None:
    # Codex, OpenCode and Pi pass an "@file" line to the model as plain text.
    for name in ("AGENTS.md", "RTK.md"):
        lines = (INSTRUCTIONS / name).read_text().splitlines()
        assert [line for line in lines if line.startswith("@")] == [], name


def test_claude_entry_point_imports_existing_files_only() -> None:
    imports = [line[1:] for line in (INSTRUCTIONS / "CLAUDE.md").read_text().splitlines() if line.startswith("@")]

    assert imports == ["AGENTS.md", "RTK.md"]
    assert all((INSTRUCTIONS / name).is_file() for name in imports)


def test_link_instructions_links_every_agent(tmp_path: Path) -> None:
    link_instructions(tmp_path)

    for target, source in EXPECTED_LINKS.items():
        link = tmp_path / target
        assert link.is_symlink(), target
        assert link.resolve() == INSTRUCTIONS / source, target


def test_link_instructions_backs_up_a_regular_file_and_is_repeatable(tmp_path: Path) -> None:
    old = tmp_path / ".codex" / "AGENTS.md"
    old.parent.mkdir(parents=True)
    old.write_text("old rules\n")

    first = link_instructions(tmp_path)
    second = link_instructions(tmp_path)

    backups = list(old.parent.glob("AGENTS.md.bak-*"))
    assert [b.read_text() for b in backups] == ["old rules\n"]
    assert "backed up" in first and "backed up" not in second
    assert old.resolve() == INSTRUCTIONS / "AGENTS.md"
