from fastapi import HTTPException, Request, UploadFile, File, APIRouter
from api.upload.upload import upload_multi_image
from src.llm_gemini import llm_2, llm, llm_3_invoke, llm_3_invoke_multi, llm_3
from src.utils import parse_json_from_llm_response, build_detection_results, calculate_union_bbox, to_snake_case
from src.info_image import read_image, cut_bounding_boxes
from src.prompt import (prompt_classification, 
                        prompt_cut_fire_extinguisher, 
                        prompt_cut_fire_extinguisher_2d, 
                        prompt_cut_pressure_gauge_2d,
                        # prompt_clock_fire_extinguisher,
                        # prompt_interface_fire_extinguisher_MT3,
                        # prompt_interface_fire_extinguisher_MFZ8,
                        # prompt_interface_fire_extinguisher_tray,
                        prompt_co2_fire_extinguisher,
                        prompt_dry_chemical_fire_extinguisher,
                        prompt_pressure_gauge_fire_extinguisher,
                        prompt_tray_fire_extinguisher,
                        prompt_cut_co2_fire_extinguisher,
                        prompt_cut_dry_chemical_fire_extinguisher,
                        prompt_cut_pressure_gauge_fire_extinguisher,
                        prompt_cut_tray_fire_extinguisher,
                        prompt_5s_fire_extinguisher_cabinet,
                        )
                    
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

router = APIRouter()


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
        list_url_image = upload_multi_image(files=files, request=request, category=category)
        message = prompt_5s_fire_extinguisher_cabinet(list_url_image['urls'])
        print(f"Message for LLM: {message}")
        ai_msg = llm_3.invoke(message)
        data_json = parse_json_from_llm_response(ai_msg.content)
        return data_json
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in fire extinguisher processing: {str(e)}"
        )
