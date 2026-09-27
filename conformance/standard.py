import dataclasses
import pathlib
import re
import typing


STANDARD: typing.Final = pathlib.Path(__file__).resolve().parent.parent / "docs" / "standard.md"
_REQUIREMENT: typing.Final = re.compile(r"^### ([A-Z]{2}\d+) · .*\{ #\1 \}$", re.MULTILINE)
_ROW: typing.Final = re.compile(r"^\| `([a-z0-9.-]+)` \| (.+?) \| .+ \|$", re.MULTILINE)
_CITED_ID: typing.Final = re.compile(r"\[([A-Z]{2}\d+)\]\(#\1\)")


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exemption:
    ids: frozenset[str]
    whole_core: bool

    def covers(self, requirement: str) -> bool:
        return requirement not in self.ids if self.whole_core else requirement in self.ids


def requirement_ids(text: str) -> list[str]:
    return _REQUIREMENT.findall(text)


def exemptions(text: str) -> dict[str, Exemption]:
    table = text.split("## Exemptions", 1)[1].split("\n## ", 1)[0]
    return {
        repo: Exemption(ids=frozenset(_CITED_ID.findall(scope)), whole_core=scope.startswith("the core as a whole"))
        for repo, scope in _ROW.findall(table)
    }
