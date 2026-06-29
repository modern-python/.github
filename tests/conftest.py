import xml.etree.ElementTree as ET
import pytest


@pytest.fixture
def parse_svg():
    def _parse(svg: str) -> ET.Element:
        return ET.fromstring(svg)  # raises on malformed XML

    return _parse
