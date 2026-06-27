from pathlib import Path
from brand.build import geometry as g

ROOT = Path(__file__).resolve().parents[2]
ORG = ROOT / "brand" / "org"

MANIFEST: list[tuple[Path, object]] = []


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def render_org() -> None:
    inner = g.icon_inner("org")
    _write(ORG / "icon.svg", g.org_icon())
    _write(ORG / "favicon.svg", g.org_favicon())
    _write(ORG / "horizontal.svg", g.lockup_horizontal(inner, "modern-python", label="Modern Python"))
    _write(ORG / "stacked.svg", g.lockup_stacked(inner, "modern-python", label="Modern Python"))
    _write(ORG / "social.svg", g.social_card(inner, "modern-python", label="Modern Python"))


def main() -> None:
    render_org()
    # project rendering added in later tasks


if __name__ == "__main__":
    main()
