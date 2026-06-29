# per-project-brand-marks — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a large-format logo for every org repo — the constant
green+gold snake-frame with one gold inner symbol per repo — from `brand/build/`
into `brand/projects/<repo>/`.

**Spec:** [`design.md`](./design.md)

**Branch:** `brand-project-marks` (already created)

**Commit strategy:** Per-task commits.

## Global constraints

- **Colours come only from `brand/build/tokens.py`** — `GREEN_INK #356852`
  (frame struct), `GOLD_LIGHT #c98a00` (frame accent + inner symbol),
  `CREAM #f4f1e8` (negative space). The only exception: `pytest` bar tints
  (declared in `symbols.py` as `_BAR_TINTS`).
- **Frame geometry is fixed:** 100×100 viewBox, `margin=9`, arm `Lx=Ly=53`,
  stroke `s=11`. Inner symbol centred at `(50, 50)`, nominal radius `R=23`.
- **Two colours only** (green + gold); no per-family accent. Differentiate by
  symbol shape.
- **Large-format only.** Do not touch the org favicon/avatar (`brand/org/`).
- All new code: imports at module level, annotate function args, `ty: ignore`
  (not `type: ignore`) if a suppression is ever needed.
- Tooling: `uv run python -m brand.build.render` regenerates; `rsvg-convert`
  rasterises PNGs (skipped gracefully if absent, per existing `export_png`).

---

### Task 1: Symbol module scaffold + shared helpers

**Files:**
- Create: `brand/build/symbols.py`
- Test: `tests/test_symbols.py`

**Interfaces:**
- Produces: `_ah(tx,ty,ang,sz,fill=GOLD)`, `_cyl(cx,cy,r,h=0.78,w=1.0,fill=GOLD)`,
  `_star5(cx,cy,R,color,inner=0.42)`, `_circ_arc(cx,cy,rad,a0,a1,w)` — all return
  SVG-fragment `str`. Module constants `GOLD=GOLD_LIGHT`, `_BAR_TINTS`.

- [ ] **Step 1: Write the failing test**

  ```python
  # tests/test_symbols.py
  from xml.dom import minidom
  from brand.build import symbols as sym

  def _wrap(markup: str) -> str:
      return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{markup}</svg>'

  def test_helpers_emit_parseable_svg() -> None:
      for markup in (
          sym._ah(50, 50, 0.0, 6),
          sym._cyl(50, 50, 20),
          sym._star5(50, 50, 18, sym.GOLD),
          sym._circ_arc(50, 50, 20, 285, 425, 4.5),
      ):
          minidom.parseString(_wrap(markup))  # raises on malformed XML
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_symbols.py -q`
  Expected: FAIL — `ModuleNotFoundError`/`AttributeError` (symbols not defined).

- [ ] **Step 3: Implement the module + helpers**

  ```python
  # brand/build/symbols.py
  import math

  from brand.build.tokens import CREAM, GOLD_LIGHT

  GOLD = GOLD_LIGHT
  # pytest emblem bar tints (light->dark) — the one allowed non-token palette
  _BAR_TINTS = ("#e6b14d", "#d99a1f", GOLD, "#9c6c00")


  def _ah(tx: float, ty: float, ang: float, sz: float, fill: str = GOLD) -> str:
      """Simple isoceles arrowhead, tip at (tx,ty) pointing toward `ang` (radians)."""
      a1 = ang + math.radians(150)
      a2 = ang - math.radians(150)
      return (
          f'<polygon points="{tx:.1f},{ty:.1f} '
          f"{tx + sz * math.cos(a1):.1f},{ty + sz * math.sin(a1):.1f} "
          f'{tx + sz * math.cos(a2):.1f},{ty + sz * math.sin(a2):.1f}" fill="{fill}"/>'
      )


  def _cyl(cx: float, cy: float, r: float, h: float = 0.78, w: float = 1.0, fill: str = GOLD) -> str:
      """Database cylinder centred on (cx,cy)."""
      rx = 0.5 * r * w
      return (
          f'<ellipse cx="{cx}" cy="{cy - h / 2 * r:.1f}" rx="{rx:.1f}" ry="{0.16 * r:.1f}" fill="{fill}"/>'
          f'<rect x="{cx - rx:.1f}" y="{cy - h / 2 * r:.1f}" width="{2 * rx:.1f}" height="{h * r:.1f}" fill="{fill}"/>'
          f'<ellipse cx="{cx}" cy="{cy + h / 2 * r:.1f}" rx="{rx:.1f}" ry="{0.16 * r:.1f}" fill="{fill}"/>'
          f'<ellipse cx="{cx}" cy="{cy - h / 2 * r:.1f}" rx="{rx:.1f}" ry="{0.16 * r:.1f}" '
          f'fill="none" stroke="{CREAM}" stroke-width="0.8"/>'
      )


  def _star5(cx: float, cy: float, radius: float, color: str, inner: float = 0.42) -> str:
      """Five-pointed star centred on (cx,cy)."""
      pts: list[tuple[float, float]] = []
      for i in range(5):
          ao = -90 + i * 72
          pts.append((cx + radius * math.cos(math.radians(ao)), cy + radius * math.sin(math.radians(ao))))
          ai = ao + 36
          pts.append((cx + radius * inner * math.cos(math.radians(ai)), cy + radius * inner * math.sin(math.radians(ai))))
      body = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
      return f'<polygon points="{body}" fill="{color}"/>'


  def _circ_arc(cx: float, cy: float, rad: float, a0: float, a1: float, w: float) -> str:
      """Clockwise arc a0->a1 (deg, increasing) with a leading arrowhead at a1."""
      a1s = a1 - 7  # stop the stroke short so the head caps it cleanly
      x0 = cx + rad * math.cos(math.radians(a0))
      y0 = cy + rad * math.sin(math.radians(a0))
      x1 = cx + rad * math.cos(math.radians(a1s))
      y1 = cy + rad * math.sin(math.radians(a1s))
      large = 1 if (a1s - a0) % 360 > 180 else 0
      d = (
          f'<path d="M{x0:.1f} {y0:.1f} A {rad:.1f} {rad:.1f} 0 {large} 1 {x1:.1f} {y1:.1f}" '
          f'fill="none" stroke="{GOLD}" stroke-width="{w}" stroke-linecap="butt"/>'
      )
      ex = cx + rad * math.cos(math.radians(a1))
      ey = cy + rad * math.sin(math.radians(a1))
      ang = math.radians(a1 + 90)  # forward (clockwise) tangent
      length = w * 3.0
      width = w * 1.7
      dx, dy = math.cos(ang), math.sin(ang)
      px, py = -dy, dx
      tip = (ex + 0.55 * length * dx, ey + 0.55 * length * dy)
      base = (ex - 0.45 * length * dx, ey - 0.45 * length * dy)
      d += (
          f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} '
          f"{base[0] + width * px:.1f},{base[1] + width * py:.1f} "
          f'{base[0] - width * px:.1f},{base[1] - width * py:.1f}" fill="{GOLD}"/>'
      )
      return d
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `uv run pytest tests/test_symbols.py -q`
  Expected: PASS (1 test).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/symbols.py tests/test_symbols.py
  git commit -m "feat(brand): symbol module scaffold + shared helpers"
  ```

