import os
import pathlib

import pytest

from census import python_releases, report, rules, snapshot


pytestmark = pytest.mark.census


def test_every_repo_meets_the_core() -> None:
    local_root = os.environ.get("CENSUS_LOCAL_ROOT")
    snapshots = snapshot.load_from_local(pathlib.Path(local_root)) if local_root else snapshot.load_from_github()
    assert snapshots, "no repos loaded"
    context = rules.Context(
        newest_python=python_releases.newest_cycle(),
        profile_descriptions=report.profile_descriptions(
            pathlib.Path(__file__).parent.parent / "profile" / "README.md"
        ),
    )
    findings = report.run_census(snapshots, context)
    assert not findings, "\n" + report.render_markdown(findings, len(snapshots))
