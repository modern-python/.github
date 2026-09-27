import argparse
import collections
import datetime
import json
import pathlib
import re
import subprocess
import typing
import urllib.error
import urllib.request

from conformance.checks import (
    UNCHECKED,
    Finding,
    Metadata,
    Repo,
    Status,
    evaluate,
    release_fingerprint,
)
from conformance.standard import STANDARD, exemptions


ORG: typing.Final = "modern-python"
PROFILE: typing.Final = pathlib.Path(__file__).resolve().parent.parent / "profile" / "README.md"
_PROFILE_ROW: typing.Final = re.compile(r"^\| \[`([a-z0-9.-]+)`\]\([^)]*\) \| ([^|]+?) \|", re.MULTILINE)
_MARK: typing.Final = {Status.PASS: "pass", Status.WARN: "WARN", Status.FAIL: "FAIL", Status.EXEMPT: "exempt"}


def _gh_json(*arguments: str) -> typing.Any:
    completed = subprocess.run(["gh", *arguments], check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def published_from(info: dict[str, typing.Any], name: str) -> bool:
    urls = [info.get("home_page") or "", *(info.get("project_urls") or {}).values()]
    return any(f"github.com/{ORG}/{name}" in url for url in urls)


def _on_pypi(name: str) -> bool:
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=30) as response:
            return published_from(json.load(response)["info"], name)
    except urllib.error.HTTPError:
        return False


def core_repos() -> list[dict[str, typing.Any]]:
    listed = _gh_json(
        "repo", "list", ORG, "--no-archived", "--source", "--limit", "200",
        "--json", "name,description,homepageUrl,repositoryTopics",
    )
    return sorted((repo for repo in listed if _on_pypi(repo["name"])), key=lambda repo: repo["name"])


def profile_rows(text: str) -> dict[str, str]:
    return {name: description.strip() for name, description in _PROFILE_ROW.findall(text)}


def _clone(name: str, workdir: pathlib.Path) -> pathlib.Path:
    target = workdir / name
    if not target.exists():
        subprocess.run(
            ["git", "clone", "--quiet", "--depth", "1", f"https://github.com/{ORG}/{name}", str(target)], check=True
        )
    return target


def with_release_consistency(repos: list[Repo], results: dict[str, list[Finding]]) -> None:
    fingerprints = {repo.name: release_fingerprint(repo) for repo in repos}
    compared = [fingerprints[repo.name] for repo in repos if not repo.exempt_from("RL5")]
    modal = collections.Counter(compared).most_common(1)[0][0] if compared else ""
    for repo in repos:
        if fingerprints[repo.name] == modal:
            finding = Finding(requirement="RL5", status=Status.PASS)
        elif repo.exempt_from("RL5"):
            finding = Finding(requirement="RL5", status=Status.EXEMPT)
        else:
            finding = Finding(requirement="RL5", status=Status.FAIL, detail="release.yml differs from the other repos")
        results[repo.name].append(finding)


def render(name: str, findings: list[Finding]) -> str:
    ordered = sorted(findings, key=lambda finding: (finding.requirement[:2], int(finding.requirement[2:])))
    lines = [f"## `{name}`", "", "| Requirement | Result | Detail |", "|---|---|---|"]
    lines += [
        f"| [{finding.requirement}](https://modern-python.org/standard/#{finding.requirement}) "
        f"| {_MARK[finding.status]} | {finding.detail} |"
        for finding in ordered
        if finding.status in (Status.FAIL, Status.WARN)
    ]
    return "\n".join(lines) + "\n"


def run(workdir: pathlib.Path, out: pathlib.Path, today: datetime.date) -> dict[str, list[Finding]]:
    exempt = exemptions(STANDARD.read_text(encoding="utf-8"))
    rows = profile_rows(PROFILE.read_text(encoding="utf-8"))
    repos = []
    for listed in core_repos():
        name = listed["name"]
        titles = _gh_json("pr", "list", "-R", f"{ORG}/{name}", "--state", "merged", "--limit", "20", "--json", "title")
        metadata = Metadata(
            description=listed.get("description") or "",
            homepage=listed.get("homepageUrl") or "",
            topics=tuple(topic["name"] for topic in listed.get("repositoryTopics") or []),
            profile_row=rows.get(name),
            pr_titles=tuple(entry["title"] for entry in titles),
        )
        repos.append(
            Repo(name=name, root=_clone(name, workdir), metadata=metadata, exemption=exempt.get(name), today=today)
        )
    results = {repo.name: evaluate(repo) for repo in repos}
    with_release_consistency(repos, results)
    out.mkdir(parents=True, exist_ok=True)
    failing = sorted(name for name, findings in results.items() if any(f.status is Status.FAIL for f in findings))
    for name, findings in results.items():
        (out / f"{name}.md").write_text(render(name, findings), encoding="utf-8")
    (out / "failing.txt").write_text("".join(f"{name}\n" for name in failing), encoding="utf-8")
    (out / "checked.txt").write_text("".join(f"{name}\n" for name in sorted(results)), encoding="utf-8")
    summary = [
        f"Checked {len(results)} core repos on {today.isoformat()}; {len(failing)} failing.",
        f"Not checked automatically: {', '.join(UNCHECKED)}.",
        "",
    ]
    summary += [render(name, findings) for name, findings in sorted(results.items())]
    (out / "summary.md").write_text("\n".join(summary), encoding="utf-8")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(prog="conformance", description="Check the core repos against the standard.")
    parser.add_argument("--workdir", type=pathlib.Path, required=True, help="where to clone the repos")
    parser.add_argument("--out", type=pathlib.Path, required=True, help="where to write the reports")
    arguments = parser.parse_args()
    arguments.workdir.mkdir(parents=True, exist_ok=True)
    run(arguments.workdir, arguments.out, datetime.datetime.now(tz=datetime.UTC).date())


if __name__ == "__main__":
    main()
