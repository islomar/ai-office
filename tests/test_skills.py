import datetime as dt
import json
import re
import subprocess
from pathlib import Path

import pytest

from ai_office import skills

TODAY = dt.date(2026, 11, 15)


def write_skill(root: Path, name: str, description: str = "Does things.") -> None:
    folder = root / "skills" / name
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n")


def test_list_skills_reads_name_and_description(tmp_path: Path) -> None:
    write_skill(tmp_path, "ship", "Lint, commit\n  and push.")
    write_skill(tmp_path, "alpha")
    (tmp_path / "skills" / "README.md").write_text("# Skills\n")

    found = skills.list_skills(tmp_path)

    assert [(s.name, s.description) for s in found] == [("alpha", "Does things."), ("ship", "Lint, commit and push.")]


def test_skill_without_front_matter_uses_folder_name(tmp_path: Path) -> None:
    (tmp_path / "skills" / "bare").mkdir(parents=True)
    (tmp_path / "skills" / "bare" / "SKILL.md").write_text("# Bare\n")

    assert [(s.name, s.description) for s in skills.list_skills(tmp_path)] == [("bare", "")]


@pytest.mark.parametrize("folder", [".agents/skills/ship", ".claude/skills/ship"])
def test_installed_when_skill_folder_exists(tmp_path: Path, folder: str) -> None:
    (tmp_path / folder).mkdir(parents=True)

    assert skills.is_installed(tmp_path, "ship")


def test_installed_when_lock_file_lists_it(tmp_path: Path) -> None:
    (tmp_path / "skills-lock.json").write_text(json.dumps({"version": 2, "skills": {"ship": {}}}))

    assert skills.is_installed(tmp_path, "ship")
    assert not skills.is_installed(tmp_path, "other")


def test_not_installed_with_broken_lock_file(tmp_path: Path) -> None:
    (tmp_path / "skills-lock.json").write_text("{broken")

    assert not skills.is_installed(tmp_path, "ship")


def test_no_notice_when_pin_is_latest() -> None:
    times = {"created": "2020-01-01T00:00:00Z", "1.7.6": "2026-11-03T00:00:00Z"}

    assert skills.update_notice("1.7.6", times, TODAY) is None


def test_newer_release_younger_than_seven_days_is_not_proposed() -> None:
    times = {"1.7.6": "2026-11-03T00:00:00Z", "1.8.1": "2026-11-11T00:00:00Z"}

    notice = skills.update_notice("1.7.6", times, TODAY)

    assert "1.8.1" in notice and "Keeping 1.7.6" in notice
    assert "UPDATE AVAILABLE" not in notice


def test_newest_mature_release_is_proposed() -> None:
    times = {
        "1.7.6": "2026-11-03T00:00:00Z",
        "1.8.0": "2026-11-05T00:00:00Z",
        "1.8.1": "2026-11-08T00:00:00Z",
        "1.9.0": "2026-11-14T00:00:00Z",
    }

    notice = skills.update_notice("1.7.6", times, TODAY)

    assert notice.startswith("UPDATE AVAILABLE: skills CLI 1.8.1")
    assert "Bash(npx -y skills@1.8.1 *)" in notice


def test_versions_compare_numerically_and_prereleases_are_ignored() -> None:
    times = {"1.9.0": "2026-10-01T00:00:00Z", "1.10.0-beta.1": "2026-10-01T00:00:00Z", "1.10.0": "2026-10-02T00:00:00Z"}

    assert "skills CLI 1.10.0 " in skills.update_notice("1.9.0", times, TODAY)


def test_install_command_pins_the_cli_version() -> None:
    command = skills.install_command("ship", ("claude-code", "opencode"))

    assert command == [
        "npx", "-y", f"skills@{skills.SKILLS_CLI_PINNED}", "add", "islomar/ai-office",
        "--skill", "ship", "-a", "claude-code", "-a", "opencode", "-y",
    ]  # fmt: skip


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_workflow_template_uses_the_pinned_cli_and_no_other_version() -> None:
    template = (REPO_ROOT / skills.WORKFLOW_TEMPLATE).read_text()

    assert re.findall(r"skills@[\w.\-]+", template) == [f"skills@{skills.SKILLS_CLI_PINNED}"]


def test_workflow_template_pins_actions_to_full_commits() -> None:
    template = (REPO_ROOT / skills.WORKFLOW_TEMPLATE).read_text()
    uses = re.findall(r"uses:\s*(\S+)", template)

    assert uses and all(re.fullmatch(r"[\w\-]+/[\w\-]+@[0-9a-f]{40}", u) for u in uses)


