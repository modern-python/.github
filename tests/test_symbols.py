from xml.dom import minidom
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
