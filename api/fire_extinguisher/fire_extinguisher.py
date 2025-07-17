from fastapi import HTTPException, Request, UploadFile, File, APIRouter
import threading
from api.upload.upload import upload_multi_image
from api.detection.detection import cut_object_detection
from models.request_models import Object_Detection
from src.prompt import prompt_interface_fire_extinguisher, prompt_clock_fire_extinguisher
from src.llm_gemini import llm
import json
from src.info_image import read_image

from PIL import Image
from io import BytesIO
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import aiohttp
import asyncio

router = APIRouter()

def process_single_image(image_url, object, index, http_request = None):
    """Xử lý một ảnh và lưu kết quả vào shared list"""
    try:
        
        object_detection_data = Object_Detection(
            # objects="CO2 fire extinguisher (without a pressure gauge)",
            objects= object,
            url_image=image_url
        )
        
        # Gọi cut_object_detection
        detection_result = cut_object_detection(
            object_detection=object_detection_data,
            request = http_request
        )
        
        return{
                "index": index,
                "status": "success",
                "detection_result": detection_result,
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error in fire extinguisher processing: {str(e)}"
        )

async def select_image_clock_async(image_urls, request=None):
    """
    Async version of select_image_clock to avoid blocking
    """
    if not image_urls:
        return None
    
    async def get_image_size(session, url):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    content = await response.read()
                    image = Image.open(BytesIO(content)).convert("RGB")
                    w, h = image.size[:2]
                    return url, w * h
                else:
                    print(f"HTTP error {response.status} for URL: {url}")
                    return url, 0
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return url, 0
    
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [get_image_size(session, url) for url in image_urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        max_area = 0
        selected_url = None
        for result in results:
            if isinstance(result, tuple):
                url, area = result
                if area > max_area:
                    max_area = area
                    selected_url = url
        
        return selected_url
    except Exception as e:
        print(f"Error in select_image_clock_async: {e}")
        return None

def process_llm_threading(urls, extinguisher_type, function_prompt):
    """
    Thread function to process LLM for each fire extinguisher type
    """
    try:
        if not urls:
            return {"type": extinguisher_type, "status": "no_images", "result": None}
        
        messages = function_prompt(urls)
        print("---------------------------------------")
        print(f"Processing {extinguisher_type} with messages: {messages}")
        ai_msg = llm.invoke(messages)
        print("---------------------------------------")
        print(f"LLM response for {extinguisher_type}: {ai_msg.content}")
        print("---------------------------------------")
        detections = json.loads(ai_msg.content)
        
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

@router.post("/fire_extinguisher/")
async def fire_extinguisher(
    files: list[UploadFile] = File(...),
    request: Request = None, 
    category: str = "6S"
):
    """
    Endpoint to upload an image for fire extinguisher interface
    """
    try:
        # Upload multiple images => list url image
        list_url_image = await upload_multi_image(files=files, request=request, category=category)


        
        objects="CO2 fire extinguisher (without a pressure gauge) | Powder fire extinguisher (with pressure gauge) | clock of fire extinguisher | Fire extinguisher tray"
        max_workers = len(list_url_image)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            # Dùng vòng loop để submit task với index
            for index, name in enumerate(list_url_image["urls"]):
                future = executor.submit(process_single_image, name, objects, index, request)
                futures.append(future)
            
            # Lấy kết quả theo thứ tự
            results = []
            for future in futures:
                result = future.result()
                results.append(result)

        # urls_image_fire_extinguigher_co2 = []
        # urls_image_fire_extinguigher_powder = []
        # urls_image_fire_extinguigher_clock = []
        # urls_image_fire_extinguigher_tray = []

        # for item in results:
        #     if item["status"] == "success" and item["detection_result"]:
        #         # detection_result là một list, lấy URL từ mỗi detection
        #         for detection in item["detection_result"]:
        #             if "url" in detection and "label" in detection:
        #                 label = detection["label"]
        #                 url = detection["url"]
                        
        #                 # Phân loại theo label
        #                 if "CO2 fire extinguisher" in label:
        #                     urls_image_fire_extinguigher_co2.append(url)
        #                 elif "Powder fire extinguisher" in label:
        #                     urls_image_fire_extinguigher_powder.append(url)
        #                 elif "clock of fire extinguisher" in label:
        #                     urls_image_fire_extinguigher_clock.append(url)
        #                 elif "Fire extinguisher tray" in label:
        #                     urls_image_fire_extinguigher_tray.append(url)

        # urls_image_fire_extinguigher_clock = await select_image_clock_async(urls_image_fire_extinguigher_clock)

        # with ThreadPoolExecutor(max_workers=4) as executor:
        #     futures = []
            
        #     future = executor.submit(process_llm_threading, 
        #                              urls_image_fire_extinguigher_co2, 
        #                              "co2",
        #                              prompt_interface_fire_extinguisher)
        #     futures.append(future)

        #     future = executor.submit(process_llm_threading, 
        #                              urls_image_fire_extinguigher_powder, 
        #                              "powder",
        #                              prompt_interface_fire_extinguisher)
        #     futures.append(future)

        #     future = executor.submit(process_llm_threading, 
        #                              urls_image_fire_extinguigher_clock, 
        #                              "clock",
        #                              prompt_clock_fire_extinguisher)
        #     futures.append(future)
            
        #     # Lấy kết quả theo thứ tự
        #     results = []
        #     for future in futures:
        #         result = future.result()
        #         results.append(result)
        # return {
        #     "co2": urls_image_fire_extinguigher_co2,
        #     "powder": urls_image_fire_extinguigher_powder,
        #     "clock": urls_image_fire_extinguigher_clock,
        #     "tray": urls_image_fire_extinguigher_tray}
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error in fire extinguisher processing: {str(e)}"
        )

