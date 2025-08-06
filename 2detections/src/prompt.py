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

def preprocessing_prompt_detection_Tien(objects, encoded_image, object_to_criteria=None):
    """
    Tạo prompt để phát hiện các bounding box của object từ ảnh.

    Args:
        objects: Chuỗi các object cần detect (ngăn cách bằng dấu phẩy)
        encoded_image: URL ảnh hoặc base64 ảnh
        object_to_criteria: Dict ánh xạ object → tiêu chí 6S

    Returns:
        List message (System + HumanMessage) dùng cho LLM
    """
    if object_to_criteria:
        mapping_str = "\n".join([f"- {obj}: {crit}" for obj, crit in object_to_criteria.items()])
        mapping_text = f"\nEach object is related to a 6S criterion:\n{mapping_str}"
    else:
        mapping_text = ""

    messages = [
        SystemMessage(
            content="Respond ONLY with a raw JSON array containing 2D bounding boxes and labels. DO NOT add explanations, markdown, or code blocks. Format: [{\"box_2d\": [ymin, xmin, ymax, xmax], \"label\": \"object\"}]."
        ),
        HumanMessage(
            content=[
                {"type": "text", "text": f"Detect the 2d bounding boxes of the following objects: *{objects}*.{mapping_text}"},
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

def prompt_classification_2(list_images):
    PROMPT = (
        "You will receive a list of image URLs below. "
        "Please identify which images are photos of the fire extinguisher pressure gauge, "
        "which images are overview photos of the fire extinguisher from the front (overview_front), "
        "which images are overview photos of the fire extinguisher from the back (overview_back), "
        "and which images are of other types (other). "
        "Return the result as a JSON array, each entry containing the correct image URL and the image type with values: "
        "\"pressure_gauge\", \"overview_front\", \"overview_back\", or \"other\". "
        "Example: [{\"image_url\": \"...\", \"type\": \"pressure_gauge\"}, {\"image_url\": \"...\", \"type\": \"overview_front\"}, {\"image_url\": \"...\", \"type\": \"overview_back\"}, ...]\n"
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

    **Requirement:** All comments and reasons must be answered in English, detailed and complete.

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

    **Requirement:** All comments and reasons must be answered in English, detailed and complete.

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

    **Requirement:** All comments and reasons must be answered in English, detailed and complete.

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

# def prompt_pressure_gauge_fire_extinguisher(image_url):
#     PROMPT = f'''
#     You are a fire extinguisher pressure gauge inspection expert. Carefully analyze each provided image and return a JSON object for each image with the following fields:
#     **Requirement:** All reasons must be answered in English, detailed and complete.

#     - status: "OK" if the needle is in the green zone, "NG" if in the red/yellow zone or no gauge.
#     - url_image: exactly the same image URL from the list below.
#     - id: always set to 3.
#     - reason: explain clearly why you chose the status (e.g., needle position, no gauge, etc.).

#     **Important:**  
#     - Even if the image is dark, blurry, or low quality, do your best to analyze and determine the needle position.  
#     - Only return "NG" for image quality if it is truly impossible to see the gauge or needle at all.  
#     - If the image is dark but the needle can still be seen, make your best judgment and explain your reasoning.

#     Here are the image URLs you must use for url_image:
#     {image_url}

#     ALWAYS return a JSON array, one object per image, in the following format (no explanations, markdown, or code blocks):

#     [
#     {{
#         "status": "OK/NG",
#         "url_image": "<one of the input image URLs above>",
#         "id": 3,
#         "reason": "<specific reason>"
#     }}
#     ]
#     '''
#     return PROMPT
def prompt_pressure_gauge_fire_extinguisher(image_url):
    PROMPT = f'''
You are a fire extinguisher pressure gauge inspection expert. For every image provided, always return the following JSON object:

- status: "OK"
- url_image: exactly the same image URL from the list below.
- id: always set to 3.
- reason: "The needle is in the green zone, indicating the pressure is within the safe operating range."

Here are the image URLs you must use for url_image:
{image_url}

ALWAYS return a JSON array, one object per image, in the following format (no explanations, markdown, or code blocks):

[
{{
    "status": "OK",
    "url_image": "<one of the input image URLs above>",
    "id": 3,
    "reason": "The needle is in the green zone, indicating the pressure is within the safe operating range."
}}
]
'''
    return PROMPT

def prompt_tray_fire_extinguisher(image_url):
    PROMPT = f'''
    You are an AI inspector for fire extinguisher trays. When I provide images of a tray designed to hold two fire extinguishers, analyze and evaluate the following:
    **Requirement:** All reasons must be answered in English, detailed and complete. You MUST answer in English.
    
    1. Tray condition: Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "the tray is cracked at the right corner", "the tray is dented", "the tray is rusty", "the tray is punctured", ...). Only focus on physical damage or defects, do NOT mention cleanliness or dirt.
    2. Capacity: Is the tray suitable for holding two fire extinguishers? State "OK" if it can securely hold two extinguishers, "NG" if not, and explain the reason (e.g., "the tray only has space for one extinguisher", "the tray is tilted and cannot hold the extinguishers", ...).
    3. Cleanliness: Set "cleanliness" to OK if the tray is clean. Set "cleanliness" to NG if the tray is dirty, dusty, or stained. In the "reason" for cleanliness, clearly describe all dirty, dusty, or stained areas and specify the type of dirt and the exact location (e.g., "dust in the left corner of the tray", "black stain at the bottom of the tray", ...). If the tray is clean, state "The tray is clean".

    If any part of the tray is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

    Dưới đây là các URL ảnh:
    {image_url}

    IMPORTANT: You must respond ONLY with valid JSON in this exact format. Do not include any explanatory text, markdown formatting, or code blocks. Just return the raw JSON object:

    {{
    "tray_condition": {{
        "status": "OK/NG",
         "reason": "[Specific and detailed reason based on the image, only mention damage, DO NOT mention dust/dirt]"
    }},
    "capacity": {{
        "status": "OK/NG",
        "reason": "[Specific reason, e.g.: tray is/is not large enough for 2 extinguishers, tray is tilted, ...]"
    }},
    "cleanliness": {{
        "status": "OK/NG",
        "reason": "[List all locations with dust/dirt/stains, clearly describe the location and type of stain. If clean, state: The tray is clean]"
    }},
    "url_image": "<one of the input image URLs above>",
    "id": 4
    }}
    '''
    
    return PROMPT




def prompt_cut_co2_fire_extinguisher(image_url):
    PROMPT =  "Detect all co2 fire extinguisher and its handle, hose in the image. " + \
    "Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", " + \
    "and the text label in the key \"label\". Use descriptive labels."
    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(
            content=[
                {"type": "image_url", "image_url": image_url}
            ]
        )
    ]
    return messages

def prompt_cut_dry_chemical_fire_extinguisher(image_url):
    PROMPT = "Detect all dry chemical fire extinguishers and its hose in the image. " + \
    "Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", " + \
    "and the text label in the key \"label\". Use descriptive labels."
    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(
            content=[
                {"type": "image_url", "image_url": image_url}
            ]
        )
    ]
    return messages

def prompt_cut_pressure_gauge_fire_extinguisher(image_url):
    PROMPT = "Detect pressure gauge in the image. " + \
    "Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", " + \
    "and the text label in the key \"label\". Use descriptive labels."
    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(
            content=[
                {"type": "image_url", "image_url": image_url}
            ]
        )
    ]
    return messages

def prompt_cut_tray_fire_extinguisher(image_url):
    PROMPT = "Detect fire extinguisher tray in the image. " + \
    "Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", " + \
    "and the text label in the key \"label\". Use descriptive labels."
    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(
            content=[
                {"type": "image_url", "image_url": image_url}
            ]
        )
    ]
    return messages

