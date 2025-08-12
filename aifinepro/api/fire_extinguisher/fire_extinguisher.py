from fastapi import HTTPException, Request, UploadFile, File, APIRouter, Response
from api.upload.upload import upload_multi_image
from src.utils import parse_json_from_llm_response, build_detection_results, calculate_union_bbox, to_snake_case
from src.llm_gemini_2 import llm_vision, llm_gemini
from src.prompt_2 import prompt_cut_all_fire_extinguisher, prompt_fire_extinguisher, prompt_pressure_gauge, prompt_fire_extinguisher_tray
from src.info_image import cut_bounding_boxes, read_image
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.genai import types
router = APIRouter()
from ultralytics import YOLO
from PIL import Image
import io
import os
import torch
import time
import uuid
from src.model import ImageClassifier
classifier = ImageClassifier()
# Load a model
model_fire = YOLO("best_fire_2.pt")  # pretrained YOLOv8n model
model_clock = YOLO("best_clock_11.pt")  # pretrained YOLOv8n model for clock detection

def cut_fire_extinguisher(url_image, request):
    w,h,img = read_image(url_image)
    print("Image dimensions:", w, h)  # Debugging line to check image dimensions
    prompt_cut_fire_extinguisher_2 = prompt_cut_all_fire_extinguisher(url_image)
    print("Prompt for cutting fire extinguisher:", prompt_cut_fire_extinguisher_2)  # Debugging line to check prompt
    response = llm_vision(prompt_cut_fire_extinguisher_2)
    return response
    try:
        response = response['choices'][0]['message']['content']
        response = parse_json_from_llm_response(response)
        print("LLM response:", response)  # Debugging line to check LLM response
        results = cut_bounding_boxes(response, w, h,1932,2548, img, url_image, request=request)
        return results
    except Exception as e:
        raise Exception(f"Error invoking LLM: {str(e)}")


# @router.post("/fire_extinguisher/")
# def fire_extinguisher(
#     files: list[UploadFile] = File(...),
#     request: Request = None, 
#     category: str = "6S"
# ):
#     """
#     Endpoint to upload an image for fire extinguisher interface
#     """
#     try:
#         # Upload multiple images => list url image
#         list_url_image = upload_multi_image(files=files, request=request, category=category)
#         url_image = ["http://104.198.192.254:8080/static/images/raw/6S/6S_raw_1754555315.jpg", 
#                      "http://104.198.192.254:8080/static/images/raw/6S/6S_raw_1754549401.jpg", 
#                      "http://104.198.192.254:8080/static/images/raw/6S/6S_raw_1754549340.jpeg"]
#         print("hi")
        
#         results = cut_fire_extinguisher(url_image[0], request)
#         # results = llm_gemini([url_image[0]])


#         # results = llm_gemini([url_image[0]], "You are a professional fire extinguisher object detection expert with extensive experience in identifying and locating fire safety equipment in various environments")
#         # results = [] 
#         # with ThreadPoolExecutor() as executor:
#         #     futures = []
#         #     for url in url_image:
#         #         future = executor.submit(cut_fire_extinguisher, url, request)
#         #         futures.append(future)

#         #     for future in as_completed(futures):
#         #         response = future.result()
#         #         results.append(response)

#         return results
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error in fire extinguisher processing: {str(e)}"
#         )
    
from io import BytesIO

# @router.post("/fire_extinguisher2/")
# def fire_extinguisher2(url_image: str = ""):
#     """
#     Endpoint to return image as binary response
#     """
#     try:
#         w, h, img = read_image(url_image)
        
#         # Convert PIL image to bytes
#         img_io = BytesIO()
#         img.save(img_io, format='PNG')
#         img_io.seek(0)
        
#         return Response(
#             content=img_io.getvalue(),
#             media_type="image/png",
#             headers={"Content-Disposition": "inline; filename=image.png"}
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error in fire extinguisher processing: {str(e)}"
#         )

