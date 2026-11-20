"""Create and check the Markdown records of the workspace.

A record is a Markdown file with YAML front matter.
Its file name is `<id>-<slug>.md`, and the id carries a random suffix,
so two people can create records at the same time without clashing.
"""

from __future__ import annotations

import datetime as dt
import re
import secrets
from dataclasses import dataclass
from pathlib import Path

import yaml

KINDS = {
    "task": {
        "folder": "tasks",
        "prefix": "T",
        "required": ["id", "title", "status", "created"],
        "statuses": ["open", "doing", "validating", "done", "discarded"],
        "initial": "open",
    },
    "decision": {
        "folder": "decisions",
        "prefix": "DR",
        "required": ["id", "title", "status", "date"],
        "statuses": ["proposed", "accepted", "superseded", "rejected"],
        "initial": "proposed",
    },
    "knowledge": {
        "folder": "knowledge",
        "prefix": "K",
        "required": ["id", "title", "updated"],
        "statuses": None,
        "initial": None,
    },
}

ID_PATTERN = re.compile(r"^(T|DR|K)-[0-9a-f]{6}$")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

# Instruction files must not send agents to per-user harness memory:
# knowledge that matters lives in this repository.
PRIVATE_MEMORY = re.compile(r"\.claude/projects/[^\s)]*memory")
SCANNED_SUFFIXES = {".md", ".json", ".toml", ".yaml", ".yml"}
SKIPPED_DIRS = {".git", ".venv", "node_modules", "tools", "tests"}


@dataclass(frozen=True)
class Problem:
    path: Path
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(slug) > 60:
        slug = slug[:61].rsplit("-", 1)[0]
    return slug or "untitled"


def new_id(prefix: str) -> str:
    return f"{prefix}-{secrets.token_hex(3)}"


def create(root: Path, kind: str, title: str, today: dt.date | None = None) -> Path:
    spec = KINDS[kind]
    today = today or dt.date.today()
    record_id = new_id(spec["prefix"])
    meta: dict[str, object] = {"id": record_id, "title": title}
    if kind == "task":
        meta |= {"status": spec["initial"], "created": today}
    elif kind == "decision":
        meta |= {"status": spec["initial"], "date": today}
    else:
        meta |= {"updated": today}
    path = root / spec["folder"] / f"{record_id}-{slugify(title)}.md"
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=10_000)
    path.write_text(f"---\n{front}---\n\n# {title}\n", encoding="utf-8")
    return path


def read_front_matter(path: Path) -> dict | None:
    match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        return None
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, dict) else None


def check_records(root: Path) -> list[Problem]:
    problems: list[Problem] = []
    seen: dict[str, Path] = {}
    for spec in KINDS.values():
        folder = root / spec["folder"]
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.md")):
            if path.name == "README.md":
                continue
            meta = read_front_matter(path)
            if meta is None:
                problems.append(Problem(path, "missing YAML front matter"))
                continue
            for field in spec["required"]:
                if field not in meta:
                    problems.append(Problem(path, f"missing field '{field}'"))
            record_id = str(meta.get("id", ""))
            if record_id and not record_id.startswith(f"{spec['prefix']}-"):
                problems.append(Problem(path, f"id '{record_id}' must start with '{spec['prefix']}-'"))
            elif record_id and not ID_PATTERN.match(record_id):
                problems.append(Problem(path, f"id '{record_id}' must be <prefix>-<6 hex chars>"))
            if record_id and not path.name.startswith(f"{record_id}-"):
                problems.append(Problem(path, f"file name must start with '{record_id}-'"))
            if record_id in seen:
                problems.append(Problem(path, f"duplicate id '{record_id}', also in {seen[record_id]}"))
            elif record_id:
                seen[record_id] = path
            statuses = spec["statuses"]
            if statuses and "status" in meta and meta["status"] not in statuses:
                problems.append(Problem(path, f"status '{meta['status']}' not in {statuses}"))
    return problems


def check_private_memory(root: Path) -> list[Problem]:
    problems: list[Problem] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in SCANNED_SUFFIXES:
            continue
        if SKIPPED_DIRS.intersection(path.relative_to(root).parts):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if PRIVATE_MEMORY.search(line):
                problems.append(
                    Problem(path, f"line {number} points to per-user harness memory; move the content into knowledge/")
                )
    return problems


def check(root: Path) -> list[Problem]:
    return check_records(root) + check_private_memory(root)


@dataclass(frozen=True)
class Task:
    id: str
    status: str
    created: dt.date
    title: str


# Work in progress first: a started or merged task needs attention before a new one.
PENDING_ORDER = ("doing", "validating", "open")


def pending_tasks(root: Path) -> list[Task]:
    """Tasks that still need work, in progress first, then oldest first."""
    found = []
    for path in sorted((root / KINDS["task"]["folder"]).glob("T-*.md")):
        meta = read_front_matter(path) or {}
        if meta.get("status") in PENDING_ORDER:
            found.append(Task(meta["id"], meta["status"], meta["created"], meta["title"]))
    return sorted(found, key=lambda t: (PENDING_ORDER.index(t.status), t.created, t.id))
