import json

from fastapi import APIRouter
from fastapi import HTTPException, Request
from src.llm_gemini import llm
from src.prompt import preprocessing_prompt_segmentaion
from src.info_image import (read_image,
                            draw_segmentation)
from models.request_models import Object_Detection

router = APIRouter()


@router.post("/draw_segmentation/")
def draw_segmentation(object_detection: Object_Detection, request: Request = None):
    """
    Endpoint to perform segmentation on an image
    """

    # Create messages for LLM with prompt and image
    messages = preprocessing_prompt_segmentaion(
        objects=object_detection.objects,
        encoded_image=object_detection.url_image
    )

    # Read image dimensions (width, height)
    w, h, image = read_image(object_detection.url_image)

    # Call LLM to perform detection
    ai_msg = llm.invoke(messages)

    try:
        # Parse JSON response from LLM
        detections = json.loads(ai_msg.content)
        # Generate bounding boxes from detection results
        response_data = draw_segmentation(
            detections, w, h, image, object_detection.url_image, request)
        return response_data
    except Exception as e:
        # Return general error
        raise HTTPException(
            status_code=500,
            detail=f"Error processing detection: {str(e)}"
        )