---

### Task 2: Dependency-injection symbols

**Files:**
- Modify: `brand/build/symbols.py`
- Test: `tests/test_symbols.py`

**Interfaces:**
- Produces (each `(cx,cy,r) -> str`): `graph(cx,cy,r,*,dashed)`,
  `bolt_disc(cx,cy,r)`, `star_disc(cx,cy,r)`, `faststream(cx,cy,r)`,
  `terminal(cx,cy,r)`, `bars(cx,cy,r)`, `chevron(cx,cy,r)`. Module constant
  `FASTSTREAM_PATH`.

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_symbols.py
  import pytest

  DI_SYMBOLS = ["bolt_disc", "star_disc", "faststream", "terminal", "bars", "chevron"]

  @pytest.mark.parametrize("name", DI_SYMBOLS)
  def test_di_symbol_parses(name: str) -> None:
      markup = getattr(sym, name)(50, 50, 23)
      minidom.parseString(_wrap(markup))

  def test_graph_dashed_vs_solid() -> None:
      assert "stroke-dasharray" in sym.graph(50, 50, 23, dashed=True)
      assert "stroke-dasharray" not in sym.graph(50, 50, 23, dashed=False)
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_symbols.py -q`
  Expected: FAIL — `AttributeError` on the new symbol names.

- [ ] **Step 3: Implement the DI symbols**

  ```python
  # append to brand/build/symbols.py
  FASTSTREAM_PATH = (
      "m499.61,356.87l-92.61-160.41-36.48-63.19-10.46,251.02c.07,2.86-.78,6.05-2.51,8.6"
      "-2.98,4.41-7.42,5.31-9.92,2.02l.02-.03-68.85-90.48-107.13,38.09v.04c-3.89,1.38-7.11"
      "-1.8-7.2-7.12-.05-3.08.97-6.22,2.6-8.57L327.1,58.07l-12.71-22.02c-25.95-44.94-90.82"
      "-44.94-116.77,0l-92.61,160.41L12.39,356.87c-25.95,44.94,6.49,101.12,58.38,101.12"
      "h370.45c51.9,0,84.33-56.18,58.38-101.12Z"
  )


  def bolt_disc(cx: float, cy: float, r: float) -> str:
      """FastAPI cue: lightning bolt knocked out of a gold disc."""
      norm = [(0.30, -0.80), (-0.42, 0.18), (0.05, 0.18), (-0.22, 0.82), (0.48, -0.22), (0.05, -0.22)]
      pts = " ".join(f"{cx + dx * r * 0.82:.1f},{cy + dy * r * 0.82:.1f}" for dx, dy in norm)
      return f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{GOLD}"/><polygon points="{pts}" fill="{CREAM}"/>'


  def star_disc(cx: float, cy: float, r: float) -> str:
      """Litestar cue: star knocked out of a gold disc."""
      return f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{GOLD}"/>' + _star5(cx, cy, r * 0.72, CREAM)


  def faststream(cx: float, cy: float, r: float) -> str:
      """FastStream's own delta/stream mark, recoloured gold (sized ~2r tall)."""
      size = r * 2.1
      sc = size / 462.0
      return (
          f'<g transform="translate({cx - 256 * sc:.1f},{cy - 231 * sc:.1f}) scale({sc:.4f})">'
          f'<path d="{FASTSTREAM_PATH}" fill="{GOLD}"/></g>'
      )


  def terminal(cx: float, cy: float, r: float) -> str:
      """Typer cue: terminal window showing a T> prompt."""
      return (
          f'<rect x="{cx - r:.1f}" y="{cy - r * 0.72:.1f}" width="{2 * r:.1f}" height="{r * 1.44:.1f}" '
          f'rx="{r * 0.2:.1f}" fill="{GOLD}"/>'
          f'<text x="{cx - r * 0.58:.1f}" y="{cy + r * 0.42:.1f}" '
          f'font-family="ui-monospace,Menlo,monospace" font-size="{r * 0.98:.1f}" '
          f'font-weight="700" fill="{CREAM}">T&gt;</text>'
      )


  def bars(cx: float, cy: float, r: float) -> str:
      """pytest cue: stepped bars hanging from a crossbar (gold tints), vertically centred."""
      bw = r * 0.34
      gap = r * 0.22
      x0 = cx - r
      stub = r * 0.18
      cb = r * 0.2
      maxlen = r * 1.0
      total = stub + r * 0.12 + cb + maxlen
      top = cy - total / 2
      y_stub = top
      y_cb = top + stub + r * 0.12
      y_bar = y_cb + cb
      heights = [1.0, 0.78, 0.55, 0.38]
      out = [f'<rect x="{x0:.1f}" y="{y_cb:.1f}" width="{2 * r:.1f}" height="{cb:.1f}" rx="{cb / 2:.1f}" fill="{GOLD}"/>']
      for i in range(4):
          x = x0 + i * (bw + gap)
          out.append(f'<rect x="{x:.1f}" y="{y_stub:.1f}" width="{bw:.1f}" height="{stub:.1f}" fill="{_BAR_TINTS[i]}"/>')
          out.append(f'<rect x="{x:.1f}" y="{y_bar:.1f}" width="{bw:.1f}" height="{r * heights[i]:.1f}" rx="1" fill="{_BAR_TINTS[i]}"/>')
      return "".join(out)


  def chevron(cx: float, cy: float, r: float) -> str:
      """The org chevron (used by templates and as a standalone cue)."""
      return (
          f'<polyline points="{cx - r * 0.45:.1f},{cy - r:.1f} {cx + r * 0.7:.1f},{cy:.1f} '
          f'{cx - r * 0.45:.1f},{cy + r:.1f}" fill="none" stroke="{GOLD}" '
          f'stroke-width="{r * 0.5:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
      )


  def graph(cx: float, cy: float, r: float, *, dashed: bool) -> str:
      """Dependency graph: 3 nodes + two edges. dashed=auto-wired (modern-di),
      solid=explicit (that-depends)."""
      top = (cx, cy - 0.62 * r)
      bl = (cx - 0.82 * r, cy + 0.6 * r)
      br = (cx + 0.82 * r, cy + 0.6 * r)
      nr = r * 0.24
      w = r * 0.15
      da = ' stroke-dasharray="4 3"' if dashed else ""
      return (
          f'<line x1="{top[0]:.1f}" y1="{top[1]:.1f}" x2="{bl[0]:.1f}" y2="{bl[1]:.1f}" stroke="{GOLD}" stroke-width="{w:.1f}"{da}/>'
          f'<line x1="{top[0]:.1f}" y1="{top[1]:.1f}" x2="{br[0]:.1f}" y2="{br[1]:.1f}" stroke="{GOLD}" stroke-width="{w:.1f}"{da}/>'
          f'<circle cx="{top[0]:.1f}" cy="{top[1]:.1f}" r="{nr:.1f}" fill="{GOLD}"/>'
          f'<circle cx="{bl[0]:.1f}" cy="{bl[1]:.1f}" r="{nr:.1f}" fill="{GOLD}"/>'
          f'<circle cx="{br[0]:.1f}" cy="{br[1]:.1f}" r="{nr:.1f}" fill="{GOLD}"/>'
      )
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `uv run pytest tests/test_symbols.py -q`
  Expected: PASS (helpers + 6 parametrized DI symbols + graph test).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/symbols.py tests/test_symbols.py
  git commit -m "feat(brand): dependency-injection inner symbols"
  ```

---

### Task 3: Microservices/messaging symbols

**Files:**
- Modify: `brand/build/symbols.py`
- Test: `tests/test_symbols.py`

**Interfaces:**
- Produces (each `(cx,cy,r) -> str`): `rocket`, `chain`, `stopwatch`,
  `lanes`, `outbox`.

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_symbols.py
  MSG_SYMBOLS = ["rocket", "chain", "stopwatch", "lanes", "outbox"]

  @pytest.mark.parametrize("name", MSG_SYMBOLS)
  def test_msg_symbol_parses(name: str) -> None:
      minidom.parseString(_wrap(getattr(sym, name)(50, 50, 23)))
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_symbols.py -q`
  Expected: FAIL — `AttributeError` on the new names.

