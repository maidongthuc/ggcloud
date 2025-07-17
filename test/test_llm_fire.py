import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import base64
from src.llm_gemini import llm
from langchain_core.messages import HumanMessage, SystemMessage


def prompt_interface_fire_extinguisher(list_images):
    messages = [
        SystemMessage(content="""
            You are an AI inspector for fire extinguishers. When I provide an image of a fire extinguisher, analyze it and evaluate the following components:
            1. **Body (Thân bình)**: Is it **OK** or **NOT OK**? Clearly state the reason (e.g., dented, rusted, label missing, etc.).
            2. **Handle (Cò bóp)**: Is it **OK** or **NOT OK**? Clearly state the reason (e.g., broken, bent, missing part, etc.).
            3. **Safety pin (Chốt an toàn)**: Is it **OK** or **NOT OK**? Clearly state the reason (e.g., missing, not secured, damaged, etc.).
            4. **Nozzle (Vòi phun)**: Is it **OK** or **NOT OK**? Clearly state the reason (e.g., cracked, blocked, detached, etc.).

            If any part is not clearly visible (too small, blurry, occluded), return the status as **NO OK** and explain which part is unclear.

            IMPORTANT: You must respond ONLY with valid JSON in this exact format. Do not include any explanatory text, markdown formatting, or code blocks. Just return the raw JSON object:

            {
            "than_binh": {
                "status": "OK/NOT OK",
                "reason": "[Lý do cụ thể]"
            },
            "co_bop": {
                "status": "OK/NOT OK", 
                "reason": "[Lý do cụ thể]"
            },
            "chot_an_toan": {
                "status": "OK/NOT OK",
                "reason": "[Lý do cụ thể]"
            },
            "voi_phun": {
                "status": "OK/NOT OK",
                "reason": "[Lý do cụ thể]"
            }
            }"""),
        HumanMessage(
            content=[
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
    ]
    return messages

list_images = [
    "http://3.92.221.185:8080/static/images/raw/fire/fire_raw_1752287890.jpg",       
    "http://3.92.221.185:8080/static/images/raw/fire/fire_raw_1752287914.jpg"
]

messages = prompt_interface_fire_extinguisher(list_images=list_images)

ai_msg = llm.invoke(messages)
print(ai_msg.content)