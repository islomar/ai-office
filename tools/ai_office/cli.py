"""Command line entry point: `uv run ai-office <command>`."""

from __future__ import annotations

import argparse
import datetime as dt
import shlex
import sys
from pathlib import Path

from ai_office import records, skills

CLAUDE_SETTINGS = Path.home() / ".claude" / "settings.json"


def find_root(start: Path) -> Path:
    for folder in [start, *start.parents]:
        if (folder / "AGENTS.md").is_file() and (folder / "pyproject.toml").is_file():
            return folder
    raise SystemExit("ai-office: run this inside the ai-office repository")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ai-office")
    commands = parser.add_subparsers(dest="command", required=True)

    new = commands.add_parser("new", help="create a task, decision or knowledge record")
    new.add_argument("kind", choices=sorted(records.KINDS))
    new.add_argument("title")

    commands.add_parser("check", help="check every record and instruction file")

    listing = commands.add_parser("list-skills", help="list the skills in skills/")
    listing.add_argument("--repo", type=Path, default=Path.cwd(), help="mark the skills installed in this repository")

    plan = commands.add_parser("install-plan", help="check a skill can be installed and print the command")
    plan.add_argument("name")
    plan.add_argument("--agent", action="append", help="target agent (repeatable), default claude-code and opencode")

    commands.add_parser("write-workflow", help="write the skills update workflow into the current repository")

    args = parser.parse_args(argv)
    tool_commands = ("list-skills", "install-plan", "write-workflow")
    root = Path(__file__).resolve().parents[2] if args.command in tool_commands else find_root(Path.cwd())

    if args.command == "list-skills":
        return list_skills(root, args.repo.resolve())
    if args.command == "install-plan":
        return install_plan(root, args.name, tuple(args.agent or skills.DEFAULT_AGENTS))
    if args.command == "write-workflow":
        print(f"wrote {skills.write_workflow(root, Path.cwd())}")
        return 0

    if args.command == "new":
        path = records.create(root, args.kind, args.title)
        print(path.relative_to(root))
        return 0

    problems = records.check(root)
    for problem in problems:
        print(problem.__str__().replace(f"{root}/", ""), file=sys.stderr)
    if problems:
        print(f"ai-office check: {len(problems)} problem(s)", file=sys.stderr)
        return 1
    print("ai-office check: ok")
    return 0


def list_skills(root: Path, repo: Path) -> int:
    found = skills.list_skills(root)
    print(f"Skills in {root / 'skills'} ({len(found)}); [x] = installed in {repo}")
    for skill in found:
        mark = "x" if skills.is_installed(repo, skill.name) else " "
        print(f"[{mark}] {skill.name}: {skill.description}")
    return 0


def install_plan(root: Path, name: str, agents: tuple[str, ...]) -> int:
    """Print the checks and, when they pass, the exact command; exit 1 when a check blocks it."""
    blocked = False
    if name not in {s.name for s in skills.list_skills(root)}:
        print(f"BLOCKED: no skill '{name}' in {root / 'skills'}. Run list-skills.")
        return 1
    reason = skills.unpublished_reason(root, name)
    if reason:
        print(f"BLOCKED: {reason}. The CLI installs from GitHub: ship ai-office first.")
        blocked = True

    times = skills.fetch_release_times()
    if times is None:
        print("WARNING: could not ask npm for skills CLI releases; update check skipped.")
    else:
        notice = skills.update_notice(skills.SKILLS_CLI_PINNED, times, dt.date.today())
        print(notice or f"skills CLI pin {skills.SKILLS_CLI_PINNED} is the latest release.")

    if not skills.has_permission_rule(CLAUDE_SETTINGS):
        print(f"NOTE: '{skills.permission_rule()}' is not in {CLAUDE_SETTINGS}; the command will need approval.")

    if blocked:
        return 1
    print("COMMAND: " + shlex.join(skills.install_command(name, agents)))
    report_update_workflow(root, Path.cwd())
    return 0


def report_update_workflow(root: Path, repo: Path) -> None:
    status = skills.workflow_status(root, repo)
    if status == "current":
        print(f"WORKFLOW: {skills.WORKFLOW_PATH} is current.")
    else:
        print(f"WORKFLOW: {skills.WORKFLOW_PATH} is {status}. "
              "Write it with: uv run --project ~/workspace/ai-office ai-office write-workflow")
    slug = skills.github_slug(repo)
    if slug is None:
        print("SETTING: no GitHub repository found; the workflow runs only once this repository is on GitHub.")
        return
    current = skills.actions_workflow_permissions(slug)
    if current is None:
        print(f"SETTING: could not read the Actions settings of {slug}; check them by hand.")
    elif current.get("can_approve_pull_request_reviews"):
        print(f"SETTING: GitHub Actions can open pull requests in {slug}.")
    else:
        print(f"SETTING: GitHub Actions cannot open pull requests in {slug}. "
              "Allow it with: " + shlex.join(skills.allow_pull_requests_command(slug, current)))


if __name__ == "__main__":
    sys.exit(main())