- [ ] **Step 3: Implement the messaging symbols**

  ```python
  # append to brand/build/symbols.py
  def rocket(cx: float, cy: float, r: float) -> str:
      """lite-bootstrap: a rocket (launch)."""
      body = (
          f'<path d="M{cx} {cy - r} Q{cx + 0.42 * r} {cy - 0.45 * r} {cx + 0.4 * r} {cy + 0.05 * r} '
          f'L{cx + 0.36 * r} {cy + 0.42 * r} L{cx - 0.36 * r} {cy + 0.42 * r} '
          f'L{cx - 0.4 * r} {cy + 0.05 * r} Q{cx - 0.42 * r} {cy - 0.45 * r} {cx} {cy - r} Z" fill="{GOLD}"/>'
      )
      fins = (
          f'<polygon points="{cx - 0.36 * r:.1f},{cy + 0.12 * r:.1f} {cx - 0.72 * r:.1f},{cy + 0.5 * r:.1f} {cx - 0.36 * r:.1f},{cy + 0.42 * r:.1f}" fill="{GOLD}"/>'
          f'<polygon points="{cx + 0.36 * r:.1f},{cy + 0.12 * r:.1f} {cx + 0.72 * r:.1f},{cy + 0.5 * r:.1f} {cx + 0.36 * r:.1f},{cy + 0.42 * r:.1f}" fill="{GOLD}"/>'
      )
      window = f'<circle cx="{cx}" cy="{cy - 0.28 * r:.1f}" r="{0.16 * r:.1f}" fill="{CREAM}"/>'
      flame = f'<polygon points="{cx - 0.18 * r:.1f},{cy + 0.42 * r:.1f} {cx + 0.18 * r:.1f},{cy + 0.42 * r:.1f} {cx:.1f},{cy + 0.8 * r:.1f}" fill="{GOLD}"/>'
      return body + fins + window + flame


  def chain(cx: float, cy: float, r: float) -> str:
      """httpware: two interlocked chain links (middleware chain)."""
      sw = r * 0.2
      return (
          f'<rect x="{cx - 0.85 * r:.1f}" y="{cy - 0.3 * r:.1f}" width="{0.9 * r:.1f}" height="{0.6 * r:.1f}" rx="{0.3 * r:.1f}" fill="none" stroke="{GOLD}" stroke-width="{sw:.1f}"/>'
          f'<rect x="{cx - 0.05 * r:.1f}" y="{cy - 0.3 * r:.1f}" width="{0.9 * r:.1f}" height="{0.6 * r:.1f}" rx="{0.3 * r:.1f}" fill="none" stroke="{GOLD}" stroke-width="{sw:.1f}"/>'
      )


  def stopwatch(cx: float, cy: float, r: float) -> str:
      """faststream-redis-timers: a stopwatch."""
      c = cy + 0.07 * r
      rr = r * 0.92
      face = (
          f'<circle cx="{cx}" cy="{c:.1f}" r="{0.9 * rr:.1f}" fill="none" stroke="{GOLD}" stroke-width="{rr * 0.16:.1f}"/>'
          f'<line x1="{cx}" y1="{c:.1f}" x2="{cx}" y2="{c - 0.55 * rr:.1f}" stroke="{GOLD}" stroke-width="{rr * 0.15:.1f}" stroke-linecap="round"/>'
          f'<line x1="{cx}" y1="{c:.1f}" x2="{cx + 0.42 * rr:.1f}" y2="{c + 0.18 * rr:.1f}" stroke="{GOLD}" stroke-width="{rr * 0.15:.1f}" stroke-linecap="round"/>'
      )
      btn = (
          f'<rect x="{cx - 0.13 * r:.1f}" y="{cy - 1.18 * r:.1f}" width="{0.26 * r:.1f}" height="{0.2 * r:.1f}" rx="2" fill="{GOLD}"/>'
          f'<line x1="{cx}" y1="{cy - 1.0 * r:.1f}" x2="{cx}" y2="{cy - 0.85 * r:.1f}" stroke="{GOLD}" stroke-width="{r * 0.14:.1f}"/>'
      )
      return face + btn


  def lanes(cx: float, cy: float, r: float, length: float = 1.7) -> str:
      """faststream-concurrent-aiokafka: three staggered parallel arrows (middle longest)."""
      out = ""
      for i, dy in enumerate((-0.55 * r, 0.0, 0.55 * r)):
          ln = length * r * (0.72 if i != 1 else 1.0)
          x1 = cx - length * r / 2
          x2 = x1 + ln
          out += (
              f'<line x1="{x1:.1f}" y1="{cy + dy:.1f}" x2="{x2 - 0.18 * r:.1f}" y2="{cy + dy:.1f}" '
              f'stroke="{GOLD}" stroke-width="{r * 0.15:.1f}" stroke-linecap="round"/>'
          )
          out += _ah(x2, cy + dy, 0.0, r * 0.3)
      return out


  def outbox(cx: float, cy: float, r: float) -> str:
      """faststream-outbox: a database cylinder publishing concentric broadcast arcs."""
      base = _cyl(cx - 0.28 * r, cy + 0.28 * r, r * 0.72, 0.72)
      bx, by = cx, cy - 0.02 * r
      out = f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{0.13 * r:.1f}" fill="{GOLD}"/>'
      for k in (0.5, 0.82, 1.14):
          kk = k * r * 0.72
          out += (
              f'<path d="M{bx + kk:.1f} {by:.1f} A {kk:.1f} {kk:.1f} 0 0 0 {bx:.1f} {by - kk:.1f}" '
              f'fill="none" stroke="{GOLD}" stroke-width="{r * 0.72 * 0.14:.1f}"/>'
          )
      return base + out
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `uv run pytest tests/test_symbols.py -q`
  Expected: PASS (5 new parametrized cases).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/symbols.py tests/test_symbols.py
  git commit -m "feat(brand): microservices/messaging inner symbols"
  ```