# @router.post("/fire_extinguisher3/")
# def fire_extinguisher3(
#     files: list[UploadFile] = File(...),
#     request: Request = None, 
#     category: str = "6S"
# ):
#     """
#     Endpoint to upload an image for fire extinguisher interface and return types.Part images
#     """
#     try:
#         image_parts = []
        
#         file = files[0]
#             # Read file content
#         file_content = file.file.read()
            
#             # Determine MIME type based on file extension or content type
#         mime_type = file.content_type or "image/jpeg"
#         if not mime_type.startswith("image/"):
#             mime_type = "image/jpeg"
#         print(f"Detected MIME type: {mime_type}")  # Debugging line to check MIME type
#             # Create types.Part from bytes
#         image_part = types.Part.from_bytes(
#             data=file_content, 
#             mime_type=mime_type
#         )
            
#         result = llm_gemini(image_part)
#         parse_json = parse_json_from_llm_response(result)
#         return parse_json
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error in fire extinguisher processing: {str(e)}"
#         )
    
# @router.post("/fire_extinguisher4/")
# def fire_extinguisher4(
#     files: list[UploadFile] = File(...),
#     request: Request = None, 
#     category: str = "6S"
# ):
#     """
#     Endpoint to upload an image for fire extinguisher interface and return types.Part images
#     """
#     try:
#         image_parts = []
        
#         file = files[0]
#             # Read file content
#         file_content = file.file.read()
            
#             # Convert to base64
#         base64_encoded = base64.b64encode(file_content).decode('utf-8')
        
#         prompt_cut_fire_extinguisher_2 = prompt_cut_all_fire_extinguisher(base64_encoded)
    
#         response = llm_vision(prompt_cut_fire_extinguisher_2)

#         return response
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error in fire extinguisher processing: {str(e)}"
#         )

# @router.post("/fire_extinguisher5/")
# def fire_extinguisher5(
#     files: list[UploadFile] = File(...),
#     request: Request = None, 
#     category: str = "6S"
# ):
#     """
#     Endpoint to upload an image for fire extinguisher interface and return types.Part images
#     """
#     try:
#         import os
#         from openai import OpenAI
#         import base64
#         client = OpenAI(
#             base_url="https://api.studio.nebius.com/v1/",
#             api_key="eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNjU4MjcwMTIyNjQ3NDQ4MzIzOCIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTkxMjM5NTM2MCwidXVpZCI6ImE1ODIxNWQyLTZkMzctNDk4YS1hMjc1LWRkNzAyNjkyOGM5MSIsIm5hbWUiOiJVbm5hbWVkIGtleSIsImV4cGlyZXNfYXQiOiIyMDMwLTA4LTA4VDA0OjU2OjAwKzAwMDAifQ.hBSFGUqqQPl4D3WsRk56z1niq52xJkNF66O3V1VVC9c"
#         )
#         base64_encoded_image = base64.b64encode(open("fire.jpg", "rb").read()).decode("utf-8")
#         response = client.chat.completions.create(
#             model="Qwen/Qwen2.5-VL-72B-Instruct",
#             temperature=0.5,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "text",
#                             "text": """What's happening in this photo?"""
#                         },
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"""data:image/jpeg;base64,{base64_encoded_image}"""
#                             }
#                         }
#                     ]
#                 }
#             ]
#         )

#         return response.to_json()
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error in fire extinguisher processing: {str(e)}"
#         )
    

def processing_result_fire(result, list_images, label,request):
    """
    Function to process the result from LLM and return a formatted prompt.
    """
    try:
        print(result)
        if request:
            base_url = f"{request.url.scheme}://{request.url.netloc}"
            full_urls = [f"{base_url}/{path}" for path in list_images[f"{label}"]]
            url_body = [f"{base_url}/{path}" for path in list_images.get(f"{label}_body", [])]
            url_safety_pin = [f"{base_url}/{path}" for path in list_images.get(f"{label}_safety_pin", [])]
            url_handle = [f"{base_url}/{path}" for path in list_images.get(f"{label}_handle", [])]
            url_nozzle = [f"{base_url}/{path}" for path in list_images.get(f"{label}_hose", [])]
            result["url"] = full_urls
            result["body"]["url"] = url_body
            result["handle"]["url"] = url_handle
            result["safety_pin"]["url"] = url_safety_pin
            result["nozzle"]["url"] = url_nozzle

            return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in fire extinguisher processing: {str(e)}"
        )
    
