import math
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
                 acceleration: float = 500.0,
                 junction_delay: float = 0.05,
                 burn_dwell: float = 0.1,
                 scan_gap: float = 0.1,
                 overscan_factor: float = 0.1):
        self.cut_speed = cut_speed
        self.vector_engrave_speed = vector_engrave_speed
        self.raster_engrave_speed = raster_engrave_speed
        self.transit_speed = transit_speed
        self.acceleration = acceleration
        self.junction_delay = junction_delay
        self.burn_dwell = burn_dwell
        self.scan_gap = scan_gap
        # Assume an overscan time penalty of 10% per raster pass for acceleration/deceleration
        self.overscan_factor = overscan_factor 

    def _calculate_travel_time(self, distance: float, target_speed: float) -> float:
        """Calculates time for a move considering acceleration (trapezoidal profile)."""
        if distance <= 0:
            return 0.0
            
        # Distance to reach target_speed: d = v^2 / (2a)
        accel_dist = (target_speed ** 2) / (2 * self.acceleration)
        
        if distance >= 2 * accel_dist:
            # Reaches target speed: Accelerate + Constant + Decelerate
            accel_time = target_speed / self.acceleration
            const_dist = distance - (2 * accel_dist)
            const_time = const_dist / target_speed
            return (2 * accel_time) + const_time
        else:
            # Triangular profile: Never reaches target speed
            # Peak speed v_p = sqrt(d * a)
            peak_speed = math.sqrt(distance * self.acceleration)
            peak_time = peak_speed / self.acceleration
            return 2 * peak_time
            
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
        total_distance_burned = 0.0
        total_distance_transit = 0.0
        
        layer_breakdown = {
            'cut': {'time': 0.0, 'distance': 0.0},
            'mark': {'time': 0.0, 'distance': 0.0},
            'raster': {'time': 0.0, 'area': 0.0}
        }
        
        current_pos = Point(0, 0)
        
        for entity in optimized_entities:
            if entity.process_type == 'raster':
                # Raster is a block operation
                width, height = MathEngine.calculate_raster_dimensions(entity.path)
                if width > 0 and height > 0:
                    bbox = MathEngine.calculate_bounding_box(entity.path)
                    raster_start = Point(bbox[0], bbox[1])
                    
                    # Transit to start of work
                    t_dist = MathEngine.calculate_euclidean_distance(current_pos, raster_start)
                    total_distance_transit += t_dist
                    t_time = self._calculate_travel_time(t_dist, self.transit_speed)
                    transit_time += t_time
                    total_time += t_time
                    
                    # Add raster processing time
                    p_time = self.calculate_entity_time(entity)
                    total_time += p_time
                    layer_breakdown['raster']['time'] += p_time
                    layer_breakdown['raster']['area'] += (width * height)
                    
                    # Update position
                    current_pos = Point(bbox[2], bbox[3])
                continue

            # Add Dwell time at start of a cut/mark entity
            total_time += self.burn_dwell
            layer_breakdown[entity.process_type]['time'] += self.burn_dwell

            # For Cut and Mark, we iterate through segments
            for segment in entity.path:
                seg_type = type(segment).__name__
                
                if seg_type == 'Move':
                    target_point = segment.end
                    dist = MathEngine.calculate_euclidean_distance(current_pos, target_point)
                    
                    total_distance_transit += dist
                    t_time = self._calculate_travel_time(dist, self.transit_speed)
                    transit_time += t_time
                    total_time += t_time
                    
                    current_pos = target_point
                else:
                    length = segment.length()
                    speed = self.cut_speed if entity.process_type == 'cut' else self.vector_engrave_speed
                    
                    # Core burn time
                    p_time = length / speed
                    # Plus junction delay (acceleration/deceleration at the vertex)
                    p_time += self.junction_delay
                    
                    total_time += p_time
                    total_distance_burned += length
                    
                    layer_breakdown[entity.process_type]['time'] += p_time
                    layer_breakdown[entity.process_type]['distance'] += length
                    current_pos = segment.end
        
        # Convert total time to HH:MM:SS format
        hours, remainder = divmod(total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        return {
            'estimated_total_time_seconds': round(total_time, 2),
            'formatted_time': formatted_time,
            'transit_time_seconds': round(transit_time, 2),
            'total_distance_burned_mm': round(total_distance_burned, 2),
            'total_distance_transit_mm': round(total_distance_transit, 2),
            'layer_breakdown': layer_breakdown
        }