---

### Task 4: Utility symbols

**Files:**
- Modify: `brand/build/symbols.py`
- Test: `tests/test_symbols.py`

**Interfaces:**
- Produces (each `(cx,cy,r) -> str`): `db_retry`, `eof_fixer`, `tag`.

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_symbols.py
  UTIL_SYMBOLS = ["db_retry", "eof_fixer", "tag"]

  @pytest.mark.parametrize("name", UTIL_SYMBOLS)
  def test_util_symbol_parses(name: str) -> None:
      minidom.parseString(_wrap(getattr(sym, name)(50, 50, 23)))
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_symbols.py -q`
  Expected: FAIL — `AttributeError`.

- [ ] **Step 3: Implement the utility symbols**

  ```python
  # append to brand/build/symbols.py
  def db_retry(cx: float, cy: float, r: float) -> str:
      """db-retry: a database cylinder inside a two-head clockwise retry circle."""
      rad = 0.92 * r
      return _cyl(cx, cy, r * 0.6) + _circ_arc(cx, cy, rad, 285, 425, 4.5) + _circ_arc(cx, cy, rad, 105, 245, 4.5)


  def eof_fixer(cx: float, cy: float, r: float) -> str:
      """eof-fixer: a document with a newline-return (down-then-left) arrow."""
      doc = (
          f'<rect x="{cx - 0.6 * r:.1f}" y="{cy - 0.8 * r:.1f}" width="{1.2 * r:.1f}" height="{1.6 * r:.1f}" '
          f'rx="3" fill="none" stroke="{GOLD}" stroke-width="{r * 0.12:.1f}"/>'
      )
      for i in range(3):
          doc += (
              f'<line x1="{cx - 0.4 * r:.1f}" y1="{cy - 0.5 * r + i * 0.32 * r:.1f}" '
              f'x2="{cx + 0.4 * r:.1f}" y2="{cy - 0.5 * r + i * 0.32 * r:.1f}" stroke="{GOLD}" stroke-width="{r * 0.1:.1f}"/>'
          )
      doc += (
          f'<line x1="{cx - 0.2 * r:.1f}" y1="{cy + 0.55 * r:.1f}" x2="{cx + 0.45 * r:.1f}" y2="{cy + 0.55 * r:.1f}" '
          f'stroke="{GOLD}" stroke-width="{r * 0.1:.1f}"/>'
      )
      doc += _ah(cx - 0.2 * r, cy + 0.55 * r, math.pi, r * 0.24)
      return doc


  def tag(cx: float, cy: float, r: float) -> str:
      """semvertag: a price/version tag with a punch-hole, vertically centred."""
      return (
          f'<path d="M{cx - 0.2 * r:.1f} {cy - 0.48 * r:.1f} L{cx + 0.75 * r:.1f} {cy - 0.48 * r:.1f} '
          f'L{cx + 0.75 * r:.1f} {cy + 0.48 * r:.1f} L{cx - 0.2 * r:.1f} {cy + 0.48 * r:.1f} '
          f'L{cx - 0.75 * r:.1f} {cy:.1f} Z" fill="{GOLD}"/>'
          f'<circle cx="{cx - 0.28 * r:.1f}" cy="{cy:.1f}" r="{0.13 * r:.1f}" fill="{CREAM}"/>'
      )
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `uv run pytest tests/test_symbols.py -q`
  Expected: PASS.

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/symbols.py tests/test_symbols.py
  git commit -m "feat(brand): utility inner symbols"
  ```

---

### Task 5: Parametric project frame

**Files:**
- Modify: `brand/build/geometry.py`
- Test: `tests/test_projects.py`

**Interfaces:**
- Produces: `project_frame(*, struct: str, accent: str, w: int = 100, h: int = 100,
  m: int = 9, lx: int = 53, ly: int = 53, s: int = 11) -> str` — bare frame markup
  (no `<svg>` wrapper), two pinwheeled L-snakes.

- [ ] **Step 1: Write the failing test**

  ```python
  # tests/test_projects.py
  from xml.dom import minidom
  from brand.build import geometry as g
  from brand.build import tokens as t

  def test_project_frame_parses_and_uses_tokens() -> None:
      frame = g.project_frame(struct=t.GREEN_INK, accent=t.GOLD_LIGHT)
      minidom.parseString(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{frame}</svg>')
      assert t.GREEN_INK in frame and t.GOLD_LIGHT in frame
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: FAIL — `AttributeError: module ... has no attribute 'project_frame'`.

- [ ] **Step 3: Implement `project_frame`**

  ```python
  # append to brand/build/geometry.py
  def project_frame(
      *,
      struct: str,
      accent: str,
      w: int = 100,
      h: int = 100,
      m: int = 9,
      lx: int = 53,
      ly: int = 53,
      s: int = 11,
  ) -> str:
      """Two pinwheeled L-snakes in opposite corners — the constant project frame.
      Returns bare markup (no <svg> wrapper)."""
      hs = s + 3
      parts = [
          f'<path d="M{m} {m + ly} L{m} {m} L{m + lx} {m}" fill="none" stroke="{struct}" stroke-width="{s}" stroke-linejoin="miter"/>',
          f'<rect x="{m + lx - hs / 2:.1f}" y="{m - hs / 2:.1f}" width="{hs}" height="{hs}" rx="2" fill="{struct}"/>',
          f'<polygon points="{m - s / 2:.1f},{m + ly - 2:.1f} {m + s / 2:.1f},{m + ly - 2:.1f} {m + s / 2:.1f},{m + ly:.1f} {m - s / 2:.1f},{m + ly + s:.1f}" fill="{struct}"/>',
          f'<path d="M{w - m} {h - m - ly} L{w - m} {h - m} L{w - m - lx} {h - m}" fill="none" stroke="{accent}" stroke-width="{s}" stroke-linejoin="miter"/>',
          f'<rect x="{w - m - lx - hs / 2:.1f}" y="{h - m - hs / 2:.1f}" width="{hs}" height="{hs}" rx="2" fill="{accent}"/>',
          f'<polygon points="{w - m + s / 2:.1f},{h - m - ly + 2:.1f} {w - m - s / 2:.1f},{h - m - ly + 2:.1f} {w - m - s / 2:.1f},{h - m - ly:.1f} {w - m + s / 2:.1f},{h - m - ly - s:.1f}" fill="{accent}"/>',
      ]
      return "".join(parts)
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: PASS.

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/geometry.py tests/test_projects.py
  git commit -m "feat(brand): parametric project snake-frame"
  ```

---

### Task 6: Repo manifest + mark composition

**Files:**
- Create: `brand/build/projects.py`
- Test: `tests/test_projects.py`

**Interfaces:**
- Consumes: `geometry.project_frame`, all `symbols.*` functions, `tokens.*`.
- Produces: `MANIFEST: dict[str, Callable[[], str]]` (17 repos → inner-symbol
  thunks at `R=23`), `project_mark(repo: str) -> str` (full `<svg>`),
  `ALLOWED_COLORS: frozenset[str]`.

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_projects.py
  import re
  import pytest
  from brand.build import projects as p

  EXPECTED_REPOS = {
      "modern-di", "that-depends", "modern-di-fastapi", "modern-di-litestar",
      "modern-di-faststream", "modern-di-typer", "modern-di-pytest",
      "fastapi-sqlalchemy-template", "litestar-sqlalchemy-template",
      "lite-bootstrap", "httpware", "faststream-redis-timers",
      "faststream-concurrent-aiokafka", "faststream-outbox",
      "db-retry", "eof-fixer", "semvertag",
  }

  def test_manifest_covers_every_repo() -> None:
      assert set(p.MANIFEST) == EXPECTED_REPOS

  @pytest.mark.parametrize("repo", sorted(EXPECTED_REPOS))
  def test_project_mark_is_valid_svg(repo: str) -> None:
      svg = p.project_mark(repo)
      minidom.parseString(svg)
      assert svg.startswith("<svg") and 'viewBox="0 0 100 100"' in svg

  @pytest.mark.parametrize("repo", sorted(EXPECTED_REPOS))
  def test_only_allowed_colours(repo: str) -> None:
      hexes = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}", p.project_mark(repo))}
      assert hexes <= p.ALLOWED_COLORS, f"{repo} stray colours: {hexes - p.ALLOWED_COLORS}"

  def test_templates_use_chevron() -> None:
      # both templates share the org chevron (a polyline), not a bespoke symbol
      for repo in ("fastapi-sqlalchemy-template", "litestar-sqlalchemy-template"):
          assert "<polyline" in p.project_mark(repo)
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: FAIL — `ModuleNotFoundError: brand.build.projects`.

