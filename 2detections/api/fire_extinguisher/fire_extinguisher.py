from fastapi import HTTPException, Request, UploadFile, File, APIRouter
from api.upload.upload import upload_multi_image
from src.llm_gemini import llm_2, llm, llm_3_invoke, llm_3_invoke_multi
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
                        prompt_classification_2,
                        
                        )
from src.llm_gemini_2 import llm_gemini_nothinking, llm_gemini_thinking
from src.prompt_2 import (prompt_classification_2, 
                          prompt_cut_fire_extinguisher_2, 
                          prompt_system_cut_fire_extinguisher_2, 
                          prompt_cut_hose_co2_extinguisher_2,
                          prompt_cut_fire_extinguisher_tray_2,
                          prompt_cut_pressure_gauge_fire_extinguisher_2
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
        try:
            print(messages)
            ai_msg = llm_3_invoke_multi(urls, messages)
            print(ai_msg)
            print(type(ai_msg))
            detections = parse_json_from_llm_response(ai_msg)
        except Exception as e:
            print("Error in process_llm_threading:", e)
            raise
        
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
    
def process_cut_fire_extinguisher(url_image, function_prompt_cut, request=None):
    try:
        message = function_prompt_cut(url_image)
        print("message", message)
        w, h, img = read_image(url_image)
        ai_msg = llm.invoke(message)
        print("ai_msg", ai_msg.content)
        data_json = parse_json_from_llm_response(ai_msg.content)
        print("data_json", data_json)
        if not data_json or not isinstance(data_json, list):
            raise Exception("AI model trả về dữ liệu rỗng hoặc không phải list!")
        bbox = calculate_union_bbox(data_json)
        label = None
        for item in data_json:
            if item['label'].lower() == "co2 fire extinguisher":
                label = item['label']
                break
        if not label:
            for item in data_json:
                if item['label'].lower() == "dry chemical fire extinguisher":
                    label = item['label']
                    break
        if not label:
            label = max(data_json, key=lambda x: len(x['label']))['label']
        data = {'box_2d': bbox, 'label': label}
        print("data", data)
        response = cut_bounding_boxes(
            detections=[data],
            w=w,
            h=h,
            img=img,
            url_image=url_image,
            request=request
        )
        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing cut fire extinguisher: {str(e)}"
        )

def process_bbox_fire_extinguisher(list_urls, prompt_cut, prompt_system=None):
    print("list_urls", list_urls)
    ai_msg = llm_gemini_thinking(list_urls, prompt_cut, prompt_system)
    data_json = parse_json_from_llm_response(ai_msg)
    return data_json

def group_by_label(data):
    """
    Nhóm các phần tử có cùng label vào chung một mảng chứa các URL
    """
    grouped = {}
    
    for sublist in data:
        for item in sublist:
            label = item["label"]
            if label not in grouped:
                grouped[label] = []
            grouped[label].append(item["url"])
    
    return grouped

def process_cut_overview_front_fire_extinguisher(url_image, request=None):
    w, h, img = read_image(url_image)
    results = [] 
    with ThreadPoolExecutor() as executor:
        futures = []
        future = executor.submit(process_bbox_fire_extinguisher, [url_image], prompt_cut_fire_extinguisher_2, prompt_system_cut_fire_extinguisher_2)
        futures.append(future)
        future = executor.submit(process_bbox_fire_extinguisher, [url_image], prompt_cut_hose_co2_extinguisher_2, prompt_system_cut_fire_extinguisher_2)
        futures.append(future)
        future = executor.submit(process_bbox_fire_extinguisher, [url_image], prompt_cut_fire_extinguisher_tray_2)
        futures.append(future)

        for future in as_completed(futures):
            response = future.result()
            results.append(response)
    group1 = []  # hose_of_co2_fire_extinguisher + co2_fire_extinguisher
    group2 = []  # dry_chemical_fire_extinguisher

    for sublist in results:
        for item in sublist:
            if item["label"] in ["hose_of_co2_fire_extinguisher", "co2_fire_extinguisher"]:
                group1.append(item)
            else:
                group2.append(item)
    bbox = calculate_union_bbox(group1)
    label = "co2_fire_extinguisher"
    data = {'box_2d': bbox, 'label': label}
    group2.append(data)
    group1 = cut_bounding_boxes(
        detections=group2,
        w=w,  # Width not needed for union bbox
        h=h,  # Height not needed for union bbox
        img=img,  # Image not needed for union bbox
        url_image=url_image,  # URL not needed for union bbox
        request=request  # Request not needed for union bbox
    )
    return group1

