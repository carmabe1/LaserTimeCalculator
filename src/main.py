import argparse
import json
import sys
import os

# Agregamos la raíz del proyecto al sys.path para que pueda encontrar el módulo 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parsers.svg_parser import SVGParser
from src.engine.calculator import LaserTimeCalculator

def main():
    parser = argparse.ArgumentParser(description="Estimate laser execution time from SVG files.")
    parser.add_argument("file", help="Path to the input SVG file")
    
    # Required calculation parameters (Speeds in mm/s)
    parser.add_argument("--cut_speed", type=float, required=True, help="Speed for cutting paths in mm/s (Red hex #FF0000)")
    parser.add_argument("--vector_engrave_speed", type=float, required=True, help="Speed for vector marking in mm/s (Green hex #00FF00)")
    parser.add_argument("--raster_engrave_speed", type=float, required=True, help="Speed for raster engraving in mm/s (Blue hex #0000FF)")
    parser.add_argument("--transit_speed", type=float, required=True, help="Transit speed between entities in mm/s (G0 moves)")
    
    # Optional calculation parameters
    parser.add_argument("--scan_gap", type=float, default=0.1, help="Advance in Y axis per line for Raster (Default = 0.1mm)")
    parser.add_argument("--ppi", type=float, default=25.4, help="Pixels Per Inch of the SVG. If 1 unit in SVG should be 1mm, use 25.4 (Default). If using 100 DPI, use 100.")
    
    args = parser.parse_args()
    
    try:
        # 1. Parse original SVG
        svg_parser = SVGParser(args.file, ppi=args.ppi)
        entities = svg_parser.parse()
        
        if not entities:
            print(json.dumps({
                "error": "No valid laser operation paths (Red, Green, or Blue) found in the provided SVG."
            }, indent=2))
            sys.exit(1)
            
        # 2. Configure mathematical estimator
        calculator = LaserTimeCalculator(
            cut_speed=args.cut_speed,
            vector_engrave_speed=args.vector_engrave_speed,
            raster_engrave_speed=args.raster_engrave_speed,
            transit_speed=args.transit_speed,
            scan_gap=args.scan_gap
        )
        
        # 3. Compute times and distances
        report = calculator.calculate_total_job(entities)
        
        # Output clean JSON to stdout
        print(json.dumps(report, indent=4))
        
    except FileNotFoundError:
        print(json.dumps({"error": f"File not found: {args.file}"}, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"An error occurred while processing the SVG: {str(e)}"}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