- [ ] **Step 3: Implement `projects.py`**

  ```python
  # brand/build/projects.py
  from collections.abc import Callable

  from brand.build import geometry as g
  from brand.build import symbols as sym
  from brand.build import tokens as t

  R = 23
  _CX = _CY = 50

  ALLOWED_COLORS: frozenset[str] = frozenset(
      c.lower() for c in (t.GREEN_INK, t.GOLD_LIGHT, t.CREAM, *sym._BAR_TINTS)
  )

  MANIFEST: dict[str, Callable[[], str]] = {
      # dependency injection
      "modern-di": lambda: sym.graph(_CX, _CY, R, dashed=True),
      "that-depends": lambda: sym.graph(_CX, _CY, R, dashed=False),
      "modern-di-fastapi": lambda: sym.bolt_disc(_CX, _CY, R),
      "modern-di-litestar": lambda: sym.star_disc(_CX, _CY, R),
      "modern-di-faststream": lambda: sym.faststream(_CX, _CY, R),
      "modern-di-typer": lambda: sym.terminal(_CX, _CY, R),
      "modern-di-pytest": lambda: sym.bars(_CX, _CY, R),
      # templates — reuse the org chevron
      "fastapi-sqlalchemy-template": lambda: sym.chevron(_CX, _CY, R - 1),
      "litestar-sqlalchemy-template": lambda: sym.chevron(_CX, _CY, R - 1),
      # microservices, http & messaging
      "lite-bootstrap": lambda: sym.rocket(_CX, _CY, R),
      "httpware": lambda: sym.chain(_CX, _CY, R),
      "faststream-redis-timers": lambda: sym.stopwatch(_CX, _CY, R),
      "faststream-concurrent-aiokafka": lambda: sym.lanes(_CX, _CY, R),
      "faststream-outbox": lambda: sym.outbox(_CX, _CY, R),
      # utilities
      "db-retry": lambda: sym.db_retry(_CX, _CY, R),
      "eof-fixer": lambda: sym.eof_fixer(_CX, _CY, R),
      "semvertag": lambda: sym.tag(_CX, _CY, R),
  }


  def project_mark(repo: str) -> str:
      """Full <svg> for a repo: constant frame + its gold inner symbol."""
      frame = g.project_frame(struct=t.GREEN_INK, accent=t.GOLD_LIGHT)
      inner = MANIFEST[repo]()
      return (
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
          f'role="img" aria-label="{repo}">{frame}{inner}</svg>'
      )
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: PASS (manifest coverage + 17 valid-SVG + 17 colour + templates).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/projects.py tests/test_projects.py
  git commit -m "feat(brand): repo manifest + project mark composition"
  ```

