import math
from typing import Tuple
from svgelements import Path, Point

class MathEngine:
    """Handles mathematical operations for distance, area, and path discretization."""
    
    @staticmethod
    def calculate_length(path: Path, error_limit: float = 0.1) -> float:
        """
        Calculates the total length of a given SVG Path.
        `svgelements` provides a `length()` method which approximates Bézier lengths.
        The `error_limit` defines the precision for discretizing curves.
        """
        if not path:
            return 0.0
        
        # svgelements handles the discretization internally with length()
        return path.length(error=error_limit)
    
    @staticmethod
    def calculate_bounding_box(path: Path) -> Tuple[float, float, float, float]:
        """
        Calculates the bounding box of a path.
        Returns: (min_x, min_y, max_x, max_y)
        """
        if not path:
            return (0.0, 0.0, 0.0, 0.0)
            
        bbox = path.bbox()
        if not bbox:
            return (0.0, 0.0, 0.0, 0.0)
            
        return bbox
        
    @staticmethod
    def calculate_raster_dimensions(path: Path) -> Tuple[float, float]:
        """
        Calculates the width and height of the bounding box for Raster calculations.
        Returns: (width, height)
        """
        min_x, min_y, max_x, max_y = MathEngine.calculate_bounding_box(path)
        return (max_x - min_x, max_y - min_y)

    @staticmethod
    def calculate_euclidean_distance(p1: Point, p2: Point) -> float:
        """Calculates distance between two points."""
        if not p1 or not p2:
            return 0.0
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
