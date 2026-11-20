import os

import pytest


@pytest.fixture(autouse=True)
def isolated_git_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    # The pre-commit hook runs these tests inside `git commit`, which exports GIT_INDEX_FILE and other GIT_* variables.
    # A git command in a test repository would inherit them and write into the index of the commit in progress.
    for name in [name for name in os.environ if name.startswith("GIT_")]:
        monkeypatch.delenv(name)
