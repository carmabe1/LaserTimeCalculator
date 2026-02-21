import pytest
from svgelements import Path
from src.parsers.svg_parser import LaserEntity
from src.engine.calculator import LaserTimeCalculator

@pytest.fixture
def calculator():
    return LaserTimeCalculator(
        cut_speed=10.0,
        vector_engrave_speed=50.0,
        raster_engrave_speed=100.0,
        transit_speed=200.0,
        scan_gap=0.1,
        overscan_factor=0.1
    )

def test_calculate_cut_time(calculator):
    # 100x100 square (Perimeter = 400)
    path = Path("M 0 0 L 100 0 L 100 100 L 0 100 Z")
    entity = LaserEntity(path=path, color_hex='#FF0000', process_type='cut')
    
    # Time = 400 / 10 = 40 seconds
    time = calculator.calculate_entity_time(entity)
    assert time == pytest.approx(40.0, 0.1)

def test_calculate_mark_time(calculator):
    # 100x100 square (Perimeter = 400)
    path = Path("M 0 0 L 100 0 L 100 100 L 0 100 Z")
    entity = LaserEntity(path=path, color_hex='#00FF00', process_type='mark')
    
    # Time = 400 / 50 = 8 seconds
    time = calculator.calculate_entity_time(entity)
    assert time == pytest.approx(8.0, 0.1)

def test_calculate_raster_time(calculator):
    # 100x50 rectangle (Width=100, Height=50)
    path = Path("M 0 0 L 100 0 L 100 50 L 0 50 Z")
    entity = LaserEntity(path=path, color_hex='#0000FF', process_type='raster')
    
    # Width = 100, Height = 50, Speed = 100, Gap = 0.1, Overscan = 10%
    # time_per_pass = 100 / 100 = 1s
    # passes = 50 / 0.1 = 500
    # base_time = 1 * 500 = 500s
    # overscan = 500 * 0.1 = 50s
    # total = 550s
    time = calculator.calculate_entity_time(entity)
    assert time == pytest.approx(550.0, 0.1)

def test_calculate_total_job(calculator):
    # Mix of entities
    p1 = Path("M 0 0 L 10 0") # Length 10
    e1 = LaserEntity(path=p1, color_hex='#FF0000', process_type='cut') # Time: 10 / 10 = 1s
    
    p2 = Path("M 10 0 L 10 10") # Length 10
    e2 = LaserEntity(path=p2, color_hex='#00FF00', process_type='mark') # Time: 10 / 50 = 0.2s

    # Transit from p1.end (10, 0) to p2.start (10, 0) = 0 distance -> 0s transit
    
    result = calculator.calculate_total_job([e1, e2])
    
    assert result['estimated_total_time_seconds'] == pytest.approx(1.2, 0.1)
    assert result['layer_breakdown']['cut']['time'] == pytest.approx(1.0, 0.1)
    assert result['layer_breakdown']['mark']['time'] == pytest.approx(0.2, 0.1)
