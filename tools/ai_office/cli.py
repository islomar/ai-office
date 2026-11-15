"""Command line entry point: `uv run ai-office <command>`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai_office import records


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

    args = parser.parse_args(argv)
    root = find_root(Path.cwd())

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


if __name__ == "__main__":
    sys.exit(main())