---

### Task 7: Render marks to `brand/projects/<repo>/`

**Files:**
- Create: `brand/build/raster.py`
- Modify: `brand/build/render.py`
- Modify: `brand/build/projects.py`
- Test: `tests/test_projects.py`

**Interfaces:**
- Produces: `raster.export_png(svg_path, png_path, *, width=None, height=None) -> bool`
  (moved verbatim from `render.py`); `projects.render_projects(out_dir: Path | None = None) -> list[Path]`
  — writes `mark.svg` (+ `mark-512.png`, `mark-1024.png`) per repo, returns the
  written `mark.svg` paths.

Why `raster.py`: `projects` needs `export_png` and `render` needs
`render_projects`. Putting `export_png` in a third module both import keeps every
import at module level with no cycle (`render → projects → raster`, `render → raster`).

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_projects.py
  from pathlib import Path

  def test_render_projects_writes_every_mark(tmp_path: Path) -> None:
      written = p.render_projects(out_dir=tmp_path)
      assert len(written) == len(EXPECTED_REPOS)
      for repo in EXPECTED_REPOS:
          svg = tmp_path / repo / "mark.svg"
          assert svg.is_file() and svg.read_text(encoding="utf-8").startswith("<svg")
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_projects.py::test_render_projects_writes_every_mark -q`
  Expected: FAIL — `AttributeError: ... 'render_projects'`.

- [ ] **Step 3a: Extract `export_png` into `brand/build/raster.py`**

  Move the existing `export_png` function out of `render.py` verbatim:

  ```python
  # brand/build/raster.py
  import shutil
  import subprocess
  from pathlib import Path


  def export_png(
      svg_path: Path,
      png_path: Path,
      *,
      width: int | None = None,
      height: int | None = None,
  ) -> bool:
      exe = shutil.which("rsvg-convert")
      if exe is None:
          return False
      args = [exe]
      if width is not None:
          args += ["-w", str(width)]
      if height is not None:
          args += ["-h", str(height)]
      args += [str(svg_path), "-o", str(png_path)]
      subprocess.run(args, check=True)
      return True
  ```

  Then in `render.py`: delete its local `export_png` def and `shutil`/`subprocess`
  imports, and add at the top (module level):

  ```python
  from brand.build.projects import render_projects
  from brand.build.raster import export_png
  ```

- [ ] **Step 3b: Implement `render_projects` and call it from `render()`**

  ```python
  # in brand/build/projects.py — add to the top-level imports:
  from pathlib import Path

  from brand.build.raster import export_png

  # ... after project_mark(); module-level constants then the function:
  ROOT = Path(__file__).resolve().parents[2]
  PROJECTS = ROOT / "brand" / "projects"
  _PNG_SIZES = (512, 1024)


  def render_projects(out_dir: Path | None = None) -> list[Path]:
      """Write mark.svg (+ PNGs) for every repo under out_dir/<repo>/."""
      base = out_dir if out_dir is not None else PROJECTS
      written: list[Path] = []
      for repo in MANIFEST:
          d = base / repo
          d.mkdir(parents=True, exist_ok=True)
          svg = d / "mark.svg"
          svg.write_text(project_mark(repo) + "\n", encoding="utf-8")
          for sz in _PNG_SIZES:
              export_png(svg, d / f"mark-{sz}.png", width=sz, height=sz)
          written.append(svg)
      return written
  ```

  ```python
  # in brand/build/render.py, inside render() after the org marks block:
      # Per-project marks (brand/projects/<repo>/).
      render_projects()
  ```

- [ ] **Step 4: Run the test + full render**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: PASS.
  Run: `uv run python -m brand.build.render`
  Expected: no error; org marks still written to `brand/org/`; `ls brand/projects/`
  shows all 17 repo folders, each with `mark.svg` (+ PNGs if `rsvg-convert` present).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/raster.py brand/build/render.py brand/build/projects.py tests/test_projects.py brand/projects
  git commit -m "feat(brand): render per-project marks to brand/projects/"
  ```

