import json

from fastapi import APIRouter
from fastapi import HTTPException, Request
from src.llm_gemini import llm
from src.prompt import preprocessing_prompt_detection
from src.info_image import (read_image,
                            draw_bounding_boxes,
                            cut_bounding_boxes)
from models.request_models import Object_Detection

router = APIRouter()


@router.post("/draw_object_detection/")
def draw_object_detection(
    object_detection: Object_Detection,
    request: Request = None
):
    """
    Endpoint to perform object detection on an image
    Args:
        object_detection: Object containing objects to detect and image URL
    Returns: Detection results with bounding boxes or raw content if JSON parsing fails
    """
    print(f"Received objects: {object_detection.objects}")
    print(f"Received image URL: {object_detection.url_image}")

    # Create messages for LLM with prompt and image
    messages = preprocessing_prompt_detection(
        objects=object_detection.objects,
        encoded_image=object_detection.url_image
    )

    # Read image dimensions (width, height)
    w, h, img = read_image(object_detection.url_image)

    # Call LLM to perform detection
    ai_msg = llm.invoke(messages)

    try:
        # Parse JSON response from LLM
        detections = json.loads(ai_msg.content)
        # Generate bounding boxes from detection results
        response_data = draw_bounding_boxes(
            detections, w, h, img, object_detection.url_image, request)
        return response_data
    except Exception as e:
        # Return general error
        raise HTTPException(
            status_code=500,
            detail=f"Error processing detection: {str(e)}"
        )


@router.post("/cut_object_detection/")
def cut_object_detection(
    object_detection: Object_Detection,
    request: Request = None
):
    """
    Endpoint to cut bounding boxes from an image based on detection results
    Args:
        object_detection: Object containing objects to detect and image URL
    Returns: List of cropped images with bounding boxes
    """
    # Create messages for LLM with prompt and image
    messages = preprocessing_prompt_detection(
        objects=object_detection.objects,
        encoded_image=object_detection.url_image
    )

    # Read image dimensions (width, height)
    w, h, img = read_image(object_detection.url_image)

    # Call LLM to perform detection
    ai_msg = llm.invoke(messages)

    try:
        # Parse JSON response from LLM
        detections = json.loads(ai_msg.content)
        # Generate bounding boxes from detection results
        response_data = cut_bounding_boxes(
            detections, w, h, img, object_detection.url_image, request)
        return response_data
    except Exception as e:
        # Return general error
        raise HTTPException(
            status_code=500,
            detail=f"Error processing detection: {str(e)}"
        )