def processing_result_tray_clock(result, list_images, label,request):
    """
    Function to process the result from LLM and return a formatted prompt.
    """
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        full_urls = [f"{base_url}/{path}" for path in list_images[f"{label}"]]
        result["url"] = full_urls
        return result

def processing_llm(list_path, prompt, title):
    result = llm_gemini(list_path, prompt)
    return {
        "title": title,
        "result": result
    }

# @router.post("/fire_extinguisher6/")
# def fire_extinguisher6(
#     files: list[UploadFile] = File(...),
#     request: Request = None, 
#     category: str = "6S"
# ):
#     """
#     Endpoint to upload multiple images for fire extinguisher detection using YOLO model
#     and crop detected objects into separate images
#     """
#     try:
#         images = []
#         image_info = []
        
#         # Process all uploaded files
#         for i, file in enumerate(files):
#             # Read file content
#             file_content = file.file.read()
            
#             # Convert bytes to PIL Image for YOLO
#             image = Image.open(io.BytesIO(file_content))
#             images.append(image)
    

#         print(f"Processing {len(images)} images")
        
#         # Run YOLO inference on all images
#         results = model_fire(images, device='cuda' if torch.cuda.is_available() else 'cpu')
#         output_dir = "static/images/results/FIRE"
#         os.makedirs(output_dir, exist_ok=True)

#         # Process results and save cropped images
        
#         # Create output directory if not exists

#         # Define allowed class names
#         # Define allowed class names
#         allowed_classes = {
#             "co2_fire_extinguisher",
#             "dry_chemical_fire_extinguisher", 
#             "fire_extinguisher_tray"
#         }
        
#         # Change variable name to avoid conflict with YOLO results
#         detection_results = []
#         for i, result in enumerate(results):  # 'results' is from YOLO model
#             original_image = images[i]
#             boxes = result.boxes
            
#             if boxes is not None:
#                 for j, box in enumerate(boxes):
#                     # Extract class ID and get class name
#                     class_id = int(box.cls[0].item())
#                     class_name = model_fire.names[class_id]
                    
#                     # Only process if class name is in allowed classes
#                         # Extract bounding box coordinates
#                     if class_name in allowed_classes:
#                         x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
#                         # Crop the detected object
#                         cropped_image = original_image.crop((int(x1), int(y1), int(x2), int(y2)))
#                         timestamp = int(time.time())
#                         unique_id = str(uuid.uuid4())[:8]
#                         filename = f"FIRE_result_{class_name}_{timestamp}_{unique_id}.jpg"
#                         filepath = os.path.join(output_dir, filename)
                        
#                         # Save cropped image
#                         cropped_image.save(filepath, "JPEG", quality=95)

#                         # Add to results with class_name as key
#                         detection_results.append({
#                             class_name: filepath
#                         })
#                     else:
#                         # Vẽ bbox và làm tối phần xung quanh cho class không được phép
#                         from PIL import ImageDraw, ImageEnhance
                        
#                         # Get bbox coordinates
#                         x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
#                         # Define the 20px border area around bbox
#                         padding = 100
#                         border_x1 = max(0, int(x1) - padding)
#                         border_y1 = max(0, int(y1) - padding)
#                         border_x2 = min(original_image.width, int(x2) + padding)
#                         border_y2 = min(original_image.height, int(y2) + padding)
                        
#                         # Crop the expanded area (bbox + 20px padding)
#                         cropped_expanded = original_image.crop((border_x1, border_y1, border_x2, border_y2))
                        
#                         # Calculate new bbox coordinates relative to the cropped image
#                         new_x1 = int(x1) - border_x1
#                         new_y1 = int(y1) - border_y1
#                         new_x2 = int(x2) - border_x1
#                         new_y2 = int(y2) - border_y1
                        