def test_workflow_status_and_write(tmp_path: Path) -> None:
    assert skills.workflow_status(REPO_ROOT, tmp_path) == "missing"

    written = skills.write_workflow(REPO_ROOT, tmp_path)
    assert written == tmp_path / ".github/workflows/skills-update.yml"
    assert skills.workflow_status(REPO_ROOT, tmp_path) == "current"

    written.write_text(written.read_text().replace("skills@", "skills@0.0.0-"))
    assert skills.workflow_status(REPO_ROOT, tmp_path) == "outdated"


def test_allow_pull_requests_keeps_default_token_permissions() -> None:
    command = skills.allow_pull_requests_command("me/repo", {"default_workflow_permissions": "write"})

    assert command[-4:] == ["-f", "default_workflow_permissions=write", "-F", "can_approve_pull_request_reviews=true"]
    assert "repos/me/repo/actions/permissions/workflow" in command


def test_update_notice_names_every_place_that_holds_the_pin() -> None:
    notice = skills.update_notice("1.0.0", {"1.1.0": "2026-10-01T00:00:00Z"}, TODAY)

    assert "tools/ai_office/skills.py" in notice
    assert str(skills.WORKFLOW_TEMPLATE) in notice
    assert "~/.claude/settings.json" in notice


def test_permission_rule_is_found_in_settings(tmp_path: Path) -> None:
    settings = tmp_path / "settings.json"
    settings.write_text(json.dumps({"permissions": {"allow": [skills.permission_rule()]}}))

    assert skills.has_permission_rule(settings)
    assert not skills.has_permission_rule(settings, "0.0.1")
    assert not skills.has_permission_rule(tmp_path / "missing.json")


def test_git_commands_in_tests_ignore_the_commit_in_progress() -> None:
    env = subprocess.run(["env"], capture_output=True, text=True, check=True).stdout

    assert [line for line in env.splitlines() if line.startswith("GIT_")] == []


@pytest.fixture
def published_repo(tmp_path: Path) -> Path:
    remote, repo = tmp_path / "remote.git", tmp_path / "repo"

    def git(*args: str, cwd: Path = repo) -> None:
        # Skip the user's global hooks: they are slow and not under test.
        subprocess.run(["git", "-c", "core.hooksPath=/dev/null", *args], cwd=cwd, check=True, capture_output=True)

    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    subprocess.run(["git", "clone", "-q", str(remote), str(repo)], check=True, capture_output=True)
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test")
    write_skill(repo, "ship")
    git("add", ".")
    git("commit", "-q", "-m", "add ship")
    git("push", "-q", "origin", "HEAD:main")
    return repo


def test_published_skill_has_no_reason(published_repo: Path) -> None:
    assert skills.unpublished_reason(published_repo, "ship") is None


def test_uncommitted_change_is_reported(published_repo: Path) -> None:
    (published_repo / "skills" / "ship" / "SKILL.md").write_text("changed\n")

    assert skills.unpublished_reason(published_repo, "ship") == "skills/ship has uncommitted changes"


def test_unpushed_commit_is_reported(published_repo: Path) -> None:
    (published_repo / "skills" / "ship" / "SKILL.md").write_text("changed\n")
    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-qam", "change"], cwd=published_repo, check=True)

    assert skills.unpublished_reason(published_repo, "ship") == "skills/ship has commits that are not pushed to origin/main"


def test_never_committed_skill_is_reported(published_repo: Path) -> None:
    write_skill(published_repo, "draft")

    assert skills.unpublished_reason(published_repo, "draft") == "skills/draft has uncommitted changes"


@pytest.mark.parametrize(
    "stdout",
    [
        '{"created": "2016-10-06T18:56:01.340Z", "1.7.6": "2026-10-01T10:00:00.000Z"}',
        # npm 12 wraps the object in a list.
        '[{"created": "2016-10-06T18:56:01.340Z", "1.7.6": "2026-10-01T10:00:00.000Z"}]',
    ],
)
def test_release_times_read_both_npm_output_shapes(stdout: str) -> None:
    assert skills.parse_release_times(stdout) == {
        "created": "2016-10-06T18:56:01.340Z",
        "1.7.6": "2026-10-01T10:00:00.000Z",
    }


@pytest.mark.parametrize("stdout", ["[]", '["1.7.6"]', '"text"', "not json"])
def test_unexpected_npm_output_gives_no_release_times(stdout: str) -> None:
    assert skills.parse_release_times(stdout) is None
