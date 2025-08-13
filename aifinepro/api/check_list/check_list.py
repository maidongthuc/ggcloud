from fastapi import HTTPException, Request, UploadFile, File, APIRouter
from api.upload.upload import upload_multi_image, upload_multi_image_2
from src.llm_gemini import llm_2, llm, llm_3_invoke, llm_3_invoke_multi, llm_3
from src.utils import parse_json_from_llm_response, build_detection_results, calculate_union_bbox, to_snake_case
from src.info_image import read_image, cut_bounding_boxes

from src.prompt_2 import prompt_checklist   
from src.llm_gemini_2 import llm_gemini   
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

router = APIRouter()


from fastapi import HTTPException, Request, UploadFile, File, Form, APIRouter

def add_images_with_base_url(data, list_url_image, request=None):
    """
    Function to add images field to data with base URL
    """
    # Create a copy of data to avoid modifying original
    updated_data = data.copy()
    
    # Add base URL to images if request is provided
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        full_urls = [f"{base_url}/{image_path}" for image_path in list_url_image]
        updated_data["images"] = full_urls
    else:
        # If no request, use original paths
        updated_data["images"] = list_url_image.copy()
    
    return updated_data

@router.post("/check_list/")
def check_list(
    files: list[UploadFile] = File(...),
    inspection_location: str = Form(None),
    inspection_items_details: str = Form(None),
    inspection_methods_standards: str = Form(None),
    request: Request = None, 
    category: str = "CL"
):
    # ...existing code...
    """
    Endpoint to upload an image for fire extinguisher interface
    """
    try:
        # Upload multiple images => list url image
        list_url_image = upload_multi_image_2(files=files, request=request, category=category)
        print(f"List URL Image: {list_url_image['urls']}")
        message = prompt_checklist( inspection_location=inspection_location,
                                    inspection_items_details=inspection_items_details,
                                    inspection_methods_standards=inspection_methods_standards)
        ai_msg = llm_gemini(list_path=list_url_image['urls'], prompt=message)
        result = add_images_with_base_url(ai_msg, list_url_image['urls'], request)
        return {
            'status': True,
            'data': result,
            'message': f'Checklist analysis completed'
        }
        
    except Exception as e:
        print(f"Error in electric_6s: {str(e)}")
        return {
            'status': False,
            'data': {},
            'message': f'Error in electric 6S processing: {str(e)}'
        }
