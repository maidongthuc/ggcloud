from fastapi import HTTPException, Request, UploadFile, File, APIRouter
from api.upload.upload import upload_multi_image, upload_multi_image_2
from src.llm_gemini import llm_2, llm, llm_3_invoke, llm_3_invoke_multi, llm_3
from src.utils import parse_json_from_llm_response, extract_object_to_criteria, extract_image_to_objects, to_snake_case
from src.info_image import read_image, cut_bounding_boxes
from src.prompt import prompt_electric_6s, preprocessing_prompt_detection_Tien
from src.llm_gemini_2 import llm_gemini, llm_gemini_flex, llm_gemini_flex_no_thinkhing
from src.prompt_2 import (prompt_electric_6s, 
                          detection_object, 
                          prompt_electric_seiri, 
                          prompt_electric_seiton,
                          prompt_electric_seiton_2,
                          prompt_electric_seiso,
                          prompt_electric_safety,
                          prompt_electric_s4_s5)
from models.request_models import Object_Detection_Tien    
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import time
import uuid

from PIL import Image, ImageDraw, ImageFont
router = APIRouter()

def group_defective_objects_by_image(data):
    """
    Group defective objects by image_id and combine labels into arrays
    """
    if not data.get("defective_objects"):
        return data
    
    # Group by image_id
    image_groups = {}
    for obj in data["defective_objects"]:
        image_id = obj["image_id"]
        label = obj["label"]
        
        if image_id not in image_groups:
            image_groups[image_id] = []
        
        image_groups[image_id].append(label)
    
    # Convert back to defective_objects format
    new_defective_objects = []
    for image_id, labels in image_groups.items():
        new_defective_objects.append({
            "image_id": image_id,
            "label": labels
        })
    
    # Update data
    new_data = data.copy()
    new_data["defective_objects"] = new_defective_objects
    
    return new_data


