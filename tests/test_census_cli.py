import pathlib

import pytest

from census import __main__ as cli
from tests.test_census_rules import _COMPLIANT_FILES


def _checkout(root: pathlib.Path, files: dict[str, str]) -> None:
    repo = root / "demo-lib"
    (repo / ".git").mkdir(parents=True)
    (repo / ".git" / "config").write_text('[remote "origin"]\n\turl = git@github.com:modern-python/demo-lib.git\n')
    for path, text in files.items():
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)


@pytest.mark.parametrize(
    ("overrides", "expected_exit"),
    [({}, 0), ({"CLAUDE.md": "# not the pointer\n"}, cli.EXIT_FINDINGS)],
)
def test_cli_exit_code_distinguishes_findings_from_success(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    overrides: dict[str, str],
    expected_exit: int,
) -> None:
    _checkout(tmp_path, {**_COMPLIANT_FILES, **overrides})
    monkeypatch.setenv("CENSUS_NEWEST_PYTHON", "3.14")
    monkeypatch.setattr("sys.argv", ["census", "--local", str(tmp_path), "--markdown"])
    assert cli.main() == expected_exit
    assert "1 repos" in capsys.readouterr().out


def test_findings_exit_code_is_not_the_crash_exit_code() -> None:
    assert cli.EXIT_FINDINGS != 1
