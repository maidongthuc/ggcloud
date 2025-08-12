from fastapi import HTTPException, Request, UploadFile, File, APIRouter
from api.upload.upload import upload_multi_image
from src.llm_gemini import llm_2, llm, llm_3_invoke, llm_3_invoke_multi, llm_3
from src.utils import parse_json_from_llm_response, build_detection_results, calculate_union_bbox, to_snake_case
from src.info_image import read_image, cut_bounding_boxes
from src.prompt import (
                        prompt_5s_fire_extinguisher_cabinet,
                        prompt_check_list
                        )
                    
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

router = APIRouter()


from fastapi import HTTPException, Request, UploadFile, File, Form, APIRouter

@router.post("/check_list/")
def check_list(
    files: list[UploadFile] = File(...),
    inspection_location: str = Form(None),
    inspection_items_details: str = Form(None),
    inspection_methods_standards: str = Form(None),
    request: Request = None, 
    category: str = "FIRE"
):
    # ...existing code...
    """
    Endpoint to upload an image for fire extinguisher interface
    """
    try:
        # Upload multiple images => list url image
        list_url_image = upload_multi_image(files=files, request=request, category=category)
        print(inspection_location)
        print(inspection_items_details)
        print(inspection_methods_standards)
        message = prompt_check_list(list_url_image['urls'], 
                                    inspection_location=inspection_location,
                                    inspection_items_details=inspection_items_details,
                                    inspection_methods_standards=inspection_methods_standards)
        print(f"Message for LLM: {message}")
        ai_msg = llm_3.invoke(message)
        data_json = parse_json_from_llm_response(ai_msg.content)
        return data_json
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in fire extinguisher processing: {str(e)}"
        )
