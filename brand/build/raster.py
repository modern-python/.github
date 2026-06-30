import shutil
import subprocess
from pathlib import Path

_PNG_COLORS = 32  # palette size; flat art needs few (8 already looked clean; 32 = headroom)


def _quantize_png(path: Path, colors: int = _PNG_COLORS) -> None:
    """Re-save a PNG as an indexed-palette image — visually lossless for flat
    art. FASTOCTREE preserves alpha, so it is correct for both the opaque
    social cards and the transparent marks. No-op if Pillow is unavailable."""
    try:
        from PIL import Image
    except ModuleNotFoundError:
        return
    im = Image.open(path).convert("RGBA")
    q = im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE)
    q.save(path, format="PNG", optimize=True)


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
    _quantize_png(png_path)
    return True