def process_cut_overview_back_fire_extinguisher(url_image, request=None):
    w, h, img = read_image(url_image)
    results = [] 
    with ThreadPoolExecutor() as executor:
        futures = []
        future = executor.submit(process_bbox_fire_extinguisher, [url_image], prompt_cut_fire_extinguisher_2, prompt_system_cut_fire_extinguisher_2)
        futures.append(future)
        future = executor.submit(process_bbox_fire_extinguisher, [url_image], prompt_cut_fire_extinguisher_tray_2)
        futures.append(future)

        for future in as_completed(futures):
            response = future.result()
            results.append(response)
    group2 = []
    for sublist in results:
        for item in sublist:
            group2.append(item)
    group1 = cut_bounding_boxes(
        detections=group2,
        w=w,  # Width not needed for union bbox
        h=h,  # Height not needed for union bbox
        img=img,  # Image not needed for union bbox
        url_image=url_image,  # URL not needed for union bbox
        request=request  # Request not needed for union bbox
    )
    return group1
def process_cut_pressure_gauge_fire_extinguisher(url_image, request=None):
    w, h, img = read_image(url_image)
    results = process_bbox_fire_extinguisher([url_image], prompt_cut_pressure_gauge_fire_extinguisher_2)
    group1 = cut_bounding_boxes(
        detections=results,
        w=w,  # Width not needed for union bbox
        h=h,  # Height not needed for union bbox
        img=img,  # Image not needed for union bbox
        url_image=url_image,  # URL not needed for union bbox
        request=request  # Request not needed for union bbox
    )
    return group1




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
    

@router.post("/cut_fire_extinguisher/")
def cut_fire_extinguisher(
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
        messages = prompt_classification(list_url_image['urls'])
        ai_msg = llm_2.invoke(messages)
        data = parse_json_from_llm_response(ai_msg.content)

        grouped = {}
        for item in data:
            grouped.setdefault(item["type"], []).append(item["image_url"])

        results = []
        with ThreadPoolExecutor() as executor:
            futures = []
            for url in grouped['overview']:
                future = executor.submit(process_cut_fire_extinguisher, url, prompt_cut_co2_fire_extinguisher, request)
                futures.append(future)
                future = executor.submit(process_cut_fire_extinguisher, url, prompt_cut_dry_chemical_fire_extinguisher, request)
                futures.append(future)
                future = executor.submit(process_cut_fire_extinguisher, url, prompt_cut_tray_fire_extinguisher, request)
                futures.append(future)
            for url in grouped['pressure_gauge']:
                future = executor.submit(process_cut_fire_extinguisher, url, prompt_cut_pressure_gauge_fire_extinguisher, request)
                futures.append(future)

            for future in as_completed(futures):
                response = future.result()
                results.append(response)
        grouped = {}
        for group in results:
            for item in group:
                label_snake = to_snake_case(item["label"])
                grouped.setdefault(label_snake, []).append(item["url"])
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            
            future = executor.submit(process_llm_threading, 
                                     grouped['co2_fire_extinguisher'], 
                                     "MT3",
                                     prompt_co2_fire_extinguisher)
            futures.append(future)

            future = executor.submit(process_llm_threading, 
                                    grouped['dry_chemical_fire_extinguisher'], 

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

@router.post("/fire_extinguisher_2/")
def fire_extinguisher_2(
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

        prompt = prompt_classification_2(list_url_image['urls'])
        ai_msg = llm_gemini_nothinking(list_urls = list_url_image["urls"], prompt = prompt)
        data = parse_json_from_llm_response(ai_msg)

        grouped = {}
        for item in data:
            grouped.setdefault(item["type"], []).append(item["image_url"])

        # list_urls = grouped['pressure_gauge'][0]
        # results = process_cut_pressure_gauge_fire_extinguisher(list_urls, request=request)
        # return results
        results = [] 
        with ThreadPoolExecutor() as executor:
            futures = []
            for url in grouped['overview_front']:
                future = executor.submit(process_cut_overview_front_fire_extinguisher, url, request)
                futures.append(future)
            for url in grouped['overview_back']:
                future = executor.submit(process_cut_overview_back_fire_extinguisher, url, request)
                futures.append(future)
            for url in grouped['pressure_gauge']:
                future = executor.submit(process_cut_pressure_gauge_fire_extinguisher, url, request)
                futures.append(future)
            # for url in grouped['pressure_gauge']:
            #     future = executor.submit(process_cut_fire_extinguisher, url, prompt_cut_pressure_gauge_fire_extinguisher, request)
            #     futures.append(future)

            for future in as_completed(futures):
                response = future.result()
                results.append(response)
        grouped = group_by_label(results)
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            
            future = executor.submit(process_llm_threading, 
                                     grouped['co2_fire_extinguisher'], 
                                     "MT3",
                                     prompt_co2_fire_extinguisher)
            futures.append(future)

            future = executor.submit(process_llm_threading, 
                                    grouped['dry_chemical_fire_extinguisher'], 

                                     "MFZ8",
                                     prompt_dry_chemical_fire_extinguisher)
            futures.append(future)

            future = executor.submit(process_llm_threading, 
                                    grouped['pressure_gauge'], 
                                     "clock",
                                     prompt_pressure_gauge_fire_extinguisher)
            futures.append(future)

            future = executor.submit(process_llm_threading, 
                                    grouped['double_fire_extinguisher_tray'],
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