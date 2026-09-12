import pathlib
import re

from census import registry, rules


_STANDARD = pathlib.Path(__file__).parent.parent / "docs" / "standard.md"
_ROW_NAMES = re.compile(r"`([a-z0-9-]+)`")


def _exemption_table_repos() -> frozenset[str]:
    section = _STANDARD.read_text(encoding="utf-8").split("## Exemptions", 1)[1].split("## ", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("| `")]
    return frozenset(name for row in rows for name in _ROW_NAMES.findall(row.split("|")[1]))


def test_registry_and_standard_list_the_same_exempt_repos() -> None:
    """INVARIANT: every repo the census exempts has a row in the standard's Exemptions table, and vice versa.

    The registry is what the census honours; the table is what a reader sees. An exemption added to
    one and not the other is either silently unenforced or silently undocumented.
    """
    assert _exemption_table_repos() == registry.exempted_repos()


def test_every_exemption_names_a_known_item() -> None:
    known = registry.CORE_ITEMS
    for repo, items in registry.EXEMPTIONS.items():
        assert items <= known, f"{repo} is exempt from unknown items {items - known}"


def test_every_core_item_has_a_rule_or_is_a_placeholder() -> None:
    assert registry.CORE_ITEMS - set(rules.RULES) == {"shared-pytest-job"}


def test_canonical_paragraphs_match_the_standard() -> None:
    text = rules.normalize_whitespace(_STANDARD.read_text(encoding="utf-8"))
    for paragraph in registry.CANONICAL_PARAGRAPHS:
        assert rules.normalize_whitespace(paragraph) in text


def test_canonical_ignores_match_the_standard() -> None:
    block = _STANDARD.read_text(encoding="utf-8").split("ignore = [", 1)[1].split("]", 1)[0]
    assert frozenset(re.findall(r'"([A-Z0-9]+)"', block)) == registry.CANONICAL_IGNORES
