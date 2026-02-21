from typing import List, Dict, Any
from svgelements import Point
from src.parsers.svg_parser import LaserEntity
from src.engine.math_engine import MathEngine

class LaserTimeCalculator:
    """Calculates the execution time of a laser job based on the parsed entities."""
    
    def __init__(self, 
                 cut_speed: float, 
                 vector_engrave_speed: float, 
                 raster_engrave_speed: float, 
                 transit_speed: float,
                 scan_gap: float = 0.1,
                 overscan_factor: float = 0.1):
        self.cut_speed = cut_speed
        self.vector_engrave_speed = vector_engrave_speed
        self.raster_engrave_speed = raster_engrave_speed
        self.transit_speed = transit_speed
        self.scan_gap = scan_gap
        # Assume an overscan time penalty of 10% per raster pass for acceleration/deceleration
        self.overscan_factor = overscan_factor 
        
    def calculate_entity_time(self, entity: LaserEntity) -> float:
        """Calculates the time required to process a single entity."""
        if entity.process_type == 'cut':
            length = MathEngine.calculate_length(entity.path)
            return length / self.cut_speed
            
        elif entity.process_type == 'mark':
            length = MathEngine.calculate_length(entity.path)
            return length / self.vector_engrave_speed
            
        elif entity.process_type == 'raster':
            width, height = MathEngine.calculate_raster_dimensions(entity.path)
            if width == 0 or height == 0:
                return 0.0
                
            # Time per scan line = width / speed
            # Number of scan lines = height / scan_gap
            time_per_pass = width / self.raster_engrave_speed
            passes = height / self.scan_gap
            base_time = time_per_pass * passes
            
            # Add overscan penalty
            overscan_time = base_time * self.overscan_factor
            return base_time + overscan_time
            
        return 0.0

    def optimize_transit_path(self, entities: List[LaserEntity]) -> List[LaserEntity]:
        """
        Sorts entities using a simple nearest-neighbor heuristic to minimize transit moves.
        Note: True TSP is O(N!), nearest neighbor is O(N^2) but "good enough" for most laser jobs.
        """
        if not entities:
            return []
            
        unvisited = entities.copy()
        # Start at 0,0 (Home)
        current_pos = Point(0, 0)
        optimized_order = []
        
        while unvisited:
            # Find the nearest next entity
            nearest = None
            min_dist = float('inf')
            
            for entity in unvisited:
                # Approximate start point of entity as the first subpath's first point
                if entity.path and len(entity.path) > 0:
                    try:
                        start_point = entity.path[0].start
                    except AttributeError:
                        start_point = current_pos # Fallback if path parsing behaves unexpectedly
                        
                    dist = MathEngine.calculate_euclidean_distance(current_pos, start_point)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = entity
                else:
                    nearest = entity # Handle empty paths by just consuming them
                    min_dist = 0
            
            # Best matched entity
            unvisited.remove(nearest)
            optimized_order.append(nearest)
            
            # Update current_pos to the endpoint of the processed entity
            if nearest.path and len(nearest.path) > 0:
                try:
                    current_pos = nearest.path[-1].end
                except AttributeError:
                    pass

        return optimized_order

    def calculate_total_job(self, entities: List[LaserEntity]) -> Dict[str, Any]:
        """
        Calculates the complete job process analyzing transit between entities and process times.
        """
        optimized_entities = self.optimize_transit_path(entities)
        
        total_time = 0.0
        transit_time = 0.0
        total_distance_cut = 0.0
        total_distance_transit = 0.0
        
        layer_breakdown = {
            'cut': {'time': 0.0, 'distance': 0.0},
            'mark': {'time': 0.0, 'distance': 0.0},
            'raster': {'time': 0.0, 'area': 0.0} # Raster reports area roughly instead of distance
        }
        
        current_pos = Point(0, 0)
        
        for entity in optimized_entities:
            # Calculate transit to start of entity
            if entity.path and len(entity.path) > 0:
                try:
                    start_point = entity.path[0].start
                    transit_dist = MathEngine.calculate_euclidean_distance(current_pos, start_point)
                    total_distance_transit += transit_dist
                    t_time = transit_dist / self.transit_speed
                    transit_time += t_time
                    total_time += t_time
                except AttributeError:
                    pass
            
            # Add processing time
            process_time = self.calculate_entity_time(entity)
            total_time += process_time
            
            # Metrics update
            layer_breakdown[entity.process_type]['time'] += process_time
            if entity.process_type in ['cut', 'mark']:
                length = MathEngine.calculate_length(entity.path)
                layer_breakdown[entity.process_type]['distance'] += length
                total_distance_cut += length
            elif entity.process_type == 'raster':
                width, height = MathEngine.calculate_raster_dimensions(entity.path)
                layer_breakdown['raster']['area'] += (width * height)
                
            # Update position to the end of the entity
            if entity.path and len(entity.path) > 0:
                try:
                    current_pos = entity.path[-1].end
                except AttributeError:
                    pass
        
        # Convert total time to HH:MM:SS format
        hours, remainder = divmod(total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        return {
            'estimated_total_time_seconds': round(total_time, 2),
            'formatted_time': formatted_time,
            'transit_time_seconds': round(transit_time, 2),
            'total_distance_burned_mm': round(total_distance_cut, 2),
            'total_distance_transit_mm': round(total_distance_transit, 2),
            'layer_breakdown': layer_breakdown
        }
