import hashlib
import shutil
import subprocess
from pathlib import Path

try:
    from PIL import Image, PngImagePlugin
except ModuleNotFoundError:
    Image = PngImagePlugin = None

_PNG_COLORS = 32  # palette size; flat art needs few (8 already looked clean; 32 = headroom)
_SOURCE_KEY = "source-sha256"


def _source_hash(svg_path: Path, width: int | None, height: int | None) -> str:
    h = hashlib.sha256(svg_path.read_bytes())
    h.update(f"|{width}|{height}|{_PNG_COLORS}".encode())
    return h.hexdigest()


def _stored_hash(png_path: Path) -> str | None:
    if Image is None or not png_path.is_file():
        return None
    with Image.open(png_path) as im:
        return im.info.get(_SOURCE_KEY)


def _quantize_png(path: Path, source_hash: str, colors: int = _PNG_COLORS) -> None:
    """Re-save a PNG as an indexed-palette image — visually lossless for flat
    art. FASTOCTREE preserves alpha, so it is correct for both the opaque
    social cards and the transparent marks. No-op if Pillow is unavailable."""
    if Image is None:
        return
    im = Image.open(path).convert("RGBA")
    q = im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE)
    info = PngImagePlugin.PngInfo()
    info.add_text(_SOURCE_KEY, source_hash)
    q.save(path, format="PNG", optimize=True, pnginfo=info)


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
    source_hash = _source_hash(svg_path, width, height)
    if _stored_hash(png_path) == source_hash:
        return True
    args = [exe]
    if width is not None:
        args += ["-w", str(width)]
    if height is not None:
        args += ["-h", str(height)]
    args += [str(svg_path), "-o", str(png_path)]
    subprocess.run(args, check=True)
    _quantize_png(png_path, source_hash)
    return True
