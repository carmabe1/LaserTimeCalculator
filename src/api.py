import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.parsers.svg_parser import SVGParser
from src.engine.calculator import LaserTimeCalculator

app = FastAPI(title="LaserTimeCalculator API")

# Configure CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/calculate")
async def calculate_laser_time(
    file: UploadFile = File(...),
    cut_speed: float = Form(...),
    vector_engrave_speed: float = Form(...),
    raster_engrave_speed: float = Form(...),
    transit_speed: float = Form(...),
    scan_gap: float = Form(0.1),
    ppi: float = Form(25.4),
    accel: float = Form(500.0),
    junction_delay: float = Form(0.05),
    burn_dwell: float = Form(0.1)
):
    if not file.filename.lower().endswith('.svg'):
        raise HTTPException(status_code=400, detail="File must be an SVG")

    # Save to a temporary file because svgelements expects a filepath
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Parse SVG
        parser = SVGParser(filepath=tmp_path, ppi=ppi)
        entities = parser.parse()

        if not entities:
            raise HTTPException(status_code=400, detail="No valid laser operation paths (Red, Green, Blue) found.")

        # Calculate time
        calculator = LaserTimeCalculator(
            cut_speed=cut_speed,
            vector_engrave_speed=vector_engrave_speed,
            raster_engrave_speed=raster_engrave_speed,
            transit_speed=transit_speed,
            acceleration=accel,
            junction_delay=junction_delay,
            burn_dwell=burn_dwell,
            scan_gap=scan_gap
        )
        report = calculator.calculate_total_job(entities)
        
        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing SVG: {str(e)}")
    finally:
        # Clean up temp file
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
