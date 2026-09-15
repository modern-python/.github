import datetime
import json
from pathlib import Path

import pytest

from scripts.python_matrix import derive, main

_TODAY = datetime.date(2026, 9, 15)
_CYCLES = [
    {"cycle": "3.15", "releaseDate": "2026-10-01"},
    {"cycle": "3.14", "releaseDate": "2025-10-07"},
    {"cycle": "3.13", "releaseDate": "2024-10-07"},
    {"cycle": "3.12", "releaseDate": "2023-10-02"},
    {"cycle": "3.11", "releaseDate": "2022-10-24"},
    {"cycle": "3.10", "releaseDate": "2021-10-04"},
    {"cycle": "3.9", "releaseDate": "2020-10-05"},
    {"cycle": "2.7", "releaseDate": "2010-07-03"},
]


def _pyproject(requires_python: str, name: str = "modern-di-fastapi") -> str:
    return f'[project]\nname = "{name}"\nrequires-python = "{requires_python}"\n'


def test_matrix_runs_from_the_floor_to_the_newest_released_cycle_plus_its_t_build() -> None:
    result = derive(_pyproject(">=3.10,<4"), _CYCLES, _TODAY, free_threaded=True)
    assert result.floor == "3.10"
    assert result.versions == ["3.10", "3.11", "3.12", "3.13", "3.14", "3.14t"]


def test_a_cycle_whose_release_date_is_in_the_future_is_not_the_ceiling() -> None:
    """INVARIANT: endoflife.date lists a cycle before it ships; the matrix waits for the release."""
    result = derive(_pyproject(">=3.13"), _CYCLES, datetime.date(2026, 10, 1), free_threaded=True)
    assert result.versions == ["3.13", "3.14", "3.15", "3.15t"]


def test_exempt_repo_gets_no_free_threaded_entry() -> None:
    result = derive(_pyproject(">=3.13"), _CYCLES, _TODAY, free_threaded=False)
    assert result.versions == ["3.13", "3.14"]


def test_package_is_the_distribution_name_with_underscores() -> None:
    result = derive(_pyproject(">=3.11", name="faststream-concurrent-aiokafka"), _CYCLES, _TODAY, free_threaded=True)
    assert result.package == "faststream_concurrent_aiokafka"


@pytest.mark.parametrize("requires_python", ["", ">3.10", "==3.12.*", "<4"])
def test_a_floor_without_a_ge_bound_is_rejected(requires_python: str) -> None:
    with pytest.raises(ValueError, match="requires-python"):
        derive(_pyproject(requires_python), _CYCLES, _TODAY, free_threaded=True)


def test_a_floor_above_every_released_cycle_is_rejected() -> None:
    with pytest.raises(ValueError, match=r"3\.15"):
        derive(_pyproject(">=3.15"), _CYCLES, _TODAY, free_threaded=True)


def test_cli_prints_github_output_lines(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(_pyproject(">=3.12", name="db-retry"), encoding="utf-8")
    cycles = tmp_path / "cycles.json"
    cycles.write_text(json.dumps(_CYCLES), encoding="utf-8")

    main(["--pyproject", str(pyproject), "--cycles", str(cycles), "--free-threaded", "false", "--today", "2026-09-15"])

    lines = capsys.readouterr().out.splitlines()
    assert lines == ["floor=3.12", 'versions=["3.12", "3.13", "3.14"]', "package=db_retry"]
