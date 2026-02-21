import os
import pytest
from src.parsers.svg_parser import SVGParser

def create_svg(filepath: str, content: str):
    with open(filepath, 'w') as f:
        f.write(content)

@pytest.fixture
def parser_env(tmp_path):
    """Fixture to provide a clean temporary directory for testing."""
    return tmp_path

def test_parser_detects_cut_mark_raster(parser_env):
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <!-- Red Cut -->
    <rect x="10" y="10" width="20" height="20" stroke="#FF0000" fill="none" />
    
    <!-- Green Mark -->
    <circle cx="50" cy="50" r="10" stroke="#00FF00" fill="none" />
    
    <!-- Blue Raster -->
    <polygon points="70,10 90,10 80,30" stroke="none" fill="#0000FF" />
    
    <!-- Ignored shape (Black) -->
    <line x1="0" y1="0" x2="100" y2="100" stroke="#000000" />
    
    <!-- Invalid Element (Text, but not converted to path for now) -->
    <text x="10" y="90" fill="#FF0000">Cut Me</text>
</svg>
    """
    svg_file = os.path.join(parser_env, "test.svg")
    create_svg(svg_file, svg_content)
    
    parser = SVGParser(svg_file)
    entities = parser.parse()
    
    assert len(entities) == 3
    
    # Verify exact contents
    cut_entities = [e for e in entities if e.process_type == 'cut']
    assert len(cut_entities) == 1
    assert cut_entities[0].color_hex == '#FF0000'
    
    mark_entities = [e for e in entities if e.process_type == 'mark']
    assert len(mark_entities) == 1
    assert mark_entities[0].color_hex == '#00FF00'
    
    raster_entities = [e for e in entities if e.process_type == 'raster']
    assert len(raster_entities) == 1
    assert raster_entities[0].color_hex == '#0000FF'
