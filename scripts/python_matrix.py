"""Derive a repo's CI Python matrix for the shared ``checks.yml``.

Every minor from the ``>=`` bound of ``requires-python`` to the newest released CPython cycle, plus
that cycle's free-threaded build. Prints ``$GITHUB_OUTPUT`` lines.
"""

import argparse
import dataclasses
import datetime
import json
import re
import sys
import tomllib
from pathlib import Path

_FLOOR = re.compile(r">=\s*(\d+)\.(\d+)")


@dataclasses.dataclass(frozen=True)
class Matrix:
    floor: str
    versions: list[str]
    package: str


def derive(pyproject: str, cycles: list[dict[str, str]], today: datetime.date, *, free_threaded: bool) -> Matrix:
    project = tomllib.loads(pyproject)["project"]
    requires_python = project.get("requires-python", "")
    floor_match = _FLOOR.search(requires_python)
    if floor_match is None:
        msg = f"requires-python {requires_python!r} has no >=X.Y bound to read the floor from"
        raise ValueError(msg)
    floor = (int(floor_match[1]), int(floor_match[2]))

    released = [
        tuple(int(part) for part in cycle["cycle"].split("."))
        for cycle in cycles
        if datetime.date.fromisoformat(cycle["releaseDate"]) <= today
    ]
    ceiling = max(minor for minor in released if minor[0] == floor[0])
    if floor > ceiling:
        msg = f"floor {floor[0]}.{floor[1]} is above the newest released cycle {ceiling[0]}.{ceiling[1]}"
        raise ValueError(msg)

    versions = [f"{floor[0]}.{minor}" for minor in range(floor[1], ceiling[1] + 1)]
    if free_threaded:
        versions.append(f"{versions[-1]}t")
    return Matrix(floor=versions[0], versions=versions, package=project["name"].replace("-", "_"))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pyproject", type=Path, required=True)
    parser.add_argument("--cycles", type=Path, required=True, help="endoflife.date/api/python.json saved to a file")
    parser.add_argument("--free-threaded", choices=["true", "false"], required=True)
    parser.add_argument(
        "--today", type=datetime.date.fromisoformat, default=datetime.datetime.now(tz=datetime.UTC).date()
    )
    args = parser.parse_args(argv)

    matrix = derive(
        args.pyproject.read_text(encoding="utf-8"),
        json.loads(args.cycles.read_text(encoding="utf-8")),
        args.today,
        free_threaded=args.free_threaded == "true",
    )
    sys.stdout.write(f"floor={matrix.floor}\nversions={json.dumps(matrix.versions)}\npackage={matrix.package}\n")


if __name__ == "__main__":
    main()
