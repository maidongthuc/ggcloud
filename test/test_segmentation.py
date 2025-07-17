import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import base64
from src.llm_gemini import llm
from langchain_core.messages import HumanMessage, SystemMessage


image_file_path = "./images/fire8.png"

with open(image_file_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

messages = [
    # SystemMessage(content=""" You are an expert in inspection and maintenance of fire extinguishers."""),
    HumanMessage(
    content=[
        {"type": "text", "text": """Give the segmentation masks for the objects *dust on the fire extinguisher wall*. 
         Output a JSON list of segmentation masks where each entry contains the 2D bounding box in the key "box_2d" and the segmentation mask in key "mask"."""},
        {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"},
    ]
)
]

ai_msg = llm.invoke(messages)
print(ai_msg.content)