---

### Task 8: Horizontal name lockup per repo

**Files:**
- Modify: `brand/build/projects.py`
- Test: `tests/test_projects.py`

**Interfaces:**
- Consumes: `text.outline_text`, `project_mark` internals.
- Produces: `project_lockup(repo: str) -> str` (mark at left + repo name in Jost
  to its right); `render_projects` also writes `lockup.svg` per repo.

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_projects.py
  @pytest.mark.parametrize("repo", ["modern-di", "faststream-outbox", "semvertag"])
  def test_lockup_is_valid_and_names_repo(repo: str) -> None:
      svg = p.project_lockup(repo)
      minidom.parseString(svg)
      assert svg.startswith("<svg")

  def test_render_projects_writes_lockup(tmp_path: Path) -> None:
      p.render_projects(out_dir=tmp_path)
      assert (tmp_path / "modern-di" / "lockup.svg").is_file()
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_projects.py -q -k lockup`
  Expected: FAIL — `AttributeError: ... 'project_lockup'`.

- [ ] **Step 3: Implement `project_lockup` and write it in `render_projects`**

  ```python
  # add near the top imports of brand/build/projects.py
  from brand.build.text import outline_text

  # add to brand/build/projects.py
  _LOCKUP_H = 100
  _NAME_SIZE = 34
  _GAP = 18


  def project_lockup(repo: str) -> str:
      """Framed mark on the left + the repo name in Jost (green) to its right."""
      mark_frame = g.project_frame(struct=t.GREEN_INK, accent=t.GOLD_LIGHT)
      inner = MANIFEST[repo]()
      name_x = _LOCKUP_H + _GAP
      name_svg, name_w = outline_text(
          repo, _NAME_SIZE, x=name_x, baseline_y=_LOCKUP_H / 2 + _NAME_SIZE * 0.34,
          anchor="start", color=t.GREEN_INK,
      )
      total_w = round(name_x + name_w + _GAP)
      return (
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {_LOCKUP_H}" '
          f'role="img" aria-label="{repo}">'
          f'<g>{mark_frame}{inner}</g>'
          f"{name_svg}</svg>"
      )
  ```

  ```python
  # in render_projects(), inside the for-loop after writing mark.svg:
          (d / "lockup.svg").write_text(project_lockup(repo) + "\n", encoding="utf-8")
  ```

- [ ] **Step 4: Run the tests + render**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: PASS.
  Run: `uv run python -m brand.build.render` then `ls brand/projects/modern-di/`
  Expected: `mark.svg`, `lockup.svg` (+ PNGs) present.

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/projects.py tests/test_projects.py brand/projects
  git commit -m "feat(brand): per-project horizontal name lockups"
  ```

