from fastapi import HTTPException, Request, UploadFile, File, APIRouter
from api.upload.upload import upload_multi_image
from src.llm_gemini import llm_2, llm, llm_3_invoke, llm_3_invoke_multi, llm_3
from src.utils import parse_json_from_llm_response, extract_object_to_criteria, extract_image_to_objects, to_snake_case
from src.info_image import read_image, cut_bounding_boxes
from src.prompt import prompt_electric_6s, preprocessing_prompt_detection_Tien
from api.detection.detection import draw_object_detection_Tien
from models.request_models import Object_Detection_Tien    
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

router = APIRouter()


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
        # Upload multiple images => list url image
    #     list_url_image = upload_multi_image(files=files, request=request, category=category)
    #     message = prompt_electric_6s(list_url_image['urls'])
    #     ai_msg = llm_3.invoke(message)
    #     print("LLM content:", ai_msg.content)  # Debugging line to check LLM response
    #     data_json = parse_json_from_llm_response(ai_msg.content)
    #     object_to_criteria = extract_object_to_criteria(data_json["data"])
    #     image_to_objects = extract_image_to_objects(data_json["data"])
    #     results = {
    #     "success": True,
    #     "data": data_json["data"],
    #     "mapping": {
    #         "object_to_criteria": object_to_criteria,
    #         "image_to_objects": image_to_objects
    #     }
    # }
    #     data = results["data"]
    #     mapping = results["mapping"]
    #     image_to_objects = mapping["image_to_objects"]
    #     object_to_criteria = mapping["object_to_criteria"]

        data = {
  "success": True,
  "data": [
    {
      "Criterion": "Seiri - Sort",
      "Result": "NG",
      "Error details": [
        {
          "Reason": "Debris present on the bottom surface of the cabinet.",
          "Error object": "Small piece of paper and white particles (debris) on the bottom surface",
          "Image URL": "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1753781062_0.jpg"
        }
      ]
    },
    {
      "Criterion": "Seiton - Set in order",
      "Result": "NG",
      "Error details": [
        {
          "Reason": "Wires are loose and untidy at the bottom right.",
          "Error object": "Loose wires at the bottom right",
          "Image URL": "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1753781062_0.jpg"
        },
        {
          "Reason": "Wires are not labeled.",
          "Error object": "Unlabeled wires (e.g., blue, red, yellow, black wires at bottom left, black/yellow wire at right)",
          "Image URL": "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1753781062_0.jpg"
        },
        {
          "Reason": "The protective plastic cover is incomplete, exposing live parts.",
          "Error object": "Incomplete plastic cover exposing live terminals on the top right busbar",
          "Image URL": "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1753781062_0.jpg"
        }
      ]
    },
    {
      "Criterion": "Seiso - Shine",
      "Result": "NG",
      "Error details": [
        {
          "Reason": "Dust and debris are present on the cabinet floor.",
          "Error object": "Dust and debris on the bottom surface of the cabinet",
          "Image URL": "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1753781062_0.jpg"
        }
      ]
    },
    {
      "Criterion": "Safety",
      "Result": "NG",
      "Error details": [
        {
          "Reason": "Live terminals are exposed due to an incomplete protective cover.",
          "Error object": "Exposed live terminals on the top right busbar",
          "Image URL": "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1753781062_0.jpg"
        }
      ]
    },
    {
      "Criterion": "Seiketsu - Standardize",
      "Result": "OK"
    },
    {
      "Criterion": "Shitsuke - Sustain",
      "Result": "OK"
    },
    {
      "Criterion": "Summary",
      "Result": "NG",
      "Reason": "Multiple 6S criteria (Seiri, Seiton, Seiso, Safety) are rated NG."
    }
  ],
  "mapping": {
    "object_to_criteria": {
      "Small piece of paper and white particles (debris) on the bottom surface": "Seiri - Sort",
      "Loose wires at the bottom right": "Seiton - Set in order",
      "Unlabeled wires (e.g., blue, red, yellow, black wires at bottom left, black/yellow wire at right)": "Seiton - Set in order",
      "Incomplete plastic cover exposing live terminals on the top right busbar": "Seiton - Set in order",
      "Dust and debris on the bottom surface of the cabinet": "Seiso - Shine",
      "Exposed live terminals on the top right busbar": "Safety"
    },
    "image_to_objects": {
      "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1753781062_0.jpg": [
        "Small piece of paper and white particles (debris) on the bottom surface",
        "Loose wires at the bottom right",
        "Unlabeled wires (e.g., blue, red, yellow, black wires at bottom left, black/yellow wire at right)",
        "Incomplete plastic cover exposing live terminals on the top right busbar",
        "Dust and debris on the bottom surface of the cabinet",
        "Exposed live terminals on the top right busbar"
      ]
    }
  }
}
        object_to_criteria = data['mapping']['object_to_criteria']
        for url, objects in data['mapping']['image_to_objects'].items():
            obj_payload = Object_Detection_Tien(
                objects=objects,
                url_image=url,
                object_to_criteria=object_to_criteria
            )
        
        draw_result = draw_object_detection_Tien(obj_payload, request)
        return draw_result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in fire extinguisher processing: {str(e)}"
        )