#                         # Create darkened version of the cropped image
#                         enhancer = ImageEnhance.Brightness(cropped_expanded)
#                         darkened_cropped = enhancer.enhance(0.3)  # Make 70% darker
                        
#                         # Create mask for the original bbox area within the cropped image
#                         mask = Image.new('L', cropped_expanded.size, 0)  # Black mask
#                         draw_mask = ImageDraw.Draw(mask)
#                         draw_mask.rectangle([new_x1, new_y1, new_x2, new_y2], fill=255)
                        
#                         # Paste original brightness back only to the bbox area
#                         darkened_cropped.paste(cropped_expanded, mask=mask)
                        
#                         draw = ImageDraw.Draw(darkened_cropped)
#                         draw.rectangle([new_x1, new_y1, new_x2, new_y2], 
#                                      outline="#00FF00", width=3)
                        
#                         # Save the final cropped and highlighted image
#                         timestamp = int(time.time())
#                         unique_id = str(uuid.uuid4())[:8]
#                         filename = f"FIRE_highlighted_{class_name}_{timestamp}_{unique_id}.jpg"
#                         filepath = os.path.join(output_dir, filename)
#                         darkened_cropped.save(filepath, "JPEG", quality=95)
#                         detection_results.append({
#                             class_name: filepath
#                         })


#         grouped_results = {}
#         for detection in detection_results:
#             # Lấy class_name và image từ mỗi detection
#             for class_name, cropped_image in detection.items():
#                 # Nếu class_name chưa có trong grouped_results, tạo list mới
#                 if class_name not in grouped_results:
#                     grouped_results[class_name] = []
                
#                 # Thêm cropped_image vào list của class_name tương ứng
#                 grouped_results[class_name].append(cropped_image)
#         PROMPT = prompt_fire_extinguisher
#         result = llm_gemini(grouped_results['dry_chemical_fire_extinguisher'], PROMPT)
#         parse_json = parse_json_from_llm_response(result)
#         print(grouped_results)
#         if request:
#             base_url = f"{request.url.scheme}://{request.url.netloc}"
#             print("Base URL:", base_url)  # Debugging line to check base URL
#         result = processing_result_fire(parse_json, grouped_results, 'dry_chemical_fire_extinguisher', request)
#         return parse_json
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error in fire extinguisher processing: {str(e)}"
#         )


