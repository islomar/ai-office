import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = (REPO_ROOT / "Makefile").read_text()
TARGET = re.compile(r"^([a-zA-Z0-9_-]+):(?!=)(.*)$", re.MULTILINE)


def test_every_target_has_a_description_so_make_help_lists_everything() -> None:
    undocumented = [name for name, rest in TARGET.findall(MAKEFILE) if "## " not in rest]

    assert undocumented == []


def test_plain_make_shows_the_help() -> None:
    output = subprocess.run(["make", "-s", "-C", str(REPO_ROOT)], capture_output=True, text=True, check=True).stdout

    listed = {line.split()[0] for line in output.splitlines() if line.strip()}
    assert listed == {name for name, _ in TARGET.findall(MAKEFILE)}
