"""List the skills of this repository and plan their installation in other repositories.

Installation uses the skills CLI (https://github.com/vercel-labs/skills) at a pinned version.
A pin keeps a new, possibly compromised npm release from running unnoticed.
`update_notice` tells when a newer release has been public long enough to adopt.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

SKILLS_CLI_PACKAGE = "skills"
SKILLS_CLI_PINNED = "1.7.6"
MIN_RELEASE_AGE_DAYS = 7
SOURCE_REPOSITORY = "islomar/ai-office"
# Two agents make the CLI keep one copy in .agents/skills and link it from .claude/skills.
# A single claude-code target copies into .claude/skills, and the first `update` then moves it.
DEFAULT_AGENTS = ("claude-code", "opencode")
WORKFLOW_TEMPLATE = Path("templates/skills-update.yml")
WORKFLOW_PATH = Path(".github/workflows/skills-update.yml")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path


def list_skills(root: Path) -> list[Skill]:
    skills = []
    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        match = FRONT_MATTER.match(skill_md.read_text(encoding="utf-8"))
        meta = (yaml.safe_load(match.group(1)) if match else None) or {}
        skills.append(
            Skill(
                name=str(meta.get("name", skill_md.parent.name)),
                description=" ".join(str(meta.get("description", "")).split()),
                path=skill_md.parent,
            )
        )
    return skills


def is_installed(repo: Path, name: str) -> bool:
    if any((repo / folder / "skills" / name).exists() for folder in (".agents", ".claude")):
        return True
    lock = repo / "skills-lock.json"
    if lock.is_file():
        try:
            return name in json.loads(lock.read_text(encoding="utf-8")).get("skills", {})
        except (json.JSONDecodeError, AttributeError):
            return False
    return False


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def update_notice(pinned: str, release_times: dict[str, str], today: dt.date) -> str | None:
    """Return a message when a newer stable release is at least MIN_RELEASE_AGE_DAYS old.

    `release_times` is the `time` field of `npm view <package> --json`: version -> ISO timestamp.
    """
    releases = {
        version: dt.date.fromisoformat(stamp[:10])
        for version, stamp in release_times.items()
        if SEMVER.match(version)
    }
    newer = sorted((v for v in releases if _version_key(v) > _version_key(pinned)), key=_version_key)
    if not newer:
        return None
    mature = [v for v in newer if (today - releases[v]).days >= MIN_RELEASE_AGE_DAYS]
    latest = newer[-1]
    if not mature:
        return (
            f"skills CLI {latest} is out ({releases[latest]}), but younger than {MIN_RELEASE_AGE_DAYS} days. "
            f"Keeping {pinned}."
        )
    candidate = mature[-1]
    return (
        f"UPDATE AVAILABLE: skills CLI {candidate} ({releases[candidate]}) is at least "
        f"{MIN_RELEASE_AGE_DAYS} days old; the pin is {pinned}. "
        f"Read its changelog, then update SKILLS_CLI_PINNED in tools/ai_office/skills.py, "
        f"SKILLS_CLI in {WORKFLOW_TEMPLATE}, and the allow rule '{permission_rule(candidate)}' "
        f"in ~/.claude/settings.json."
    )


def workflow_status(root: Path, repo: Path) -> str:
    """Return 'missing', 'outdated' or 'current' for the update workflow in `repo`."""
    installed = repo / WORKFLOW_PATH
    if not installed.is_file():
        return "missing"
    template = (root / WORKFLOW_TEMPLATE).read_text(encoding="utf-8")
    return "current" if installed.read_text(encoding="utf-8") == template else "outdated"


def write_workflow(root: Path, repo: Path) -> Path:
    target = repo / WORKFLOW_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text((root / WORKFLOW_TEMPLATE).read_text(encoding="utf-8"), encoding="utf-8")
    return target


def github_slug(repo: Path) -> str | None:
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            cwd=repo, capture_output=True, text=True, timeout=20, check=True,
        )  # fmt: skip
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def actions_workflow_permissions(slug: str) -> dict | None:
    """The repository's Actions settings: default_workflow_permissions, can_approve_pull_request_reviews."""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{slug}/actions/permissions/workflow"],
            capture_output=True, text=True, timeout=20, check=True,
        )  # fmt: skip
        return json.loads(result.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return None


def allow_pull_requests_command(slug: str, current: dict) -> list[str]:
    """`gh api` call that lets Actions open pull requests and keeps the default token permissions."""
    return [
        "gh", "api", "-X", "PUT", f"repos/{slug}/actions/permissions/workflow",
        "-f", f"default_workflow_permissions={current.get('default_workflow_permissions', 'read')}",
        "-F", "can_approve_pull_request_reviews=true",
    ]  # fmt: skip


def fetch_release_times(package: str = SKILLS_CLI_PACKAGE) -> dict[str, str] | None:
    try:
        result = subprocess.run(
            ["npm", "view", package, "time", "--json"], capture_output=True, text=True, timeout=20, check=True
        )
        return json.loads(result.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return None


def permission_rule(version: str = SKILLS_CLI_PINNED) -> str:
    return f"Bash(npx -y skills@{version} *)"


def has_permission_rule(settings_file: Path, version: str = SKILLS_CLI_PINNED) -> bool:
    try:
        settings = json.loads(settings_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return permission_rule(version) in settings.get("permissions", {}).get("allow", [])


def install_command(name: str, agents: tuple[str, ...] = DEFAULT_AGENTS) -> list[str]:
    command = ["npx", "-y", f"skills@{SKILLS_CLI_PINNED}", "add", SOURCE_REPOSITORY, "--skill", name]
    for agent in agents:
        command += ["-a", agent]
    return command + ["-y"]


def unpublished_reason(root: Path, name: str) -> str | None:
    """Return why the skill on GitHub may differ from the local one, or None when it is published."""

    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True).stdout

    path = f"skills/{name}"
    if git("status", "--porcelain", "--untracked-files=all", "--", path).strip():
        return f"{path} has uncommitted changes"
    if git("rev-list", "--count", "origin/main..HEAD", "--", path).strip() != "0":
        return f"{path} has commits that are not pushed to origin/main"
    return None