def run_model_fire(images, output_dir, request=None):
    results = model_fire(images, device='cuda' if torch.cuda.is_available() else 'cpu')
    allowed_classes = {
        "co2_fire_extinguisher",
        "dry_chemical_fire_extinguisher", 
        "fire_extinguisher_tray"
    }
    
    # Change variable name to avoid conflict with YOLO results
    detection_results = []
    for i, result in enumerate(results):  # 'results' is from YOLO model
        original_image = images[i]
        boxes = result.boxes
        
        if boxes is not None:
            for j, box in enumerate(boxes):
                # Extract class ID and get class name
                class_id = int(box.cls[0].item())
                class_name = model_fire.names[class_id]
                
                # Only process if class name is in allowed classes
                    # Extract bounding box coordinates
                if class_name in allowed_classes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    # Crop the detected object
                    cropped_image = original_image.crop((int(x1), int(y1), int(x2), int(y2)))
                    timestamp = int(time.time())
                    unique_id = str(uuid.uuid4())[:8]
                    filename = f"FIRE_result_{class_name}_{timestamp}_{unique_id}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    
                    # Save cropped image
                    cropped_image.save(filepath, "JPEG", quality=95)

                    # Add to results with class_name as key
                    detection_results.append({
                        class_name: filepath
                    })
                else:
                    # Vẽ bbox và làm tối phần xung quanh cho class không được phép
                    from PIL import ImageDraw, ImageEnhance
                    
                    # Get bbox coordinates
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

    grouped_results = {}
    for detection in detection_results:
        # Lấy class_name và image từ mỗi detection
        for class_name, cropped_image in detection.items():
            # Nếu class_name chưa có trong grouped_results, tạo list mới
            if class_name not in grouped_results:
                grouped_results[class_name] = []
            
            # Thêm cropped_image vào list của class_name tương ứng
            grouped_results[class_name].append(cropped_image)
    
    llm_results = []
    with ThreadPoolExecutor() as executor:
        futures = []
        future = executor.submit(processing_llm, grouped_results['dry_chemical_fire_extinguisher'], prompt_fire_extinguisher, "dry_chemical_fire_extinguisher")
        futures.append(future)
        future = executor.submit(processing_llm, grouped_results['co2_fire_extinguisher'], prompt_fire_extinguisher, "co2_fire_extinguisher")
        futures.append(future)
        future = executor.submit(processing_llm, grouped_results['fire_extinguisher_tray'], prompt_fire_extinguisher_tray, "fire_extinguisher_tray")
        futures.append(future)

        for future in as_completed(futures):
            response = future.result()
            results.append(response)   # print(results)

        for future in as_completed(futures):
            try:
                response = future.result()
                title = response["title"]
                result = response["result"]
                
                # Process based on title
                if title in ["dry_chemical_fire_extinguisher", "co2_fire_extinguisher"]:
                    processed_result = processing_result_fire(result, grouped_results, title, request)
                elif title == "fire_extinguisher_tray":
                    processed_result = processing_result_tray_clock(result, grouped_results, title, request)
                else:
                    processed_result = result  # Fallback
                
                llm_results.append({
                    "title": title,
                    "processed_result": processed_result
                })
                
            except Exception as e:
                print(f"Error processing result: {str(e)}")
    
    return llm_results
def run_model_clock(images, output_dir, request):
    results = model_clock(images, device='cuda' if torch.cuda.is_available() else 'cpu')
    # Change variable name to avoid conflict with YOLO results
    detection_results = []
    for i, result in enumerate(results):  # 'results' is from YOLO model
        original_image = images[i]
        boxes = result.boxes
        
        if boxes is not None:
            for j, box in enumerate(boxes):
                # Extract class ID and get class name
                class_id = int(box.cls[0].item())
                class_name = model_clock.names[class_id]
            
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Crop the detected object
                cropped_image = original_image.crop((int(x1), int(y1), int(x2), int(y2)))
                timestamp = int(time.time())
                unique_id = str(uuid.uuid4())[:8]
                filename = f"FIRE_result_{class_name}_{timestamp}_{unique_id}.jpg"
                filepath = os.path.join(output_dir, filename)
                # Save cropped image
                cropped_image.save(filepath, "JPEG", quality=95)

                # Add to results with class_name as key
                detection_results.append({
                    class_name: filepath
                })
               

    grouped_results = {}
    for detection in detection_results:
        # Lấy class_name và image từ mỗi detection
        for class_name, cropped_image in detection.items():
            # Nếu class_name chưa có trong grouped_results, tạo list mới
            if class_name not in grouped_results:
                grouped_results[class_name] = []
            
            # Thêm cropped_image vào list của class_name tương ứng
            grouped_results[class_name].append(cropped_image)
    result = llm_gemini(grouped_results['pressure_gauge'], prompt_pressure_gauge)
    print(result)
    result_3 = processing_result_tray_clock(result[0], grouped_results, 'pressure_gauge', request)
    return result_3


