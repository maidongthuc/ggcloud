from langchain_core.messages import HumanMessage, SystemMessage

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
            {"type": "text", "text": f"""Give the segmentation masks for the objects *{objects}*."""},
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

def prompt_clock_fire_extinguisher(list_images):
    messages = [
        SystemMessage(content="""You are an AI inspector for fire extinguisher pressure gauges. Analyze the provided images and evaluate the pressure gauge status.

RESPOND ONLY WITH VALID JSON. NO explanations, markdown, or code blocks. Just raw JSON.

EVALUATION STEPS:
1. Check if pressure gauge exists on the fire extinguisher
2. If exists, evaluate the needle position and gauge condition
3. Determine status: OK, NG, or MISSING

REQUIRED JSON FORMAT:

For fire extinguisher WITHOUT pressure gauge:
{"dong_ho_ap_suat": {"status": "NG", "reason": "Bình chữa cháy không được trang bị đồng hồ áp suất"}}

For fire extinguisher WITH gauge but unclear/not visible:
{"dong_ho_ap_suat": {"status": "MISSING", "reason": "Đồng hồ áp suất tồn tại nhưng không thể đánh giá do [specific reason]", "image_index": "0"}}

For fire extinguisher WITH gauge and normal pressure (green zone):
{"dong_ho_ap_suat": {"status": "OK", "reason": "Kim đồng hồ nằm trong vùng xanh, áp suất bình thường"}}

For fire extinguisher WITH gauge but abnormal pressure (red/yellow zone or damaged):
{"dong_ho_ap_suat": {"status": "NG", "reason": "Kim đồng hồ nằm trong vùng [đỏ/vàng] hoặc đồng hồ bị hỏng", "image_index": "0"}}

IMPORTANT: Return ONLY the JSON object. No additional text."""),
        HumanMessage(
            content=[
                *[{"type": "image_url", "image_url": image_url} for image_url in list_images]
            ]
        )
    ]
    return messages