from fastapi import HTTPException, Request, UploadFile, File, APIRouter
from api.upload.upload import upload_multi_image
from src.llm_gemini import llm_2, llm, llm_3_invoke, llm_3_invoke_multi
from src.utils import parse_json_from_llm_response, build_detection_results
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
                        )
                    
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

router = APIRouter()


def process_pressure_gauge(url_image, request):
    w, h, img = read_image(url_image)
    messages = prompt_cut_pressure_gauge_2d
    ai_msg = llm_3_invoke(url_image, messages, w, h, img)
    detection = parse_json_from_llm_response(ai_msg)
    return cut_bounding_boxes(
        detections=detection,
        w=w,
        h=h,
        img=img,
        url_image=url_image,
        request=request
    )

def process_overview(url_image, request):
    w, h, img = read_image(url_image)
    messages = prompt_cut_fire_extinguisher_2d
    ai_msg = llm_3_invoke(url_image, messages, w, h, img)
    detection = parse_json_from_llm_response(ai_msg)
    object_detection = build_detection_results(detection)
    return cut_bounding_boxes(
        detections=object_detection,
        w=w,
        h=h,
        img=img,
        url_image=url_image,
        request=request
    )

def process_llm_threading(urls, extinguisher_type, function_prompt):
    """
    Thread function to process LLM for each fire extinguisher type
    """
    try:
        if not urls:
            return {"type": extinguisher_type, "status": "no_images", "result": None}
        
        messages = function_prompt(urls)
        print(messages)
        ai_msg = llm_3_invoke_multi(urls, messages)
        print(ai_msg)
        print(type(ai_msg))
        detections = parse_json_from_llm_response(ai_msg)
        
        return {
            "type": extinguisher_type,
            "status": "success",
            "result": detections
        }
    except Exception as e:
        return {
            "type": extinguisher_type,
            "status": "error", 
            "error": str(e)
        }
def filter_valid_urls(urls):
    return [url for url in urls if url and url.startswith("http")]

@router.post("/fire_extinguisher/")
def fire_extinguisher(
    files: list[UploadFile] = File(...),
    request: Request = None, 
    category: str = "6S"
):
    """
    Endpoint to upload an image for fire extinguisher interface
    """
    try:
        # Upload multiple images => list url image
        list_url_image = upload_multi_image(files=files, request=request, category=category)
        if not list_url_image or 'urls' not in list_url_image or not list_url_image['urls']:
            raise HTTPException(
                status_code=500,
                detail="Error uploading images: upload_multi_image returned None or missing 'urls'"
            )
        # classification
        messages = prompt_classification(list_url_image['urls'])
        ai_msg = llm_2.invoke(messages)
        data = parse_json_from_llm_response(ai_msg.content)

        grouped = {}
        for item in data:
            grouped.setdefault(item["type"], []).append(item["image_url"])
        
        results = []
        with ThreadPoolExecutor() as executor:
            futures = []
            if grouped.get('pressure_gauge'):
                for url_image in grouped['pressure_gauge']:
                    futures.append(executor.submit(process_pressure_gauge, url_image, request))
            if grouped.get('overview'):
                for url_image in grouped['overview']:
                    futures.append(executor.submit(process_overview, url_image, request))
            for future in as_completed(futures):
                results.append(future.result())

        # Trả về kết quả (tùy ý bạn xử lý kết quả trả về)
        grouped = {}
        for group in results:
            for item in group:
                grouped.setdefault(item["label"], []).append(item["url"])

        # grouped = {'pressure_gauge': ['http://0.0.0.0:8080/static/images/results/6S/6S_0_1753666781.jpg'], 'co2_fire_extinguisher_total': ['http://0.0.0.0:8080/static/images/results/6S/6S_0_1753666789.jpg', 'http://0.0.0.0:8080/static/images/results/6S/6S_0_1753666790.jpg'], 'dry_chemical_fire_extinguisher_total': ['http://0.0.0.0:8080/static/images/results/6S/6S_1_1753666789.jpg', 'http://0.0.0.0:8080/static/images/results/6S/6S_1_1753666790.jpg'], 'fire_extinguisher_tray': ['http://0.0.0.0:8080/static/images/results/6S/6S_2_1753666789.jpg', 'http://0.0.0.0:8080/static/images/results/6S/6S_2_1753666790.jpg']}
        # grouped = {
        # "pressure_gauge": [
        #     "http://0.0.0.0:8080/static/images/results/6S/6S_0_1753677482.jpg"
        # ],
        # "co2_fire_extinguisher_total": [
        #     "http://0.0.0.0:8080/static/images/results/6S/6S_0_1753677490.jpg",
        #     "http://0.0.0.0:8080/static/images/results/6S/6S_0_1753677495.jpg"
        # ],
        # "dry_chemical_fire_extinguisher_total": [
        #     "http://0.0.0.0:8080/static/images/results/6S/6S_1_1753677490.jpg",
        #     "http://0.0.0.0:8080/static/images/results/6S/6S_1_1753677495.jpg"
        # ],
        # "fire_extinguisher_tray": [
        #     "http://0.0.0.0:8080/static/images/results/6S/6S_2_1753677490.jpg",
        #     "http://0.0.0.0:8080/static/images/results/6S/6S_2_1753677495.jpg"
        # ]
        # }
        # test_values = process_llm_threading(grouped['co2_fire_extinguisher_total'], 'MT3', prompt_co2_fire_extinguisher)
        # print(test_values)
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            
            future = executor.submit(process_llm_threading, 
                                     grouped['co2_fire_extinguisher_total'], 
                                     "MT3",
                                     prompt_co2_fire_extinguisher)
            futures.append(future)

            future = executor.submit(process_llm_threading, 
                                    grouped['dry_chemical_fire_extinguisher_total'], 

                                     "MFZ8",
                                     prompt_dry_chemical_fire_extinguisher)
            futures.append(future)

            future = executor.submit(process_llm_threading, 
                                    grouped['pressure_gauge'], 
                                     "clock",
                                     prompt_pressure_gauge_fire_extinguisher)
            futures.append(future)

            future = executor.submit(process_llm_threading, 
                                    grouped['fire_extinguisher_tray'],
                                     "tray",
                                     prompt_tray_fire_extinguisher)
            futures.append(future)
            
            # Lấy kết quả theo thứ tự
            results = []
            for future in futures:
                result = future.result()
                results.append(result)

        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in fire extinguisher processing: {str(e)}"
        )