def transform_data(data):
    transformed_results = []
    
    # Dictionary để mapping tên tiếng Việt
    vietnamese_names = {
        "tray_condition": "Tình trạng khay",
        "capacity": "Dung tích",
        "cleanliness": "Độ sạch",
        "body": "Thân bình",
        "handle": "Tay cầm",
        "safety_pin": "Chốt an toàn",
        "nozzle": "Vòi phun",
        "pressure_gauge": "Đồng hồ áp suất"
    }
    
    for item in data["fire_results"]:
        title = item["title"]
        processed_result = item["processed_result"]
        
        # Create base structure
        transformed_item = {
            "title": title,
            "images": processed_result.get("url", []),  # Changed from "url" to "images"
            "details": []
        }
        
        # Handle fire_extinguisher_tray
        if title == "fire_extinguisher_tray":
            # Add tray_condition
            if "tray_condition" in processed_result:
                transformed_item["details"].append({
                    "item": "tray_condition",
                    "name": vietnamese_names["tray_condition"],
                    "status": processed_result["tray_condition"]["status"],
                    "reason": processed_result["tray_condition"]["reason"]
                })
            
            # Add capacity
            if "capacity" in processed_result:
                transformed_item["details"].append({
                    "item": "capacity",
                    "name": vietnamese_names["capacity"],
                    "status": processed_result["capacity"]["status"],
                    "reason": processed_result["capacity"]["reason"]
                })
            
            # Add cleanliness
            if "cleanliness" in processed_result:
                transformed_item["details"].append({
                    "item": "cleanliness",
                    "name": vietnamese_names["cleanliness"],
                    "status": processed_result["cleanliness"]["status"],
                    "reason": processed_result["cleanliness"]["reason"]
                })
        
        # Handle co2_fire_extinguisher and dry_chemical_fire_extinguisher
        elif title in ["co2_fire_extinguisher", "dry_chemical_fire_extinguisher"]:
            components = ["body", "handle", "safety_pin", "nozzle", "cleanliness"]
            
            for component in components:
                if component in processed_result:
                    detail_item = {
                        "item": component,
                        "name": vietnamese_names[component],
                        "status": processed_result[component]["status"],
                        "reason": processed_result[component]["reason"]
                    }
                    
                    # Add images if exists (changed from "url" to "images")
                    if "url" in processed_result[component]:
                        detail_item["images"] = processed_result[component]["url"]
                    
                    # Add object array for cleanliness if exists
                    if component == "cleanliness" and "object" in processed_result[component]:
                        detail_item["object"] = processed_result[component]["object"]
                    
                    transformed_item["details"].append(detail_item)
            
            # Add pressure_gauge to dry_chemical_fire_extinguisher only
            if title == "dry_chemical_fire_extinguisher" and "clock_results" in data and data["clock_results"]:
                pressure_gauge_detail = {
                    "item": "pressure_gauge",
                    "name": vietnamese_names["pressure_gauge"],
                    "status": data["clock_results"]["status"],
                    "reason": data["clock_results"]["reason"],
                    "images": data["clock_results"].get("url", [])  # Changed from "url" to "images"
                }
                transformed_item["details"].append(pressure_gauge_detail)
        
        # Add id if exists
        if "id" in processed_result:
            transformed_item["id"] = processed_result["id"]
        
        transformed_results.append(transformed_item)
    
    return transformed_results

@router.post("/fire_extinguisher/")
def fire_extinguisher(
    files: list[UploadFile] = File(...),
    request: Request = None, 
    category: str = "6S"
):
    """
    Endpoint to upload multiple images for fire extinguisher detection using YOLO model
    and crop detected objects into separate images
    """
    try:
        grouped_results = {}
        for file in files:
            file_content = file.file.read()
            image = Image.open(io.BytesIO(file_content))
            label = classifier.predict(image)
            
            if label not in grouped_results:
                grouped_results[label] = []
            grouped_results[label].append(image)
    
        output_dir = "static/images/results/FIRE"
        os.makedirs(output_dir, exist_ok=True)

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                'fire': executor.submit(run_model_fire, grouped_results.get('fire_extinguisher'), output_dir, request),
                'clock': executor.submit(run_model_clock, grouped_results.get('clock'), output_dir, request)
            }
            
            # Collect results
            results = {key: future.result() for key, future in futures.items()}
        
        data =  {
            "fire_results": results['fire'],
            "clock_results": results['clock'],
            "grouped_results": {k: len(v) for k, v in grouped_results.items()}  # Only return counts
        }
        transformed_data = transform_data(data)
        return transformed_data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in fire extinguisher processing: {str(e)}"
        )        
    
