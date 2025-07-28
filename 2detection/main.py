import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from api.upload import upload
from api.detection import detection
# from api.segmentation import segmentation
from api.fire_extinguisher import fire_extinguisher
from fastapi.responses import FileResponse
import os
# Tạo FastAPI app
app = FastAPI(
    title="AI Detection API",
    description="Professional AI Detection System",
    version="1.0.0"
)

# Tạo API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(
    upload.router,
    prefix="/upload",
    tags=["Upload"]
)
api_router.include_router(
    detection.router,
    prefix="/detection",
    tags=["Detection"]
)
# api_router.include_router(
#     segmentation.router,
#     prefix="/segmentation",
#     tags=["Segmentation"]
# )
api_router.include_router(
    fire_extinguisher.router,
    prefix="/fire_extinguisher",
    tags=["Fire Extinguisher"]
)

# Include API router vào main app
app.include_router(api_router, prefix="/api/v1")

# Root endpoint


@app.get("/")
def root():
    return {"message": "Welcome to AI Fine Pro."}

@app.get("/static/images/{folder}/{category}/{filename}")
def get_static_image(folder: str, category: str, filename: str):
    """
    Endpoint to serve static images from static/images/{folder}/{type}/ directory
    Args:
        folder: Folder name (raw, results, etc.)
        type: Category type
        filename: Name of the image file
    Returns: Image file response or 404 error if not found
    """
    image_path = os.path.join("static", "images", folder, category, filename)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
# Chạy server khi file được execute trực tiếp
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)  # Single worker for testing