@router.post("/test_fire_extinguisher/")
async def test_fire_extinguisher(url: str):
    
    urls_image_fire_extinguigher_clock = ["http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752633759.png"]
    response = process_llm_threading(urls_image_fire_extinguigher_clock, "test", prompt_clock_fire_extinguisher)
    print(response)
    return response



# from fastapi import HTTPException, Request, UploadFile, File, APIRouter
# import threading
# from api.upload.upload import upload_multi_image
# from api.detection.detection import cut_object_detection
# from models.request_models import Object_Detection
# from src.prompt import prompt_interface_fire_extinguisher
# from src.llm_gemini import llm
# import json
# from src.info_image import read_image

# import asyncio
# import aiohttp
# from PIL import Image
# from io import BytesIO
# import threading
# from concurrent.futures import ThreadPoolExecutor, as_completed

# router = APIRouter()

# import asyncio
# import aiohttp


# def process_llm_threading(urls, extinguisher_type):
#     """
#     Thread function to process LLM for each fire extinguisher type
#     """
#     try:
#         if not urls:
#             return {"type": extinguisher_type, "status": "no_images", "result": None}
        
#         messages = prompt_interface_fire_extinguisher(urls)
#         ai_msg = llm.invoke(messages)
#         detections = json.loads(ai_msg.content)
        
#         return {
#             "type": extinguisher_type,
#             "status": "success",
#             "result": detections
#         }
#     except Exception as e:
#         return {
#             "type": extinguisher_type,
#             "status": "error", 
#             "error": str(e)
#         }
    
# async def select_image_clock_async(image_urls):
#     """
#     Async version of select_image_clock to avoid blocking
#     """
#     if not image_urls:
#         return None
    
#     async def get_image_size(session, url):
#         try:
#             async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
#                 if response.status == 200:
#                     content = await response.read()
#                     image = Image.open(BytesIO(content)).convert("RGB")
#                     w, h = image.size[:2]
#                     return url, w * h
#         except Exception as e:
#             print(f"Error processing URL {url}: {e}")
#             return url, 0
    
#     async with aiohttp.ClientSession() as session:
#         tasks = [get_image_size(session, url) for url in image_urls]
#         results = await asyncio.gather(*tasks, return_exceptions=True)
    
#     max_area = 0
#     selected_url = None
#     for result in results:
#         if isinstance(result, tuple):
#             url, area = result
#             if area > max_area:
#                 max_area = area
#                 selected_url = url
    
#     return selected_url

# @router.post("/fire_extinguisher/")
# async def fire_extinguisher(
#     files: list[UploadFile] = File(...),
#     request: Request = None, 
#     category: str = "6S"
# ):
#     """
#     Endpoint to upload an image for fire extinguisher interface
#     """
#     try:
#         # Upload multiple images
#         response = await upload_multi_image(files=files, request=request, category=category)
#         # response2 = ["http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752548166.png",
#         #              "http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752548188.png"]
#         response2 = ["http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752564039.png",
#                 "http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752564105.png",
#                 "http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752572193.png"]
#         # Shared list để lưu kết quả từ các threads
#         results = []
#         results_lock = threading.Lock()
        
