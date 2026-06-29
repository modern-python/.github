from xml.dom import minidom

import pytest

from brand.build import symbols as sym


def _wrap(markup: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{markup}</svg>'
    )


def test_helpers_emit_parseable_svg() -> None:
    for markup in (
        sym._ah(50, 50, 0.0, 6),
        sym._cyl(50, 50, 20),
        sym._star5(50, 50, 18, sym.GOLD),
        sym._circ_arc(50, 50, 20, 285, 425, 4.5),
    ):
        minidom.parseString(_wrap(markup))  # raises on malformed XML


DI_SYMBOLS = ["bolt_disc", "star_disc", "faststream", "terminal", "bars", "chevron"]


@pytest.mark.parametrize("name", DI_SYMBOLS)
def test_di_symbol_parses(name: str) -> None:
    markup = getattr(sym, name)(50, 50, 23)
    minidom.parseString(_wrap(markup))


def test_graph_dashed_vs_solid() -> None:
    assert "stroke-dasharray" in sym.graph(50, 50, 23, dashed=True)
    assert "stroke-dasharray" not in sym.graph(50, 50, 23, dashed=False)


MSG_SYMBOLS = ["rocket", "chain", "stopwatch", "lanes", "outbox"]


@pytest.mark.parametrize("name", MSG_SYMBOLS)
def test_msg_symbol_parses(name: str) -> None:
    minidom.parseString(_wrap(getattr(sym, name)(50, 50, 23)))
