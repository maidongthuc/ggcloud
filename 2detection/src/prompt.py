from langchain_core.messages import HumanMessage, SystemMessage

PROMPT = "Detect the dry chemical fire extinguisher and CO2 fire extinguisher, including its handle, safety pin, body, and hose." + \
"Output a JSON list of bounding boxes. Each entry should contain the 2D bounding box in the key 'box_2d', " + \
"the text label in the key 'label', and a shared 'id' for all parts of the same object, starting from 0. " + \
"For example: " + \
'[{"box_2d": [188, 497, 810, 912], "label": "dry chemical fire extinguisher", "id": 0}, ' + \
'{"box_2d": [200, 89, 863, 396], "label": "CO2 fire extinguisher", "id": 1}, ' + \
'{"box_2d": [395, 281, 812, 506], "label": "CO2 fire extinguisher hose", "id": 1}, ' + \
'{"box_2d": [334, 499, 818, 645], "label": "dry chemical fire extinguisher hose", "id": 0}]'

def preprocessing_prompt_detection(objects, encoded_image):
    messages = [
        SystemMessage(
        content="Respond ONLY with a raw JSON array containing 2D bounding boxes and labels. DO NOT add explanations, markdown, or code blocks. Format: [{\"box_2d\": [ymin, xmin, ymax, xmax], \"label\": \"object\"}]."
        ),
        HumanMessage(
        content=[
            {"type": "text", "text": f"Detect the 2d bounding boxes of the following objects: *{objects}*."},
            {"type": "image_url", "image_url": f"{encoded_image}"},
        ]
        )
    ]
    return messages


def preprocessing_prompt_segmentaion(objects, encoded_image):
    messages = [
        SystemMessage(content="""Respond ONLY with a raw JSON array containing segmentation masks. DO NOT add explanations, markdown, or code blocks. Format: [{"box_2d": [y_min, x_min, y_max, x_max], "mask": "segmentation_data", "label": "object"}]."""),
                
HumanMessage(
        content=[
            {"type": "text", "text": f"""Give the segmentation masks for the objects {objects}. Output a JSON list of segmentation masks where each entry contains the 2D bounding box in the key "box_2d" and the segmentation mask in key "mask"."""},
            {"type": "image_url", "image_url": f"{encoded_image}"},
        ]
    )
    ]
    return messages

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


