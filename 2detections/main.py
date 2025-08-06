import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from api.upload import upload
from api.detection import detection
from fastapi.middleware.cors import CORSMiddleware  # Thêm dòng
# from api.segmentation import segmentation
from api.fire_extinguisher import fire_extinguisher
from api.fire_cabinet import fire_cabinet
from api.electric_6s import electric_6s  # Import the electric_6s 
from api.check_list import check_list  # Import the check_list module
from fastapi.responses import FileResponse
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Tạo FastAPI app
app = FastAPI(
    title="AI Detection API",
    description="Professional AI Detection System",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả domain, có thể chỉnh lại cho an toàn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

api_router.include_router(
    fire_cabinet.router,
    prefix="/fire_extinguisher_cabinet",
    tags=["Fire Cabinet"]
)

api_router.include_router(
    electric_6s.router,
    prefix="/electric_6s",
    tags=["Electric 6S"]
)

api_router.include_router(
    check_list.router,
    prefix="/check_list",
    tags=["Checklist"]
)
# Include API router vào main app
app.include_router(api_router, prefix="/api/v1")

# Root endpoint

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
