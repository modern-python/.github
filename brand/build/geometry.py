from brand.build import tokens as t
from brand.build.text import outline_text, cap_height_scaled

OUTER_SNAKE = "M20 35 L20 65 Q20 80 35 80 L65 80 Q80 80 80 65 L80 35 Q80 20 65 20 L35 20"
MIDDLE_SNAKE = "M65 57 L65 43 Q65 35 57 35 L43 35 Q35 35 35 43 L35 57 Q35 65 43 65 L57 65"
STROKE = 8


def svg(body: str, *, w: int = 100, h: int = 100, label: str, style: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">{style}{body}</svg>')


def theme_style(
    struct_light: str,
    accent_light: str,
    struct_dark: str,
    accent_dark: str,
) -> str:
    return ("<style>:root{"
            f"--struct:{struct_light};--accent:{accent_light}"
            "}@media (prefers-color-scheme: dark){:root{"
            f"--struct:{struct_dark};--accent:{accent_dark}"
            "}}</style>")


def _outer(stroke_color: str = "var(--struct)") -> str:
    return (f'<g stroke="{stroke_color}" stroke-width="{STROKE}">'
            f'<path d="{OUTER_SNAKE}"/>'
            f'<circle cx="35" cy="20" r="5.5" fill="{stroke_color}" stroke="none"/></g>')


def _middle(stroke_color: str = "var(--accent)") -> str:
    return (f'<g stroke="{stroke_color}" stroke-width="{STROKE}">'
            f'<path d="{MIDDLE_SNAKE}"/>'
            f'<circle cx="65" cy="57" r="5.5" fill="{stroke_color}" stroke="none"/></g>')


def org_icon() -> str:
    body = ('<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'{_outer()}{_middle()}'
            '<circle cx="50" cy="50" r="5" fill="var(--struct)" stroke="none"/>'
            '</g>')
    style = theme_style(t.GREEN, t.GOLD, t.GREEN_DARK, t.GOLD_DARK)
    return svg(body, label="Modern Python", style=style)


OPTICAL_CENTER = 48.5


def _frame(frame_color: str) -> str:
    return (f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'{_outer(frame_color)}</g>')


def project_monogram(initials: str, *, frame_color: str, ink: str, label: str) -> str:
    size = 30 if len(initials) <= 2 else 26
    baseline = OPTICAL_CENTER + cap_height_scaled(size) / 2
    glyphs, _ = outline_text(initials, size, x=50, baseline_y=baseline,
                             anchor="middle", color=ink)
    return svg(_frame(frame_color) + glyphs, label=label)


def project_template(*, frame_color: str, ink: str, label: str) -> str:
    bars = "".join(
        f'<rect x="37" y="{y}" width="26" height="6" rx="3"/>'
        for y in (39, 48, 57)
    )
    glyph = f'<g fill="{ink}">{bars}</g>'
    return svg(_frame(frame_color) + glyph, label=label)


def org_favicon() -> str:
    body = ('<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'{_outer()}{_middle()}</g>')
    style = theme_style(t.GREEN, t.GOLD, t.GREEN_DARK, t.GOLD_DARK)
    return svg(body, label="Modern Python", style=style)