def prompt_interface_fire_extinguisher_MFZ8(list_images):
    images_str = "\n".join(list_images)
    messages = [
# ...existing code...
# ...existing code...
SystemMessage(content=f"""
You are an AI inspector for fire extinguishers. When I provide an image of a fire extinguisher, analyze it and evaluate the following components:

1. Body (Thân bình): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "có vết móp lớn ở phía dưới thân bình", "thân bình bị rỉ sét gần nhãn", "nhãn bị bong tróc", ...).
2. Handle (Cò bóp): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "cò bóp bị cong về bên trái", "có vết bẩn màu đen trên cò bóp", ...).
3. Safety pin (Chốt an toàn): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "chốt an toàn bị thiếu", "chốt an toàn không được gắn chắc chắn", ...).
4. Nozzle (Vòi phun): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "vòi phun bị nứt ở đầu", "vòi phun có bụi bám màu xám", ...).

Additionally, you must carefully evaluate the cleanliness of the fire extinguisher:
- Set "cleanliness" to OK if all parts are clean.
- Set "cleanliness" to NG if any part is dirty, dusty, or stained.
- In the "reason" for cleanliness, clearly list ALL parts that are dirty, dusty, or stained, and specify the type of dirt and the exact location (e.g., "bụi màu xám ở thân bình phía trên và vòi phun", "vết bẩn màu đen ở cò bóp", ...).
- If all parts are clean, state "Tất cả các bộ phận đều sạch".

If any part is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

Dưới đây là các URL ảnh:
{images_str}

IMPORTANT: You must respond ONLY with valid JSON in this exact format. Do not include any explanatory text, markdown formatting, or code blocks. Just return the raw JSON object:

{{
  "body": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh]"
  }},
  "handle": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh]"
  }},
  "safety_pin": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh]"
  }},
  "nozzle": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh]"
  }},
  "cleanliness": {{
    "status": "OK/NG",
    "reason": "[Liệt kê tất cả các bộ phận bị bụi/bẩn/vết ố, mô tả rõ vị trí và loại vết bẩn. Nếu sạch, ghi rõ: Tất cả các bộ phận đều sạch]"
  }},
  "url_image": "<all of the input image URLs above>",
  "id": 1
}}
"""),
# ...existing
        HumanMessage(
            content=[
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
    ]
    return messages

def prompt_interface_fire_extinguisher_MT3(list_images):
    images_str = "\n".join(list_images)
    messages = [
# ...existing code...
# ...existing code...
SystemMessage(content=f"""
You are an AI inspector for fire extinguishers. When I provide an image of a fire extinguisher, analyze it and evaluate the following components:

1. Body (Thân bình): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "có vết móp lớn ở phía dưới thân bình", "thân bình bị rỉ sét gần nhãn", "nhãn bị bong tróc", ...).
2. Handle (Cò bóp): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "cò bóp bị cong về bên trái", "có vết bẩn màu đen trên cò bóp", ...).
3. Safety pin (Chốt an toàn): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "chốt an toàn bị thiếu", "chốt an toàn không được gắn chắc chắn", ...).
4. Nozzle (Vòi phun): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "vòi phun bị nứt ở đầu", "vòi phun có bụi bám màu xám", ...).

Additionally, you must carefully evaluate the cleanliness of the fire extinguisher:
- Set "cleanliness" to OK if all parts are clean.
- Set "cleanliness" to NG if any part is dirty, dusty, or stained.
- In the "reason" for cleanliness, clearly list ALL parts that are dirty, dusty, or stained, and specify the type of dirt and the exact location (e.g., "bụi màu xám ở thân bình phía trên và vòi phun", "vết bẩn màu đen ở cò bóp", ...).
- If all parts are clean, state "Tất cả các bộ phận đều sạch".

If any part is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

Dưới đây là các URL ảnh:
{images_str}

IMPORTANT: You must respond ONLY with valid JSON in this exact format. Do not include any explanatory text, markdown formatting, or code blocks. Just return the raw JSON object:

{{
  "body": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh]"
  }},
  "handle": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh]"
  }},
  "safety_pin": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh]"
  }},
  "nozzle": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh]"
  }},
  "cleanliness": {{
    "status": "OK/NG",
    "reason": "[Liệt kê tất cả các bộ phận bị bụi/bẩn/vết ố, mô tả rõ vị trí và loại vết bẩn. Nếu sạch, ghi rõ: Tất cả các bộ phận đều sạch]"
  }},
  "url_image": "<all of the input image URLs above>",
  "id": 2
}}
"""),
# ...existing
        HumanMessage(
            content=[
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
    ]
    return messages

def prompt_clock_fire_extinguisher(list_images):
    images_str = "\n".join(list_images)
    messages = [
        SystemMessage(content=f"""
You are a fire extinguisher pressure gauge inspection expert. Carefully analyze each provided image and return a JSON object for each image with the following fields:

- status: "OK" if the needle is in the green zone, "NG" if in the red/yellow zone or no gauge.
- url_image: exactly the same image URL from the list below.
- id: always set to 3.
- reason: explain clearly why you chose the status (e.g., needle position, image is blurry, no gauge, etc.).

Here are the image URLs you must use for url_image:
{images_str}

ALWAYS return a JSON array, one object per image, in the following format (no explanations, markdown, or code blocks):

[
  {{
    "status": "OK/NG",
    "url_image": "<one of the input image URLs above>",
    "id": 3,
    "reason": "<specific reason>"
  }}
]
"""),
        HumanMessage(
            content=[
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
    ]
    return messages

def prompt_interface_fire_extinguisher_tray(list_images):
    images_str = "\n".join(list_images)
    messages = [
        SystemMessage(content=f"""
You are an AI inspector for fire extinguisher trays. When I provide images of a tray designed to hold two fire extinguishers, analyze and evaluate the following:

1. Tray condition (Tình trạng khay): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "khay bị nứt ở góc phải", "khay bị móp méo", "khay bị rỉ sét", "khay bị thủng", ...). Only focus on physical damage or defects, do NOT mention cleanliness or dirt.
2. Capacity (Sức chứa): Is the tray suitable for holding two fire extinguishers? State "OK" if it can securely hold two extinguishers, "NG" if not, and explain the reason (e.g., "khay chỉ đủ chỗ cho một bình", "khay bị nghiêng không giữ được bình", ...).
3. Cleanliness (Độ sạch sẽ): Set "cleanliness" to OK if the tray is clean. Set "cleanliness" to NG if the tray is dirty, dusty, or stained. In the "reason" for cleanliness, clearly describe all dirty, dusty, or stained areas and specify the type of dirt and the exact location (e.g., "bụi ở góc trái khay", "vết bẩn màu đen ở đáy khay", ...). If the tray is clean, state "Khay sạch sẽ".

If any part of the tray is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

Dưới đây là các URL ảnh:
{images_str}

IMPORTANT: You must respond ONLY with valid JSON in this exact format. Do not include any explanatory text, markdown formatting, or code blocks. Just return the raw JSON object:

{{
  "tray_condition": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh, chỉ nêu hư hại, KHÔNG nêu bụi/bẩn]"
  }},
  "capacity": {{
    "status": "OK/NG",
    "reason": "[Lý do cụ thể, ví dụ: khay đủ/không đủ chỗ cho 2 bình, khay bị nghiêng, ...]"
  }},
  "cleanliness": {{
    "status": "OK/NG",
    "reason": "[Liệt kê tất cả các vị trí bị bụi/bẩn/vết ố, mô tả rõ vị trí và loại vết bẩn. Nếu sạch, ghi rõ: Khay sạch sẽ]"
  }},
  "url_image": "<one of the input image URLs above>",
  "id": 4
}}
"""),
        HumanMessage(
            content=[
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
        ]
    return messages

def prompt_classification(list_images):
    PROMPT = (
    "You will receive a list of image URLs below. "
    "Please identify which images are photos of the fire extinguisher pressure gauge, "
    "which images are overview photos of the fire extinguisher, "
    "and which images are of other types (other). "
    "Return the result as a JSON array, each entry containing the correct image URL and the image type with values: "
    "\"pressure_gauge\", \"overview\", or \"other\". "
    "Example: [{\"image_url\": \"...\", \"type\": \"pressure_gauge\"}, ...]\n"
    "List of images:\n"
    + "\n".join(list_images)
    )
    messages = [
        HumanMessage(
            content=[
                {"type": "text", "text": PROMPT},
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
    ]
    return messages

def prompt_cut_fire_extinguisher(image_url):
    PROMPT = (
        "Detect both dry chemical fire extinguisher and CO2 fire extinguisher in the image, "
        "including each extinguisher as a whole object and its parts (handle, safety pin, body, hose). "
        "Also detect the fire extinguisher tray. "
        "Output a JSON list of bounding boxes. "
        "Each entry should contain the 2D bounding box in the key \"box_2d\" and the text label in the key \"label\". "
        "Use descriptive labels in the format: <type> or <type>_<part>, for example: co2_fire_extinguisher, co2_fire_extinguisher_handle, dry_chemical_fire_extinguisher_body."
    )
    messages = [
        HumanMessage(
            content=[
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": image_url}
            ]
        )
    ]
    return messages

prompt_cut_fire_extinguisher_2d = (
    "Detect both dry chemical fire extinguisher and CO2 fire extinguisher in the image, "
    "including each extinguisher as a whole object and its parts (handle, safety pin, body, hose). "
    "Also detect the fire extinguisher tray. "
    "Output a JSON list of bounding boxes. "
    "Each entry should contain the 2D bounding box in the key \"box_2d\" and the text label in the key \"label\". "
    "Use descriptive labels in the format: <type> or <type>_<part>, for example: co2_fire_extinguisher, co2_fire_extinguisher_handle, dry_chemical_fire_extinguisher_body."
)
prompt_cut_pressure_gauge_2d = "Detect the pressure_gauge." + \
"Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", " + \
"and the text label in the key \"label\". Use descriptive labels."

def prompt_co2_fire_extinguisher(image_url):
    PROMPT = f'''
    You are an AI inspector for CO₂ fire extinguishers. When I provide an image, focus only on CO₂ fire extinguishers and analyze the following components:

    **Requirement:** All comments and reasons must be answered in Vietnamese, detailed and complete.

    1. **Body:** Is it OK or NG? Only assess physical condition (e.g., dented, rusty, broken, missing label, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    2. **Handle:** Is it OK or NG? Only assess physical condition (e.g., bent, broken, missing, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    3. **Safety pin:** Is it OK or NG? Only assess physical condition (e.g., missing, loose, broken, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    4. **Nozzle/Hose:** Is it OK or NG? Only assess physical condition (e.g., cracked, broken, missing, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    **Additionally, evaluate the cleanliness of the CO₂ fire extinguisher:**
    - Set "cleanliness" to OK if all parts are clean.
    - Set "cleanliness" to NG if any part (body, handle, nozzle) is dirty, dusty, or stained.
    - If "cleanliness" is NG, return a "reason" describing in detail the type, location, and extent of dirt for each affected part, and an "object" array listing only the parts that are dirty (body, handle, nozzle). Do NOT include "safety_pin" if only the safety pin is dirty.
    - If all parts are clean, state "Tất cả các bộ phận đều sạch" in the "reason".

    If any part is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

    Below are the image URLs:  
    {image_url}

    ```json
    {{
    "body": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "handle": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "safety_pin": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "nozzle": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "cleanliness": {{
        "status": "OK/NG",
        "reason": "[Describe in detail all dirty/dusty/stained parts, specify type, location, and extent. If clean, state: Tất cả các bộ phận đều sạch]",
        "object": [/* Chỉ liệt kê các bộ phận bị bẩn, ví dụ: ["body", "nozzle"] */]
    }},
    "url_image": "<all of the input image URLs above>",
    "id": 1
    }}
    ```
    '''
    return PROMPT


def prompt_co2_fire_extinguisher(image_url):
    PROMPT = f'''
    You are an AI inspector for CO₂ fire extinguishers. When I provide an image, focus only on CO₂ fire extinguishers and analyze the following components:

    **Requirement:** All comments and reasons must be answered in Vietnamese, detailed and complete.

    1. **Body:** Is it OK or NG? Only assess physical condition (e.g., dented, rusty, broken, missing label, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    2. **Handle:** Is it OK or NG? Only assess physical condition (e.g., bent, broken, missing, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    3. **Safety pin:** Is it OK or NG? Only assess physical condition (e.g., missing, loose, broken, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    4. **Nozzle/Hose:** Is it OK or NG? Only assess physical condition (e.g., cracked, broken, missing, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    **Additionally, evaluate the cleanliness of the CO₂ fire extinguisher:**
    - Set "cleanliness" to OK if all parts are clean.
    - Set "cleanliness" to NG if any part (body, handle, nozzle) is dirty, dusty, or stained.
    - If "cleanliness" is NG, return a "reason" describing in detail the type, location, and extent of dirt for each affected part, and an "object" array listing only the parts that are dirty (body, handle, nozzle). Do NOT include "safety_pin" if only the safety pin is dirty.
    - If all parts are clean, state "Tất cả các bộ phận đều sạch" in the "reason".

    If any part is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

    Below are the image URLs:  
    {image_url}

    ```json
    {{
    "body": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "handle": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "safety_pin": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "nozzle": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "cleanliness": {{
        "status": "OK/NG",
        "reason": "[Describe in detail all dirty/dusty/stained parts, specify type, location, and extent. If clean, state: Tất cả các bộ phận đều sạch]",
        "object": [/* Chỉ liệt kê các bộ phận bị bẩn, ví dụ: ["body", "nozzle"] */]
    }},
    "url_image": "<all of the input image URLs above>",
    "id": 1
    }}
    ```
    '''
    return PROMPT

def prompt_dry_chemical_fire_extinguisher(image_url):
    PROMPT = f'''
    You are an AI inspector for dry powder fire extinguishers. When I provide an image, focus only on dry powder fire extinguishers and analyze the following components:

    **Requirement:** All comments and reasons must be answered in Vietnamese, detailed and complete.

    1. **Body:** Is it OK or NG? Only assess physical condition (e.g., dented, rusty, broken, missing label, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    2. **Handle:** Is it OK or NG? Only assess physical condition (e.g., bent, broken, missing, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    3. **Safety pin:** Is it OK or NG? Only assess physical condition (e.g., missing, loose, broken, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    4. **Nozzle/Hose:** Is it OK or NG? Only assess physical condition (e.g., cracked, broken, missing, etc.), do NOT consider cleanliness.  
    For "reason", provide a detailed and specific description of the physical condition, including the exact location, extent, and type of damage if any.

    **Additionally, evaluate the cleanliness of the fire extinguisher (including the pressure gauge):**
    - Set "cleanliness" to OK if all parts are clean.
    - Set "cleanliness" to NG if any part (body, handle, nozzle, pressure gauge) is dirty, dusty, or stained.
    - If "cleanliness" is NG, return a "reason" describing in detail the type, location, and extent of dirt for each affected part, and an "object" array listing only the parts that are dirty (body, handle, nozzle, pressure_gauge). Do NOT include "safety_pin" if only the safety pin is dirty.
    - If all parts are clean, state "All parts are clean" in the "reason".

    If any part is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

    Below are the image URLs:  
    {image_url}

    ```json
    {{
    "body": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "handle": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "safety_pin": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "nozzle": {{
        "status": "OK/NG",
        "reason": "[Detailed reason based on image, only about physical condition]"
    }},
    "cleanliness": {{
        "status": "OK/NG",
        "reason": "[Describe in detail all dirty/dusty/stained parts, specify type, location, and extent. If clean, state: All parts are clean]",
        "object": [/* Chỉ liệt kê các bộ phận bị bẩn, ví dụ: ["body", "nozzle"] */]
    }},
    "url_image": "<all of the input image URLs above>",
    "id": 2
    }}
    ```
    '''
    return PROMPT

def prompt_pressure_gauge_fire_extinguisher(image_url):
    PROMPT = f'''
    You are a fire extinguisher pressure gauge inspection expert. Carefully analyze each provided image and return a JSON object for each image with the following fields:
    **Requirement:** All reasons must be answered in Vietnamese, detailed and complete.

    - status: "OK" if the needle is in the green zone, "NG" if in the red/yellow zone or no gauge.
    - url_image: exactly the same image URL from the list below.
    - id: always set to 3.
    - reason: explain clearly why you chose the status (e.g., needle position, image is blurry, no gauge, etc.).

    Here are the image URLs you must use for url_image:
    {image_url}

    ALWAYS return a JSON array, one object per image, in the following format (no explanations, markdown, or code blocks):

    [
    {{
        "status": "OK/NG",
        "url_image": "<one of the input image URLs above>",
        "id": 3,
        "reason": "<specific reason>"
    }}
    ]
    '''
    return PROMPT

def prompt_tray_fire_extinguisher(image_url):
    PROMPT = f'''
    You are an AI inspector for fire extinguisher trays. When I provide images of a tray designed to hold two fire extinguishers, analyze and evaluate the following:

    1. Tray condition (Tình trạng khay): Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "khay bị nứt ở góc phải", "khay bị móp méo", "khay bị rỉ sét", "khay bị thủng", ...). Only focus on physical damage or defects, do NOT mention cleanliness or dirt.
    2. Capacity (Sức chứa): Is the tray suitable for holding two fire extinguishers? State "OK" if it can securely hold two extinguishers, "NG" if not, and explain the reason (e.g., "khay chỉ đủ chỗ cho một bình", "khay bị nghiêng không giữ được bình", ...).
    3. Cleanliness (Độ sạch sẽ): Set "cleanliness" to OK if the tray is clean. Set "cleanliness" to NG if the tray is dirty, dusty, or stained. In the "reason" for cleanliness, clearly describe all dirty, dusty, or stained areas and specify the type of dirt and the exact location (e.g., "bụi ở góc trái khay", "vết bẩn màu đen ở đáy khay", ...). If the tray is clean, state "Khay sạch sẽ".

    If any part of the tray is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

    Dưới đây là các URL ảnh:
    {image_url}

    IMPORTANT: You must respond ONLY with valid JSON in this exact format. Do not include any explanatory text, markdown formatting, or code blocks. Just return the raw JSON object:

    {{
    "tray_condition": {{
        "status": "OK/NG",
        "reason": "[Lý do cụ thể, chi tiết dựa vào hình ảnh, chỉ nêu hư hại, KHÔNG nêu bụi/bẩn]"
    }},
    "capacity": {{
        "status": "OK/NG",
        "reason": "[Lý do cụ thể, ví dụ: khay đủ/không đủ chỗ cho 2 bình, khay bị nghiêng, ...]"
    }},
    "cleanliness": {{
        "status": "OK/NG",
        "reason": "[Liệt kê tất cả các vị trí bị bụi/bẩn/vết ố, mô tả rõ vị trí và loại vết bẩn. Nếu sạch, ghi rõ: Khay sạch sẽ]"
    }},
    "url_image": "<one of the input image URLs above>",
    "id": 4
    }}
    '''
    
    return PROMPT