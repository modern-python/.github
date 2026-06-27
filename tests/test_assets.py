import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ORG = Path("brand/org")


def test_render_writes_valid_org_assets():
    subprocess.run([sys.executable, "-m", "brand.build.render"], check=True)
    for name in ("icon", "favicon", "horizontal", "stacked", "social"):
        p = ORG / f"{name}.svg"
        assert p.exists(), p
        ET.parse(p)  # well-formed
