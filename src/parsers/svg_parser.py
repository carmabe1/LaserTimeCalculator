import svgelements
from dataclasses import dataclass
from typing import List

@dataclass
class LaserEntity:
    """Represents a discrete path or shape to be processed by the laser."""
    path: svgelements.Path
    color_hex: str
    process_type: str  # 'cut', 'mark', 'raster'

class SVGParser:
    """Parses SVG files and extracts geometric entities classified by their operation color."""
    
    # Define mapping of colors to operations based on business rules
    COLOR_MAP = {
        '#FF0000': 'cut',      # Red
        '#00FF00': 'mark',     # Green
        '#0000FF': 'raster'    # Blue
    }
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.svg = svgelements.SVG.parse(filepath)
        self.entities: List[LaserEntity] = []

    def parse(self) -> List[LaserEntity]:
        """Parses the SVG geometry and classifies valid entities."""
        self.entities = []
        
        # Iterating through parsed SVG elements
        for element in self.svg.elements():
            # We are only interested in shapes/paths
            if not isinstance(element, (svgelements.Path, svgelements.Shape)):
                continue

            # Convert explicit shapes to paths for unified processing
            if isinstance(element, svgelements.Shape):
                path = svgelements.Path(element)
            else:
                path = element
            
            # Find the defining color (check stroke first, then fill)
            process_color = None
            
            # Check stroke color
            if hasattr(element, 'stroke') and isinstance(element.stroke, svgelements.Color) and element.stroke.value is not None:
                # svgelements Color hex property returns e.g. '#ff0000'
                hex_val = element.stroke.hex.upper()
                if hex_val in self.COLOR_MAP:
                    process_color = hex_val
            
            # Check fill color if stroke is not a defined operation color
            if process_color is None and hasattr(element, 'fill') and isinstance(element.fill, svgelements.Color) and element.fill.value is not None:
                hex_val = element.fill.hex.upper()
                if hex_val in self.COLOR_MAP:
                    process_color = hex_val
                    
            # If a valid process color was found, append the entity
            if process_color:
                entity = LaserEntity(
                    path=path,
                    color_hex=process_color,
                    process_type=self.COLOR_MAP[process_color]
                )
                self.entities.append(entity)
                
        return self.entities