---

### Task 9: Docs — README + architecture + finalize bundle

**Files:**
- Modify: `brand/README.md`
- Create: `architecture/brand-marks.md`
- Modify: `planning/changes/2026-06-29.01-per-project-brand-marks/design.md` (summary)

One sentence: document the shipped capability and promote it into
`architecture/`, per the planning convention.

- [ ] **Step 1: Update `brand/README.md`**

  Replace the "Deferred" section's first line so per-project marks are no longer
  listed as deferred; add a short subsection:

  ```markdown
  ## Per-project marks (`brand/projects/`)

  Each repo gets a large-format mark: the constant green+gold snake-frame with
  one gold inner symbol (see `brand/build/projects.py::MANIFEST`). Regenerate
  with `uv run python -m brand.build.render`; outputs land in
  `brand/projects/<repo>/` as `mark.svg`, `lockup.svg` (+ PNGs). These are
  large-format only — every repo's favicon/avatar stays the org mark.
  ```

- [ ] **Step 2: Create `architecture/brand-marks.md`**

  ```markdown
  # Brand marks

  The org's logo assets, generated by `brand/build/` (no frontmatter; living prose).

  ## Org marks (`brand/org/`)
  Favicon, avatar, social cards — the interlocked-snakes pinwheel with a chevron.
  Used everywhere small (favicons, avatars). See `site-branding.md` for site wiring.

  ## Per-project marks (`brand/projects/<repo>/`)
  One large-format logo per repo: the constant green+gold snake-frame
  (`geometry.py::project_frame`, margin 9 / arm 53 / stroke 11) with a single
  gold inner symbol (`symbols.py`) chosen per repo in `projects.py::MANIFEST`.
  Two-colour (green + gold); repos differ by symbol shape, not colour. The two
  project templates reuse the org chevron. `modern-di-faststream` is the only
  mark using a partner's literal logo path (FastStream's, recoloured); other
  integration cues are redrawn evocations. Outputs: `mark.svg`, `lockup.svg`
  (+ `mark-512/1024.png`). Regenerate via `uv run python -m brand.build.render`.
  ```

- [ ] **Step 3: Finalize the bundle summary**

  Edit the `summary:` in `design.md` to the realized result, e.g.:
  `summary: Per-project marks shipped — 17 repos, constant snake-frame + gold inner symbol, generated into brand/projects/.`

- [ ] **Step 4: Verify everything**

  Run: `uv run pytest -q` (full suite) → all green.
  Run: `just check-planning` → `planning: OK`.
  Run: `uv run python -m brand.build.render` → no error.

- [ ] **Step 5: Commit**

  ```bash
  git add brand/README.md architecture/brand-marks.md planning/changes/2026-06-29.01-per-project-brand-marks/design.md
  git commit -m "docs(brand): document per-project marks + promote to architecture"
  ```

---

## Notes for the executor

- After all tasks: push the branch and open a PR (do not local-merge); watch CI.
- The validated visual prototype lives only in the brainstorm scratchpad; this
  plan is the source of truth. If a rendered mark looks off, render a contact
  sheet (`rsvg-convert` each `mark.svg` to PNG) and compare — the geometry here
  is the version that passed visual review.
- Do not alter `brand/org/` (output) or the org-mark `render()` blocks; only
  move `export_png` to `raster.py` and add the per-project pass.
- `terminal()` uses a live `<svg><text>` "T>" (generic monospace). Unlike the
  org wordmark (outlined via `text.py` for font-independence), this is a tiny
  glyph and renders fine with `rsvg-convert`'s default fonts. If a downstream
  context needs font-independence, swap it to `text.outline_text` with Jost.
