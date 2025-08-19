from fastapi import HTTPException, Request, UploadFile, File, APIRouter
from api.upload.upload import upload_multi_image_2
from src.llm_gemini_2 import llm_gemini
from src.llm_gemini import llm_2, llm, llm_3_invoke, llm_3_invoke_multi, llm_3
from src.utils import parse_json_from_llm_response, build_detection_results, calculate_union_bbox, to_snake_case
from src.info_image import read_image, cut_bounding_boxes
from src.prompt_2 import prompt_fire_cabinet
from PIL import Image
import io        
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from ultralytics import YOLO
import torch
import time
import uuid
import os
from PIL import ImageDraw, ImageEnhance
model_fire_cabinet = YOLO("best_cabinet.pt")  # pretrained YOLOv8n model
router = APIRouter()

def transform_cabinet_data(data, image_results, list_images, request=None):
    transformed_results = []
    
    # Vietnamese names mapping
    vietnamese_names = {
        "overview": "Tổng quan",
        "cleanliness": "Vệ sinh",
        "organization": "Sắp xếp",
        "fire_hose": "Vòi bạc chữa cháy",
        "fire_valve": "Van mở chữa cháy", 
        "fire_nozzle": "Lăng phun chữa cháy",
        "cabinet_lock": "Chốt khóa tủ"
    }
    
    # Function to convert paths to URLs
    def paths_to_urls(paths, request):
        if not request:
            return paths
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        return [f"{base_url}/{path}" for path in paths]
    
    # 1. Handle overview (special case with nested structure)
    if "overview" in data:
        overview_item = {
            "item": "overview",
            "name": vietnamese_names["overview"],
            "images": paths_to_urls(list_images, request),  # Convert to URLs
            "details": []
        }
        
        # Add cleanliness and organization as details
        for sub_item in ["cleanliness", "organization"]:
            if sub_item in data["overview"]:
                overview_item["details"].append({
                    "item": sub_item,
                    "name": vietnamese_names[sub_item],
                    "status": data["overview"][sub_item]["status"],
                    "reason": data["overview"][sub_item]["reason"]
                })
        
        transformed_results.append(overview_item)
    
    # 2. Handle other components (fire_hose, fire_valve, fire_nozzle, cabinet_lock)
    components = ["fire_hose", "fire_valve", "fire_nozzle", "cabinet_lock"]
    
    for component in components:
        if component in data:
            component_images = image_results.get(component, [])
            component_item = {
                "item": component,
                "name": vietnamese_names[component],
                "images": paths_to_urls(component_images, request),  # Convert to URLs
                "status": data[component]["status"],
                "reason": data[component]["reason"]
            }
            
            transformed_results.append(component_item)
    
    return transformed_results



@router.post("/fire_extinguisher_cabinet/")
def fire_extinguisher_cabinet(
    files: list[UploadFile] = File(...),
    request: Request = None, 
    category: str = "FIRE"
):
    """
    Endpoint to upload an image for fire extinguisher interface
    """
    try:
        # Upload multiple images => list url image
        list_url_image = upload_multi_image_2(files=files, request=request, category=category)

        output_dir = "static/images/results/FIRE"
        os.makedirs(output_dir, exist_ok=True)

        # Read images once and store them
        images = []
        for file in files:
            # Reset file pointer to beginning
            file.file.seek(0)
            file_content = file.file.read()
            image = Image.open(io.BytesIO(file_content))
            images.append(image)

        # Run YOLO detection
        results = model_fire_cabinet(images, device='cuda' if torch.cuda.is_available() else 'cpu')
        
        detection_results = []
        for i, result in enumerate(results):
            original_image = images[i]
            boxes = result.boxes
            
            if boxes is not None:
                for j, box in enumerate(boxes):
                    # Extract class ID and get class name
                    class_id = int(box.cls[0].item())
                    class_name = model_fire_cabinet.names[class_id]
                
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    # Define the 20px border area around bbox
                    padding = 100
                    border_x1 = max(0, int(x1) - padding)
                    border_y1 = max(0, int(y1) - padding)
                    border_x2 = min(original_image.width, int(x2) + padding)
                    border_y2 = min(original_image.height, int(y2) + padding)
                    
                    # Crop the expanded area (bbox + 20px padding)
                    cropped_expanded = original_image.crop((border_x1, border_y1, border_x2, border_y2))
                    
                    # Calculate new bbox coordinates relative to the cropped image
                    new_x1 = int(x1) - border_x1
                    new_y1 = int(y1) - border_y1
                    new_x2 = int(x2) - border_x1
                    new_y2 = int(y2) - border_y1
                    
                    # Create darkened version of the cropped image
                    enhancer = ImageEnhance.Brightness(cropped_expanded)
                    darkened_cropped = enhancer.enhance(0.3)  # Make 70% darker
                    
                    # Create mask for the original bbox area within the cropped image
                    mask = Image.new('L', cropped_expanded.size, 0)  # Black mask
                    draw_mask = ImageDraw.Draw(mask)
                    draw_mask.rectangle([new_x1, new_y1, new_x2, new_y2], fill=255)
                    
                    # Paste original brightness back only to the bbox area
                    darkened_cropped.paste(cropped_expanded, mask=mask)
                    
                    draw = ImageDraw.Draw(darkened_cropped)
                    draw.rectangle([new_x1, new_y1, new_x2, new_y2], 
                                    outline="#00FF00", width=3)
                    
                    # Save the final cropped and highlighted image
                    timestamp = int(time.time())
                    unique_id = str(uuid.uuid4())[:8]
                    filename = f"FIRE_highlighted_{class_name}_{timestamp}_{unique_id}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    darkened_cropped.save(filepath, "JPEG", quality=95)
                    detection_results.append({
                        class_name: filepath
                    })

        # Group results by class name
        grouped_results = {}
        for detection in detection_results:
            for class_name, filepath in detection.items():
                if class_name not in grouped_results:
                    grouped_results[class_name] = []
                grouped_results[class_name].append(filepath)
        
        print(f"Grouped results: {grouped_results}")
        print(f"list images: {list_url_image['urls']}")

        data_ai = llm_gemini(list_url_image['urls'], prompt_fire_cabinet)
    
        response = transform_cabinet_data(data_ai, grouped_results, list_url_image['urls'], request)
        return {
            'status': True,
            'data': response,
            'message': f'Fire cabinet analysis completed!'
        }
        
    except Exception as e:
        print(f"Error in electric_6s: {str(e)}")
        return {
            'status': False,
            'data': {},
            'message': f'Error in electric 6S processing: {str(e)}'
        }