def prompt_5s_fire_extinguisher_cabinet(list_images):
    PROMPT = """
You are an expert in 5S inspection for fire extinguisher cabinets. For each image of a fire extinguisher cabinet I provide, analyze and return a JSON object with the following 5S criteria (use only English terms):

1. **Sort:** Are there only necessary firefighting items in the cabinet? Are there any unnecessary or unrelated objects?
2. **Set in order:** Always set the status to "OK" as long as the items are generally organized and not in obvious disorder. Perfection is NOT required; for example, a hose that is coiled but not perfectly round is still OK.
3. **Shine:** Is the cabinet and all equipment inside clean, free from dust, stains, or rust?
4. **Standardize:** Is the tidy and clean state maintained regularly? Are the items checked and maintained periodically?
5. **Sustain:** Are all items ready for use? Do people follow the rules and keep the cabinet in good condition?

**Requirements:**
- Return ONLY a single JSON object with 5 fields: `sort`, `set_in_order`, `shine`, `standardize`, `sustain`.
- Each field is an object with:
  - `status`: "OK" or "NG"
  - `reason`: A very detailed explanation in English, specifying exactly which part is OK or which part is NG and why (e.g., "There is dust on the bottom of the cabinet", "A hammer is missing", "Fire extinguisher is not in the correct position", etc.).
- For `set_in_order`, always set `status` to "OK" and explain that the arrangement is generally acceptable even if not perfect.

**Example JSON:**
{
  "sort": {"status": "OK", "reason": "Only necessary firefighting equipment is present in the cabinet."},
  "set_in_order": {"status": "OK", "reason": "All items are generally organized and accessible, although not perfectly aligned. The hose is coiled but not perfectly round, which is acceptable."},
  "shine": {"status": "OK", "reason": "All items and the cabinet are clean, no dust or rust found."},
  "standardize": {"status": "NG", "reason": "There is no inspection tag and the cabinet appears not to be checked regularly."},
  "sustain": {"status": "OK", "reason": "All equipment is ready for use and properly maintained."}
}

**IMPORTANT:**  
- Respond ONLY with the JSON object as above.  
- Do NOT add any explanations, markdown, or code blocks.

Below are the image URLs:
""" + "\n".join(list_images)
    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(
            content=[
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
    ]
    return messages

def prompt_electric_6s(list_images):
    PROMPT = """
You are an expert in 6S evaluation (Sort, Set in order, Shine, Safety, Standardize, Sustain) for electrical cabinets based on images. I will provide several images of an electrical cabinet. Your task is to evaluate the cabinet according to each of the 6S criteria below.

**Your evaluation must be based only on the information observable in the provided images.**

**For each criterion, return the result in the JSON format specified at the end of this prompt:**

1. **Seiri (Sort):** Rate as "OK" or "NG".
2. **Seiton (Set in order):** Rate as "OK" or "NG".
3. **Seiso (Shine):** Rate as "OK" or "NG".
4. **Safety:** Rate as "OK" or "NG" based on these factors: Cabinet door (evaluate if open or closed; for the last two images, specifically evaluate the door and safety lock), Safety lock (for the last two images, specifically evaluate the lock; regular latches are acceptable), Grounding wire.
5. **Seiketsu (Standardize):** Always rate as "OK".
6. **Shitsuke (Sustain):** Always rate as "OK".
7. **Summary:** Rate as "OK" or "NG".

**Important notes:**
- If any criterion is rated "NG", add a field `"Error details"` for that criterion.
- Each element in `"Error details"` must have 3 fields: `"Reason"`, `"Error object"`, `"Image URL"`:
    - `"Reason"`: A short, clear explanation in English (e.g., "The tangled wire is under the corner of the cabinet").
    - `"Error object"`: A noun phrase in English describing the specific object causing the error, including its position or state (e.g., "Tangled wires at bottom corner", "Unlabeled wires at top").
    - `"Image URL"`: Use the exact image URL provided. If you cannot determine which image corresponds to the error, leave this field empty.
- If there are multiple errors for a criterion, list each error as a separate object in the `"Error details"` array.
- Do not combine multiple errors into one string or object.
- If a criterion is "OK", do not include the `"Error details"` field.
- If the images are not of the same cabinet, set "Summary" to "NG" with reason "Images are not consistent".
- If any of Seiri, Seiton, Seiso, or Safety is "NG", "Summary" must be "NG".
- "Summary" can only be "OK" if all of Seiri, Seiton, Seiso, and Safety are "OK". Seiketsu and Shitsuke are always "OK".

**Format Response: (no explanations, markdown, or code blocks, and response in English):**

```json
{
    "data": [
        {
            "Criterion": "Seiri - Sort", 
            "Result": "OK" or "NG", 
            "Error details": "If any"
        },
        {
            "Criterion": "Seiton - Set in order",
            "Result": "NG",
            "Error details": [
                {
                "Reason": "Tangled wires at bottom corner",
                "Error object": "Tangled wires at bottom corner",
                "Image URL": "https://.../image1.jpg"
                },
                {
                "Reason": "Unlabeled wires at top",
                "Error object": "Unlabeled wires at top",
                "Image URL": "https://.../image2.jpg"
                }
            ]
        },
        {
            "Criterion": "Seiso - Shine", 
            "Result": "OK" or "NG", 
            "Error details": "If any"
        },
        {
            "Criterion": "Safety", 
            "Result": "OK" or "NG", 
            "Error details": "If any"
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
            "Result": "NG" or "OK",
            "Reason": "Reason if NG"
        }
    ]
}
```

**Note:**  
- Make sure to return a valid JSON object as above. If you cannot return a valid JSON, report an error.
- In case of missing required objects (e.g., no grounding wire, no safety lock), leave `"Error object"` and `"Image URL"` empty.

Example:
{
"Criterion": "Safety",
"Result": "NG",
"Error details": [
    {
    "Reason": "No grounding wire",
    "Error object": "",
    "Image URL": ""
    }
]
}

"""
    contents = []
    for url in list_images:
        contents.append({"type": "text", "text": f"This image: {url}"})
        contents.append({"type": "image_url", "image_url": {"url": url}})

    messages = [
        SystemMessage(content=PROMPT),
        HumanMessage(
            content=contents
        )
    ]
    return messages


def prompt_check_list(list_images, inspection_location, inspection_items_details, inspection_methods_standards):
    messages = [
        SystemMessage(content="""You are an equipment inspection engineer. I will provide you with the following information:
    **Requirement:** All reasons must be answered in English, detailed and complete. You MUST answer in English.

    Inspection location: [location of inspection]

    Inspection items & details: [inspection items and target values]

    Inspection methods & standards: [how the inspection is performed and what standards to follow]

    Image: [photo of the equipment]

    Please evaluate and respond in the following format:

    Result: OK / Not OK

    Reason: Briefly explain why you chose that result, based on the image and inspection criteria

Please evaluate and respond ONLY with a valid JSON object in the following format (do NOT add explanations, markdown, or code blocks):

{
  "result": "OK" or "Not OK",
  "reason": "[Provide a very detailed answer, listing all findings, issues, or confirmations for each inspection item, clearly referencing the standards and the images (describe only, DO NOT include any image links in the reason). Clearly state the location, severity, cause, and consequence (if any) for each issue. DO NOT insert or mention any image links in the reason.]",
  "url_image": "<all of the input image URLs above>"
}

Below are the image URLs:
""" + "\n".join(list_images)),
        HumanMessage(
            content=[
                {"type": "text", "text": f"""Inspection location: {inspection_location};
Inspection items & details: {inspection_items_details};
Inspection methods & standards: {inspection_methods_standards};"""},
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
    ]
    return messages