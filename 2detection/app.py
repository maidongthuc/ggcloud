from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from api.fire_extinguisher.fire_extinguisher import fire_extinguisher
from jinja2 import Template

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'temprature')
RESULTS_FOLDER = os.path.join(STATIC_FOLDER, 'images', 'results')

@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(STATIC_FOLDER, 'index.html'), encoding='utf-8') as f:
        template = Template(f.read())
        return template.render()

@app.post("/api/v1/fire_extinguisher/fire_extinguisher/")
async def fire_extinguisher_api(
    request: Request,
    files: list[UploadFile] = File(...),
    category: str = Form("")
):
    # Gọi hàm xử lý của bạn
    result = fire_extinguisher(files=files, request=request, category=category)
    return JSONResponse(result)

@app.get("/static/images/results/{filename}")
async def serve_image(filename: str):
    file_path = os.path.join(RESULTS_FOLDER, filename)
    return FileResponse(file_path)

# Nếu muốn chạy trực tiếp bằng python app.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)