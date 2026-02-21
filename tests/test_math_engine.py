import pytest
from svgelements import Path, Point
from src.engine.math_engine import MathEngine

def test_calculate_length_square():
    # 100x100 square path
    path = Path("M 0 0 L 100 0 L 100 100 L 0 100 Z")
    length = MathEngine.calculate_length(path)
    assert length == pytest.approx(400.0, 0.1)

def test_calculate_bounding_box():
    path = Path("M 0 0 L 100 0 L 100 50 L 0 50 Z")
    bbox = MathEngine.calculate_bounding_box(path)
    assert bbox == (0.0, 0.0, 100.0, 50.0)

def test_calculate_raster_dimensions():
    path = Path("M 10 20 L 110 20 L 110 70 L 10 70 Z")
    width, height = MathEngine.calculate_raster_dimensions(path)
    assert width == pytest.approx(100.0, 0.1)
    assert height == pytest.approx(50.0, 0.1)

def test_calculate_euclidean_distance():
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    dist = MathEngine.calculate_euclidean_distance(p1, p2)
    assert dist == pytest.approx(5.0, 0.01)
