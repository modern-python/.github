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


ICON_SIZE_IN_LOCKUP = 80  # px of the embedded icon nested-svg


def icon_inner(kind: str, **kw: object) -> str:
    if kind == "org":
        return ('<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
                f'{_outer()}{_middle()}'
                '<circle cx="50" cy="50" r="5" fill="var(--struct)" stroke="none"/></g>')
    if kind == "monogram":
        size = 30 if len(kw["initials"]) <= 2 else 26  # ty: ignore[arg-type]
        baseline = OPTICAL_CENTER + cap_height_scaled(size) / 2
        glyphs, _ = outline_text(
            kw["initials"],  # ty: ignore[arg-type]
            size,
            x=50,
            baseline_y=baseline,
            anchor="middle",
            color=kw["ink"],  # ty: ignore[arg-type]
        )
        return _frame(kw["frame_color"]) + glyphs  # ty: ignore[operator]
    if kind == "template":
        bars = "".join(
            f'<rect x="37" y="{y}" width="26" height="6" rx="3"/>'
            for y in (39, 48, 57)
        )
        return _frame(kw["frame_color"]) + f'<g fill="{kw["ink"]}">{bars}</g>'  # ty: ignore[operator]
    raise ValueError(kind)


def _lockup_style() -> str:
    """Combined style: --struct and --accent for the embedded icon, --ink for the wordmark."""
    return ("<style>:root{"
            f"--struct:{t.GREEN};--accent:{t.GOLD};--ink:{t.GREEN}"
            "}@media (prefers-color-scheme: dark){:root{"
            f"--struct:{t.GREEN_DARK};--accent:{t.GOLD_DARK};--ink:{t.GREEN_DARK}"
            "}}</style>")


def lockup_horizontal(icon_inner_svg: str, wordmark: str, label: str) -> str:
    fs = 46
    icon_px = 96
    gap = 26
    h = 100
    baseline = h / 2 + cap_height_scaled(fs) / 2
    wm, w = outline_text(wordmark, fs, x=icon_px + gap, baseline_y=baseline,
                         color="var(--ink)")
    total_w = icon_px + gap + w
    body = (
        f'<svg x="0" y="2" width="{icon_px}" height="{icon_px}" '
        f'viewBox="0 0 100 100">{icon_inner_svg}</svg>'
        f'{wm}'
    )
    return svg(body, w=round(total_w, 1), h=h, label=label, style=_lockup_style())


def lockup_stacked(icon_inner_svg: str, wordmark: str, label: str) -> str:
    fs = 22
    icon_px = 96
    wm, _ = outline_text(wordmark, fs, x=64, baseline_y=128, anchor="middle",
                         color="var(--ink)")
    body = (
        f'<svg x="16" y="0" width="{icon_px}" height="{icon_px}" '
        f'viewBox="0 0 100 100">{icon_inner_svg}</svg>{wm}'
    )
    return svg(body, w=128, h=140, label=label, style=_lockup_style())


def social_card(icon_inner_svg: str, wordmark: str, label: str) -> str:
    fs = 64
    icon_px = 220
    wm, _ = outline_text(wordmark, fs, x=640, baseline_y=470, anchor="middle",
                         color=t.GREEN)
    body = (
        f'<rect width="1280" height="640" fill="#ffffff"/>'
        f'<svg x="{640 - icon_px // 2}" y="150" width="{icon_px}" height="{icon_px}" '
        f'viewBox="0 0 100 100">{icon_inner_svg}</svg>{wm}'
    )
    style = ("<style>:root{"
             f"--struct:{t.GREEN};--accent:{t.GOLD}"
             "}</style>")
    return svg(body, w=1280, h=640, label=label, style=style)
