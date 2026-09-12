import argparse
import os
import pathlib
import sys

from census import python_releases, report, rules, snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Check every modern-python repo against the standard's core.")
    parser.add_argument(
        "--local", type=pathlib.Path, default=None, help="read checkouts under this directory instead of GitHub"
    )
    parser.add_argument("--markdown", action="store_true", help="print the findings as Markdown")
    args = parser.parse_args()
    local_root = args.local or (pathlib.Path(root) if (root := os.environ.get("CENSUS_LOCAL_ROOT")) else None)
    snapshots = snapshot.load_from_local(local_root) if local_root else snapshot.load_from_github()
    profile = pathlib.Path(__file__).resolve().parent.parent / "profile" / "README.md"
    context = rules.Context(
        newest_python=python_releases.newest_cycle(),
        profile_descriptions=report.profile_descriptions(profile),
    )
    findings = report.run_census(snapshots, context)
    if args.markdown:
        sys.stdout.write(report.render_markdown(findings, len(snapshots)) + "\n")
    else:
        for finding in findings:
            sys.stdout.write(f"{finding.repo}\t{finding.item}\t{finding.message}\n")
        sys.stdout.write(f"{len(findings)} findings across {len(snapshots)} repos\n")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
