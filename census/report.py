import dataclasses
import pathlib
import re
import typing

from census import registry, rules
from census.snapshot import RepoSnapshot


_PROFILE_ROW: typing.Final = re.compile(
    r"^\| \[`(?P<name>[^`]+)`\]\([^)]+\) \| (?P<description>[^|]+?) \|", re.MULTILINE
)


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Finding:
    repo: str
    item: str
    message: str


def profile_descriptions(profile: pathlib.Path) -> dict[str, str]:
    return {
        m.group("name"): m.group("description").strip()
        for m in _PROFILE_ROW.finditer(profile.read_text(encoding="utf-8"))
    }


def run_census(snapshots: typing.Iterable[RepoSnapshot], context: rules.Context) -> list[Finding]:
    findings = []
    for snapshot in snapshots:
        for item in sorted(registry.applicable_items(snapshot.name)):
            rule = rules.RULES.get(item)
            if rule is None:
                continue
            findings.extend(
                Finding(repo=snapshot.name, item=item, message=message) for message in rule(snapshot, context)
            )
    return findings


def render_markdown(findings: typing.Sequence[Finding], repo_count: int) -> str:
    if not findings:
        return f"All {repo_count} repos meet the core."
    lines = [f"{len(findings)} findings across {len({f.repo for f in findings})} of {repo_count} repos.", ""]
    for repo in sorted({finding.repo for finding in findings}):
        lines.append(f"### {repo}")
        lines.extend(f"- **{f.item}**: {f.message}" for f in findings if f.repo == repo)
        lines.append("")
    return "\n".join(lines)