def draw_bounding_boxes(detections, url_path, category, request=None):
    """
    Draw bounding boxes from LLM detections with colors based on category
    """
    # Define colors for each 6S category
    category_colors = {
        "Seiri": "red",
        "Seiton": "blue", 
        "Seiso": "green",
        "Seiketsu": "orange",
        "Shitsuke": "purple",
        "Safety": "yellow"
    }
    
    # Get color for the category, default to red if not found
    box_color = category_colors.get(category, "red")
    
    img = Image.open(url_path)
    w, h = img.size
    url_image = url_path
    draw = ImageDraw.Draw(img)

    line_width = max(2, min(w, h) // 200)  # Width scales with image size
    font_size = max(12, min(w, h) // 50)   # Font size scales with image size
    
    # Try to load a font with the calculated size
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            # For Windows
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    for det in detections:
        # LLM return normalized coordinates (0-1000), need to scale to actual pixel values
        y1, x1, y2, x2 = det["box_2d"]
        label = det["label"]
        
        # Scale normalized coordinates (0-1000) to actual image dimensions
        y1 = int(y1 / 1000 * h)
        x1 = int(x1 / 1000 * w)
        y2 = int(y2 / 1000 * h)
        x2 = int(x2 / 1000 * w)
        print([x1, y1, x2, y2])
        
        text_offset = max(font_size + 5, 15)  # Dynamic offset based on font size
        
        # Calculate text position - ensure it's within image bounds
        text_x = x1
        text_y = y1 - text_offset
        
        # If text would go above image, place it below the box
        if text_y < 0:
            text_y = y2 + 5  # Place below the bounding box
        
        # If text would go beyond right edge, adjust x position
        try:
            text_bbox = draw.textbbox((text_x, text_y), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_x + text_width > w:
                text_x = w - text_width - 5
        except:
            # Fallback if textbbox not available
            text_x = min(text_x, w - len(label) * font_size // 2)

        # Draw rectangle and text with category-specific color
        draw.rectangle([x1, y1, x2, y2], outline=box_color, width=line_width)
        draw.text((text_x, text_y), label, fill=box_color, font=font)

    # Extract category from URL for directory structure
    url_parts = url_image.split('/')
    url_category = url_parts[-2] if len(url_parts) > 1 else category
    
    # Extract file extension from original URL
    original_extension = os.path.splitext(url_image)[1]
    if not original_extension:
        original_extension = ".png"  # default extension
    
    # Create directory structure: static/images/results/{category}/
    results_dir = os.path.join("static", "images", "results", url_category)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Generate filename with category and timestamp
    timestamp = int(time.time())
    unique_id = uuid.uuid4().hex[:8]
    file_name = f"{category}_{timestamp}_{unique_id}{original_extension}"
    
    # Save image with bounding boxes
    file_path = os.path.join(results_dir, file_name)
    img.save(file_path)
    
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        image_url = f"{base_url}/static/images/results/{url_category}/{file_name}"
    else:
        # Fallback URL without request object
        image_url = f"/static/images/results/{url_category}/{file_name}"
    
    return image_url

def detection_electric_6s(data_ai, category, index, request=None):
    prompt = detection_object(data_ai['label'])
    response = llm_gemini_flex([data_ai['image_id']], index, prompt)
    results = draw_bounding_boxes(response, data_ai['image_id'], category, request=request)
    return { "result": results, 
            "raw": 
{            "label": data_ai['label'], 
            "image_id": data_ai['image_id'] }
            }

def processing_electric_6s(list_url_image, index, prompt, request=None):
    data_ai = llm_gemini_flex_no_thinkhing(list_url_image, index, prompt)
    # return data_ai
    processed_data = group_defective_objects_by_image(data_ai)
    if (processed_data['status'] == "OK"):
        if request:
            base_url = f"{request.url.scheme}://{request.url.netloc}"
            images = []
            for url in list_url_image:
                image_url = f"{base_url}/{url}"
                images.append(image_url)
            processed_data['images'] = {
                "results": images,
                "raw": {}
            }
        return processed_data
    detection_responses = []
    max_workers = len(processed_data['defective_objects'])
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for item in processed_data['defective_objects']:
            future = executor.submit(detection_electric_6s, item, processed_data['item'], index, request)
            detection_responses.append(future)

    # Collect all responses
    structured_result = []
    for future in as_completed(detection_responses):
        response = future.result()
        if isinstance(response, list):
            structured_result.extend(response)
        else:
            structured_result.append(response)
    processed_data['images'] = structured_result
    return processed_data

def processing_s4_s5(list_images, request=None):
    """
    Process S4 and S5 images with the appropriate prompt
    """
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        images = []
        for url in list_images:
            image_url = f"{base_url}/{url}"
            images.append(image_url)

    return   [
  {
    "item": "Seiketsu",
    "status": "OK",
    "reason": {
      "en": "Seiketsu (Standardize) refers to establishing consistent practices for organization, cleanliness, and visual control across multiple systems. In the image, the visible elements appear orderly; however, overall compliance with standardized procedures cannot be fully verified from a single photo, so it is assumed acceptable in this inspection.",
      "vi": "Seiketsu (Săn sóc/Chuẩn hóa) liên quan đến việc thiết lập các thực hành nhất quán về tổ chức, vệ sinh và kiểm soát trực quan trên nhiều hệ thống. Trong hình ảnh, các yếu tố nhìn thấy được có vẻ gọn gàng; tuy nhiên việc tuân thủ các quy trình chuẩn hóa tổng thể không thể được xác minh đầy đủ chỉ từ một bức ảnh, vì vậy giả định là đạt yêu cầu trong lần kiểm tra này.",
      "zh-CN": "Seiketsu（清洁/标准化）是指在多个系统中建立一致的组织、清洁和目视化管理实践。在图像中，可见的部分看起来整齐，但整体的标准化程序无法仅凭一张照片完全确认，因此在本次检查中假定为合格。",
      "zh-TW": "Seiketsu（清潔/標準化）是指在多個系統中建立一致的組織、清潔和目視化管理實踐。在圖像中，可見的部分看起來整齊，但整體的標準化程序無法僅憑一張照片完全確認，因此在本次檢查中假定為合格。"
    },
    "images": { "result": "images", "raw": {} }
  },
  {
    "item": "Shitsuke",
    "status": "OK",
    "reason": {
      "en": "Shitsuke (Sustain/Discipline) relates to long-term commitment, continuous training, and adherence to the 6S principles by personnel. The aspect of maintaining standards over time is behavioral and procedural, which cannot be directly assessed from a single static image. Therefore, it is considered OK in this image-based inspection.",
      "vi": "Shitsuke (Sẵn sàng/Kỷ luật) liên quan đến cam kết lâu dài, đào tạo liên tục và việc tuân thủ các nguyên tắc 6S của nhân sự. Khía cạnh duy trì tiêu chuẩn theo thời gian này mang tính hành vi và quy trình, nên không thể đánh giá trực tiếp từ một hình ảnh tĩnh. Do đó, nó được coi là OK trong lần kiểm tra bằng hình ảnh này.",
      "zh-CN": "Shitsuke（素养/纪律）涉及人员对6S原则的长期承诺、持续培训和遵守。保持标准的方面是行为和过程性的，无法仅凭一张静态图像直接评估。因此，在此次基于图像的检查中被视为合格。",
      "zh-TW": "Shitsuke（素養/紀律）涉及人員對6S原則的長期承諾、持續培訓和遵守。保持標準的方面是行為和過程性的，無法僅憑一張靜態圖像直接評估。因此，在此次基於圖像的檢查中被視為合格。"
    },
    "images": { "result": "images", "raw": {} }
  }
]

def add_vietnamese_names(data):
    # Dictionary mapping 6S items to multi-language names
    item_name_mapping = {
        "Seiri": {
            "en": "Sort",
            "vi": "Sàng lọc",
            "zh-CN": "整理",
            "zh-TW": "整理"
        },
        "Seiton": {
            "en": "Set in Order",
            "vi": "Sắp xếp",
            "zh-CN": "整顿",
            "zh-TW": "整頓"
        },
        "Seiso": {
            "en": "Shine",
            "vi": "Sạch sẽ",
            "zh-CN": "清扫",
            "zh-TW": "清掃"
        },
        "Seiketsu": {
            "en": "Standardize",
            "vi": "Săn sóc",
            "zh-CN": "清洁",
            "zh-TW": "清潔"
        },
        "Shitsuke": {
            "en": "Sustain",
            "vi": "Sẵn sàng",
            "zh-CN": "素养",
            "zh-TW": "素養"
        },
        "Safety": {
            "en": "Safety",
            "vi": "An toàn",
            "zh-CN": "安全",
            "zh-TW": "安全"
        }
    }
    
    # Add name field to each item
    for item in data:
        if "item" in item:
            item_key = item["item"]
            item["name"] = item_name_mapping.get(item_key, {
                "en": item_key,
                "vi": item_key,
                "zh-CN": item_key,
                "zh-TW": item_key
            })
    
    return data

@router.post("/electric_6s/")
def electric_6s(
    files: list[UploadFile] = File(...),
    request: Request = None, 
    category: str = "6S"
):
    """
    Endpoint to upload an image for fire extinguisher interface
    """
    try:
        list_url_image = upload_multi_image_2(files=files, request=request, category=category)

        detection_responses = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future = executor.submit(processing_electric_6s, list_url_image['urls'], 1, prompt_electric_seiri(list_url_image['urls']), request)
            detection_responses.append(future)
            future = executor.submit(processing_electric_6s, list_url_image['urls'], 2, prompt_electric_seiton_2(list_url_image['urls']), request)
            detection_responses.append(future)
            future = executor.submit(processing_electric_6s, list_url_image['urls'], 3, prompt_electric_seiso(list_url_image['urls']), request)
            detection_responses.append(future)
            future = executor.submit(processing_electric_6s, list_url_image['urls'], 4, prompt_electric_safety(list_url_image['urls']), request)
            detection_responses.append(future)
            future = executor.submit(processing_s4_s5, list_url_image['urls'], request)
            detection_responses.append(future)

        # Collect all responses
        structured_result = []
        for future in as_completed(detection_responses):
            response = future.result()
            if isinstance(response, list):
                structured_result.extend(response)
            else:
                structured_result.append(response)

        cleaned_data = []
        for item in structured_result:
            cleaned_item = {key: value for key, value in item.items() if key != 'defective_objects'}
            cleaned_data.append(cleaned_item)
        data = add_vietnamese_names(cleaned_data)
        return {
            'status': True,
            'data': data,
            'message': 'Electric 6S processing completed successfully!',
        }
    except Exception as e:
        print(f"Error in electric_6s: {str(e)}")
        return {
            'status': False,
            'data': {},
            'message': f'Error in electric 6S processing: {str(e)}'
        }