#         def process_single_image(image_url, index, object):
#             """Xử lý một ảnh và lưu kết quả vào shared list"""
#             try:
                
#                 object_detection_data = Object_Detection(
#                     # objects="CO2 fire extinguisher (without a pressure gauge)",
#                     objects= object,
#                     url_image=image_url
#                 )
                
#                 # Gọi cut_object_detection
#                 detection_result = cut_object_detection(
#                     object_detection=object_detection_data,
#                     request=request
#                 )
                
#                 # Thread-safe thêm kết quả
#                 with results_lock:
#                     results.append({
#                         "index": index,
#                         "status": "success",
#                         "detection_result": detection_result,
#                     })
                    
#             except Exception as e:
#                 results.append({
#                         "index": index,
#                         "status": "error",
#                         "error": str(e)
#                     })
        
#         # Tạo và khởi chạy các threads
#         threads = []

#         objects="CO2 fire extinguisher (without a pressure gauge) | Powder fire extinguisher (with pressure gauge) | clock of fire extinguisher | Fire extinguisher tray"
#         for index, image_url in enumerate(response2):
#             thread = threading.Thread(
#                 target=process_single_image, 
#                 args=(image_url, index, objects)
#             )
#             threads.append(thread)
#             thread.start()

#         # Chờ tất cả threads hoàn thành
#         for thread in threads:
#             thread.join()
        
#         # Sắp xếp kết quả theo index để đảm bảo thứ tự
#         results.sort(key=lambda x: x["index"])

#         # Phân loại kết quả theo từng loại fire extinguisher
#         urls_image_fire_extinguigher_co2 = []
#         urls_image_fire_extinguigher_powder = []
#         urls_image_fire_extinguigher_clock = []
#         urls_image_fire_extinguigher_tray = []

#         for item in results:
#             if item["status"] == "success" and item["detection_result"]:
#                 # detection_result là một list, lấy URL từ mỗi detection
#                 for detection in item["detection_result"]:
#                     if "url" in detection and "label" in detection:
#                         label = detection["label"]
#                         url = detection["url"]
                        
#                         # Phân loại theo label
#                         if "CO2 fire extinguisher" in label:
#                             urls_image_fire_extinguigher_co2.append(url)
#                         elif "Powder fire extinguisher" in label:
#                             urls_image_fire_extinguigher_powder.append(url)
#                         elif "clock of fire extinguisher" in label:
#                             urls_image_fire_extinguigher_clock.append(url)
#                         elif "Fire extinguisher tray" in label:
#                             urls_image_fire_extinguigher_tray.append(url)
#         # In kết quả để kiểm tra
#         print("CO2 URLs:", urls_image_fire_extinguigher_co2)
#         print("Powder URLs:", urls_image_fire_extinguigher_powder)
#         print("Clock URLs:", urls_image_fire_extinguigher_clock)
#         print("Tray URLs:", urls_image_fire_extinguigher_tray)
#         url_image_fire_extinguigher_clock = await select_image_clock_async(urls_image_fire_extinguigher_clock)

#         urls_image_fire_extinguigher_co2 = ["http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752633920.png",
#                                             "http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752633936.png"]
#         urls_image_fire_extinguigher_powder = ["http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752633859.png",
#                                                "http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752633891.png"]
#         urls_image_fire_extinguigher_clock = ["http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752633759.png"]
#         urls_image_fire_extinguigher_tray = ["http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752633641.png",
#                                              "http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752633683.png"]


#         with ThreadPoolExecutor(max_workers=4) as executor:
#             # Submit all tasks
#             future_to_type = {
#                 executor.submit(process_llm_threading, urls_image_fire_extinguigher_co2, "co2"): "co2",
#                 executor.submit(process_llm_threading, urls_image_fire_extinguigher_powder, "powder"): "powder", 
#                 executor.submit(process_llm_threading, urls_image_fire_extinguigher_clock, "clock"): "clock",
#                 executor.submit(process_llm_threading, urls_image_fire_extinguigher_tray, "tray"): "tray"
#             }
            
#             # Collect results
#             final_results = {}
#             for future in as_completed(future_to_type):
#                 try:
#                     result = future.result()
#                     final_results[result["type"]] = result
#                 except Exception as e:
#                     extinguisher_type = future_to_type[future]
#                     final_results[extinguisher_type] = {
#                         "type": extinguisher_type,
#                         "status": "error",
#                         "error": str(e)
#                     }

#         return final_results
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, 
#             detail=f"Error in fire extinguisher processing: {str(e)}"
#         )
