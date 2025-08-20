
prompt_cut_dry_chemical_fire_extinguisher_2 = "Detect the *dry chemical fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels."
prompt_cut_co2_fire_extinguisher_2 = "Detect the *co2 fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels."
prompt_cut_fire_extinguisher_2 = "Detect the *dry chemical fire extinguisher* and *co2 fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format."
prompt_cut_hose_co2_extinguisher_2 = "Detect the *hose of co2 fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format such as *hose_of_co2_fire_extinguisher*."
prompt_cut_fire_extinguisher_tray_2 = "Detect the *double fire extinguisher tray* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format such as *double_fire_extinguisher_tray*."
prompt_cut_pressure_gauge_fire_extinguisher_2 = "Detect the *pressure gauge of fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format such as *pressure_gauge*."
prompt_system_cut_fire_extinguisher_2 = "Large dry chemical fire extinguishers are bigger than co2 fire extinguishers."
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
    return PROMPT

def detection_object(list_label):
    # Wrap each object with **object**
    wrapped_objects = [f"**{label}**" for label in list_label]
    objects = ", ".join(wrapped_objects)
    prompt = f"""- Detect the {objects} in the image.  
- Output the result as a **JSON list** of bounding boxes, where each entry contains:
  - `box_2d`: [y1, x1, y2, x2]
  - `label`: object name in `snake_case` format."""
    return prompt
# def prompt_cut_all_fire_extinguisher(url_image):
#     prompt = "If image is overview photo of the fire extinguisher:" \
# " - Detect the *dry chemical fire extinguisher*, *co2 fire extinguisher* and  *fire extinguisher tray* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format." \
# "If image is photo of the fire extinguisher pressure gauge:" \
# " - Detect the *pressure gauge of fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format."

#     messages = [
#       {
#         "role": "user",
#         "content": [
#           {
#             "type": "text",
#             "text": prompt
#           },
#           {
#             "type": "image_url",
#             "image_url": {
#               "url": url_image
#             }
#           }
#         ]
#       }
#     ]
#     return messages

def prompt_cut_all_fire_extinguisher(image_base64):
    prompt = """## If the image is an overview photo of the fire extinguisher:
- Only detect the **dry chemical fire extinguisher**, **co2 fire extinguisher**, and **co2 fire extinguisher hose** in the image.  
- Output the result as a **JSON list** of bounding boxes, where each entry contains:
  - `box_2d`: [y1, x1, y2, x2]
  - `label`: object name in `snake_case` format.

## If the image is a photo of the fire extinguisher pressure gauge:
- Detect the **pressure gauge of fire extinguisher** in the image.  
- Output the result as a **JSON list** of bounding boxes, where each entry contains:
  - `box_2d`: [y1, x1, y2, x2]
  - `label`: object name in `snake_case` format."""
 
    messages = [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"  # Sử dụng data URL format
            }
            }
        ]
      }
    ]
    return messages

prompt_fire_extinguisher = f'''
You are an AI inspector for fire extinguishers. When I provide an image about fire extinguishers, focus and analyze the following components:

**Language requirement**
- All field names and non-reason comments/instructions are in **English**.
- For every **reason** field, return a **4-language object** with **exact keys**: "en", "vi", "zh-CN", "zh-TW".
- Return **JSON only** (no extra text before/after).

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


```json
{{
  "body": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed reason in English about physical condition only]",
      "vi": "[Bản dịch Tiếng Việt]",
      "zh-CN": "[简体中文翻译]",
      "zh-TW": "[繁體中文翻譯]"
    }}
  }},
  "handle": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed reason in English about physical condition only]",
      "vi": "[Bản dịch Tiếng Việt]",
      "zh-CN": "[简体中文翻译]",
      "zh-TW": "[繁體中文翻譯]"
    }}
  }},
  "safety_pin": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed reason in English about physical condition only]",
      "vi": "[Bản dịch Tiếng Việt]",
      "zh-CN": "[简体中文翻译]",
      "zh-TW": "[繁體中文翻譯]"
    }}
  }},
  "nozzle": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed reason in English about physical condition only]",
      "vi": "[Bản dịch Tiếng Việt]",
      "zh-CN": "[简体中文翻译]",
      "zh-TW": "[繁體中文翻譯]"
    }}
  }},
  "cleanliness": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed multi-part cleanliness summary by component; if clean, 'All parts are clean']",
      "vi": "[Tóm tắt chi tiết độ sạch theo từng bộ phận; nếu sạch, 'Tất cả các bộ phận đều sạch']",
      "zh-CN": "[按部件给出清洁度细节；若干净则写：所有部件均干净]",
      "zh-TW": "[按部件給出清潔度細節；若乾淨則寫：所有部件均乾淨]"
    }},
  }}
}}
'''

prompt_fire_extinguisher_tray = f'''
You are an AI inspector for fire extinguisher trays. When I provide images of a tray designed to hold two fire extinguishers, analyze and evaluate the following:
**Requirement:** All reasons must be answered in English, detailed and complete. You MUST answer in English.

1. Tray condition: Is it OK or NG? Clearly state the specific and detailed reason based on the image (e.g., "the tray is cracked at the right corner", "the tray is dented", "the tray is rusty", "the tray is punctured", ...). Only focus on physical damage or defects, do NOT mention cleanliness or dirt.
2. Capacity: Is the tray suitable for holding two fire extinguishers? State "OK" if it can securely hold two extinguishers, "NG" if not, and explain the reason (e.g., "the tray only has space for one extinguisher", "the tray is tilted and cannot hold the extinguishers", ...).
3. Cleanliness: Set "cleanliness" to OK if the tray is clean. Set "cleanliness" to NG if the tray is dirty, dusty, or stained. In the "reason" for cleanliness, clearly describe all dirty, dusty, or stained areas and specify the type of dirt and the exact location (e.g., "dust in the left corner of the tray", "black stain at the bottom of the tray", ...). If the tray is clean, state "The tray is clean".

If any part of the tray is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

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
}}
}}
'''

prompt_pressure_gauge = f'''
You are a fire extinguisher pressure gauge inspection expert. Carefully analyze each provided image and return a JSON object for each image with the following fields:

**Language requirement**
- For every "reason", return a 4-language object with exact keys: "en", "vi", "zh-CN", "zh-TW".
- Write the English explanation first, then provide faithful translations for the other languages.
- Return JSON only (no extra text before/after).

- status: "OK" if the needle is in the green zone, "NG" if in the red/yellow zone or no gauge.
- url_image: exactly the same image URL from the list below.
- id: always set to 3.
- reason: explain clearly why you chose the status (e.g., needle position, no gauge, etc.).

**Important:**  
- Even if the image is dark, blurry, or low quality, do your best to analyze and determine the needle position.  
- Only return "NG" for image quality if it is truly impossible to see the gauge or needle at all.  
- If the image is dark but the needle can still be seen, make your best judgment and explain your reasoning.

ALWAYS return a JSON array, one object per image, in the following format (no explanations, markdown, or code blocks):

[
  {{
    "status": "OK/NG",
    "url_image": "<exact URL from the list>",
    "id": 3,
    "reason": {{
      "en": "<Specific English reason with needle zone/position or why not visible>",
      "vi": "<Bản dịch tiếng Việt tương ứng>",
      "zh-CN": "<对应的简体中文说明>",
      "zh-TW": "<對應的繁體中文說明>"
    }}
  }}
]
'''


prompt_fire_cabinet = f'''
prompt_fire_cabinet = f"""
You are an AI inspector for fire extinguisher cabinets.

**Language requirement**
- For every "reason", return a 4-language object with exact keys: "en", "vi", "zh-CN", "zh-TW".
- Write the English explanation first, then provide accurate translations in Vietnamese, Simplified Chinese, and Traditional Chinese.
- Return only valid JSON (no markdown, no code blocks, no explanatory text).

When I provide images of a fire extinguisher cabinet, analyze and evaluate the following components:

1. **Overview (Tổng quan)**  
   - **Cleanliness:** Is it OK or NG? Check if the cabinet is clean, free from dust, dirt, stains, or debris. Describe specific locations and types of dirt if any.  
   - **Organization:** Is it OK or NG? Check if fire extinguishers and equipment are properly arranged, not tilted, properly positioned, and organized neatly.  

2. **Fire hose (Vòi bạc chữa cháy):** Is it OK or NG? Check the physical condition of the fire hose - cracks, tears, proper coiling, connection integrity, and overall condition.  

3. **Fire valve (Van mở chữa cháy):** Is it OK or NG? Check the fire valve condition - operation capability, no damage, corrosion, leaks, and accessibility.  

4. **Fire nozzle (Lăng phun chữa cháy):** Is it OK or NG? Check the fire nozzle condition - physical damage, blockages, proper attachment, and functionality.  

5. **Cabinet lock (Chốt khóa tủ):** Is it OK or NG? Check the cabinet lock mechanism - proper function, no damage, security, and ease of emergency access.  

**Visibility rule**  
If any component is not clearly visible (too small, blurry, occluded), return status = NG and explain clearly in the "reason" which part is unclear and why.

**Output format (strict JSON, one object only):**
{{
  "overview": {{
    "cleanliness": {{
      "status": "OK/NG",
      "reason": {{
        "en": "[Detailed cleanliness assessment in English]",
        "vi": "[Bản dịch tiếng Việt]",
        "zh-CN": "[简体中文翻译]",
        "zh-TW": "[繁體中文翻譯]"
      }}
    }},
    "organization": {{
      "status": "OK/NG",
      "reason": {{
        "en": "[Detailed organization assessment in English]",
        "vi": "[Bản dịch tiếng Việt]",
        "zh-CN": "[简体中文翻译]",
        "zh-TW": "[繁體中文翻譯]"
      }}
    }}
  }},
  "fire_hose": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed hose condition assessment in English]",
      "vi": "[Bản dịch tiếng Việt]",
      "zh-CN": "[简体中文翻译]",
      "zh-TW": "[繁體中文翻譯]"
    }}
  }},
  "fire_valve": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed valve condition assessment in English]",
      "vi": "[Bản dịch tiếng Việt]",
      "zh-CN": "[简体中文翻译]",
      "zh-TW": "[繁體中文翻譯]"
    }}
  }},
  "fire_nozzle": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed nozzle condition assessment in English]",
      "vi": "[Bản dịch tiếng Việt]",
      "zh-CN": "[简体中文翻译]",
      "zh-TW": "[繁體中文翻譯]"
    }}
  }},
  "cabinet_lock": {{
    "status": "OK/NG",
    "reason": {{
      "en": "[Detailed lock condition assessment in English]",
      "vi": "[Bản dịch tiếng Việt]",
      "zh-CN": "[简体中文翻译]",
      "zh-TW": "[繁體中文翻譯]"
    }}
  }}
}}
"""

'''

def prompt_electric_6s(list_images):
    # Hiển thị danh sách ảnh kèm số để tiện đọc, NHƯNG yêu cầu output phải dùng đúng PATH
    image_list_str = "\n".join([f"- Image #{i+1}: {path}" for i, path in enumerate(list_images, start=1)])

    prompt = f"""Bạn là một **chuyên gia kiểm tra an toàn điện** chuyên về **phương pháp 6S** cho tủ điện công nghiệp.  
Hãy phân tích các hình ảnh được cung cấp và đánh giá sự tuân thủ theo các điều kiện tiêu chuẩn 6S.  
Bạn được cung cấp nhiều hình ảnh tủ điện với đường dẫn tệp như sau:

{image_list_str}

---

## Nội dung cần kiểm tra

### 1) Seiri (Sàng lọc)
-Xem xét và loại bỏ các vật dụng thừa trong tủ điện, như dây dẫn cũ, linh kiện hỏng hoặc công cụ không cần thiết.

### 2) Seiton (Sắp xếp)
- Sắp xếp những thứ cần thiết theo thứ tự ngăn nắp và có biểu thị dễ thấy, dễ lấy trong tủ điện
- Sắp xếp đúng vật vào đúng chỗ trong tủ điện
- Sắp xếp vị trí các công cụ,… sao cho tiến trình làm việc trôi chảy trong tủ điện

### 3) Seiso (Sạch sẽ)
- Giữ gìn nơi làm việc, thiết bị dụng cụ sạch sẽ trong tủ điện
- Hạn chế nguồn gây dơ bẩn, bừa bãi trong tủ điện
- Lau chùi, quét dọn có ý thức trong tủ điện

### 4) Seiketsu (Săn sóc)
- Duy trì thành quả đạt được
- Thực hiện 3S mọi lúc mọi nơi
- Duy trì nguyên tắc 3 không:
  • Không có vật vô dụng
  • Không bừa bãi
  • Không dơ bẩn

### 5) Shitsuke (Sẵn sàng)
- Tự giác thực hiện và duy trì 3S
- Hướng dẫn người chưa biết về 5S thực hiện 5S

### 6) Safety (An toàn)
- Không có cách điện bị hư hỏng, nứt hoặc cháy chảy.  
- Không có mối nối lỏng, đầu hở hoặc hàn kém.  
- Tất cả nắp che, tấm chắn và lớp bảo vệ được lắp đặt đầy đủ.  
- Tiếp địa đúng và hoạt động tốt.  
---

## Output format (JSON rules)
- Return exactly **6 objects** in this order: "Seiri", "Seiton", "Seiso", "Seiketsu", "Shitsuke", "Safety".
- Each object must have:
  - "item": one of the fixed values above.
  - "status": "OK" or "NG".
  - "reason": a **detailed** explanation (write 3–8 sentences) explicitly citing visible evidence and implications for safety/operations. Avoid generic phrases.
  - "defective_objects": **only if** status is "NG" → an array of objects; otherwise [].

### Defective object schema (no bounding boxes, minimal fields)
For each defective object, include **only**:
- "image_id": the **exact image path** as listed in the input.
- "label": object name (see Controlled Vocabulary below).  
No other fields are allowed. **Do not** output coordinates, polygons, masks, or any bbox fields.

**Return valid JSON only (no comments, no trailing commas, no markdown).**
**Use ASCII quotes only.**

---

## Controlled Vocabulary (labels)
Use these when applicable; otherwise create clear labels:
- "tangled cable bundle"
- "excess spare parts inside cabinet"
- "unrelated object inside cabinet"
- "debris inside cabinet"
- "missing label on breaker"
- "worn or unreadable label"
- "incorrect wire color code"
- "exposed conductor"
- "damaged insulation"
- "broken cable gland"
- "loose terminal connection"
- "missing cover or guard"
- "blocked_breaker access"
- "corrosion on terminal"
- "moisture sign inside cabinet"
- "overheating discoloration"

---

## Example Output
[
  {{
    "item": "Seiri",
    "status": "OK",
    "reason": "The cabinet interior appears dedicated to operational components with no unrelated tools, packing materials, or expired parts. Spare items are not stored inside the enclosure, reducing clutter and improving airflow. Shelves and DIN rails are populated only with necessary devices for control and protection, indicating disciplined inventory control. No bundles of unused wires or coils suggesting temporary storage are visible.",
    "defective_objects": []
  }},
  {{
    "item": "Seiton",
    "status": "NG",
    "reason": "Cable routing shows several uncontrolled loops that cross device fronts, suggesting the absence of ties or guides. The layout does not consistently follow power flow or functional grouping, making tracing circuits difficult. Access to certain breaker toggles appears partially obstructed by cable bundles, which can delay emergency isolation. This arrangement increases the chance of accidental actuation and complicates troubleshooting, violating good order principles.",
    "defective_objects": [
      {{
        "image_id": "/path/to/example.jpg",
        "label": "tangled_cable_bundle"
      }}
    ]
  }},
  {{
    "item": "Seiso",
    "status": "OK",
    "reason": "Surfaces and device faces appear free of dust and oil residue, indicating recent cleaning. No loose screws, clipped wire ends, or paper scraps are visible on the cabinet floor. Metallic parts show a consistent finish without staining, and ventilation cutouts look unobstructed. The overall cleanliness reduces the risk of thermal buildup and tracking across contaminants.",
    "defective_objects": []
  }},
  {{
    "item": "Seiketsu",
    "status": "NG",
    "reason": "Not all protective devices carry durable identification labels that match a documented diagram. Several positions display blank spaces where circuit IDs should be placed, which hinders rapid isolation and re-energization. Inconsistent label materials and fonts suggest a lack of standardized labeling practice. This inconsistency increases the risk of human error during maintenance and emergency operations.",
    "defective_objects": [
      {{
        "image_id": "/path/to/example2.jpg",
        "label": "missing_label_on_breaker"
      }}
    ]
  }},
  {{
    "item": "Shitsuke",
    "status": "OK",
    "reason": "Cable dressing and terminal torque marks appear consistent, implying adherence to routine checks. No leftover consumables or temporary markers remain, suggesting work areas were restored after interventions. The uniformity of labeling where present indicates ongoing discipline. Visual cues collectively imply sustained housekeeping and periodic verification.",
    "defective_objects": []
  }},
  {{
    "item": "Safety",
    "status": "NG",
    "reason": "A conductor appears exposed at a terminal interface, with insulation stripped too far back from the clamping point. The visible metallic strands present accidental contact and arcing risks, especially under vibration. Missing heat-shrink or strain relief indicates inadequate termination practice. Such defects can lead to localized heating, oxidation, and eventual equipment failure or shock hazards.",
    "defective_objects": [
      {{
        "image_id": "/path/to/example2.jpg",
        "label": "exposed_conductor"
      }}
    ]
  }}
]
"""
    return prompt

def prompt_electric_seiton(list_images):
    # Display image list with numbering, but REQUIRE that output must use the exact PATH
    image_list_str = "\n".join([f"- Image no {i+1}: {path}" for i, path in enumerate(list_images, start=1)])

    prompt = f"""You are an **expert electrical safety inspector** specializing in the **6S methodology** for industrial electrical cabinets.  
Analyze the provided images and **evaluate only under the Seiton (Set in Order) condition**.  
You are given multiple images of electrical cabinets with their file paths:

{image_list_str}
---
## Inspection criteria (Seiton – Set in Order)
- **Only evaluate necessary equipment/components for the electrical cabinet** (devices, components, cables, related accessories).  
  → **Ignore** unrelated items such as water bottles, pliers/hammers for personal use, gloves, papers, tape… (these belong to **Seiri – Sort**, not Seiton).
- Components, devices, and wiring must be **arranged neatly and logically**, ensuring safe and convenient operation.  
- Cables must be routed through **trays/conduits/ducts** or **tied neatly with cable ties**; avoid tangling or overlapping.  
- Accessories/components must be **placed in their designated positions**, facilitating operation and maintenance.  
- There must be **clear position markings/labels/indicators** to ensure easy identification and traceability.  

*Note:* If an **unrelated object** (e.g., a water bottle) is found inside/on the cabinet, you should **briefly mention in the "reason" that this is a Seiri issue**, but **do not list it in the `defective_objects` of Seiton**.
---

## Output format (JSON rules)
- Return exactly **1 object** with:
  - "item": always "Seiton".
  - "status": "OK" or "NG".
  - "reason": **clear and concise explanation (2–4 sentences)**, describing evidence in the image and its impact on safety/operation.  
  - "defective_objects": **only when status = "NG"** → an array of objects describing **Seiton-related arrangement defects of necessary items**; otherwise, return [].

### Defective object schema (Seiton-only)
Each object must include:
- "image_id": exact image path from input.
- "label": specific defect name (e.g., "tangled cable bundle", ...).  

---

## Example Output
{{
  "item": "Seiton",
  "status": "NG",
  "reason": "Several cable bundles are left untied and not routed in trays, which obstructs operation and makes maintenance difficult.",
  "defective_objects": [
    {{
      "image_id": "/path/to/cabinet_with_tangled_cables.jpg",
      "label": "tangled cable bundle"
    }}
  ]
}}
"""
    return prompt


def prompt_electric_seiton_2(list_images):
    # Display image list with numbering, but REQUIRE that output must use the exact PATH
    image_list_str = "\n".join([f"- Image no {i+1}: {path}" for i, path in enumerate(list_images, start=1)])

    prompt = f"""You are an **expert electrical safety inspector** specializing in the **6S methodology** for industrial electrical cabinets.  
Analyze the provided images and **evaluate only under the Seiton (Set in Order) condition**.  
You are given multiple images of electrical cabinets with their file paths:

{image_list_str}

---
## Inspection criteria (Seiton – Set in Order)
- **Only check if there are tangled cables inside the cabinet.**  
- If tangled cables are found → status = "NG".  
- If no tangled cables are found → status = "OK".  

---
## Output format (JSON rules)
- Return exactly **1 object** with:
  - "item": always "Seiton".
  - "status": "OK" or "NG".
  - "reason": must be an object with 4 language keys: "en", "vi", "zh-CN", "zh-TW".  
    - Each explanation should be concise (2–3 sentences) describing the evidence in the image and its impact.  
  - "defective_objects": 
    - If status = "NG": array with at least one object describing `"tangled cable bundle"`.  
    - If status = "OK": return [].

### Defective object schema
Each object must include:
- "image_id": exact image path from input.
- "label": must be "tangled cable bundle".  

---
## Example Outputs

### Case 1: Tangled cables detected
{{
  "item": "Seiton",
  "status": "NG",
  "reason": {{
    "en": "Several cable bundles inside the cabinet are tangled and not tied properly, which obstructs maintenance and may cause accidental damage.",
    "vi": "Nhiều bó dây trong tủ bị rối và không được buộc gọn, gây cản trở việc bảo trì và có thể dẫn đến hư hỏng ngoài ý muốn.",
    "zh-CN": "机柜内有多组电缆捆绑在一起且未妥善固定，妨碍维护并可能造成意外损坏。",
    "zh-TW": "機櫃內有多組電纜纏繞在一起且未妥善固定，妨礙維護並可能造成意外損壞。"
  }},
  "defective_objects": [
    {{
      "image_id": "/path/to/cabinet_with_tangled_cables.jpg",
      "label": "tangled cable bundle"
    }}
  ]
}}

### Case 2: No tangled cables
{{
  "item": "Seiton",
  "status": "OK",
  "reason": {{
    "en": "All cable bundles inside the cabinet are neatly routed and secured, ensuring clear access and safe operation.",
    "vi": "Tất cả các bó dây trong tủ được sắp xếp gọn gàng và cố định chắc chắn, đảm bảo việc tiếp cận dễ dàng và vận hành an toàn.",
    "zh-CN": "机柜内所有电缆捆绑均布置整齐并牢固固定，确保清晰的通道和安全运行。",
    "zh-TW": "機櫃內所有電纜捆綁均佈置整齊並牢固固定，確保清晰的通道和安全運行。"
  }},
  "defective_objects": []
}}
"""
    return prompt


def prompt_electric_seiso(list_images):
    # Display image list with numbering, but REQUIRE that output must use the exact PATH
    image_list_str = "\n".join([f"- Image no {i+1}: {path}" for i, path in enumerate(list_images, start=1)])

    prompt = f"""You are an **expert electrical safety inspector** specializing in the **6S methodology** for industrial electrical cabinets.  
Analyze the provided images and **evaluate only under the Seiso (Shine/Cleanliness) condition**.  
You are given multiple images of electrical cabinets with their file paths:

{image_list_str}

---
## Inspection criteria (Seiso – Cleanliness)
- Focus **only on areas with clearly visible and accumulated dust**.  
- Small, light, or negligible dust should be ignored (do not report as NG).  
- If significant dust accumulation is found → status = "NG".  
- If the cabinet looks generally clean or only has minor dust → status = "OK".  

---
## Output format (JSON rules)
- Return exactly **1 object** with:
  - "item": always "Seiso".
  - "status": "OK" or "NG".
  - "reason": must be an object with 4 language keys: "en", "vi", "zh-CN", "zh-TW".
    - Each explanation should be concise (2–3 sentences) describing the evidence in the image, the area where dust is clearly visible, and its impact.
  - "defective_objects": 
    - If status = "NG": array with one or more objects.  
    - If status = "OK": return [].

### Defective object schema
Each object must include:
- "image_id": exact image path from input.
- "label": must describe **dust and its location** (e.g., "dust bottom of cabinet", "dust on circuit breaker surfaces", "dust near cooling fan").  

---
## Example Outputs

### Case 1: Heavy dust detected
{{
  "item": "Seiso",
  "status": "NG",
  "reason": {{
    "en": "Heavy dust is accumulated at the bottom of the cabinet and along the lower rails. The buildup indicates inadequate cleaning and may impair airflow or deposit on contacts.",
    "vi": "Bụi dày tích tụ ở đáy tủ và dọc các thanh ray phía dưới. Sự tích tụ này cho thấy việc vệ sinh chưa đạt yêu cầu và có thể cản trở luồng khí hoặc bám lên các tiếp điểm.",
    "zh-CN": "机柜底部及下方导轨处有明显大量积尘。该堆积表明清洁不到位，可能影响气流或沉积到接触点上。",
    "zh-TW": "機櫃底部及下方導軌處有明顯大量積塵。此堆積顯示清潔不足，可能影響氣流或沉積於接點。"
  }},
  "defective_objects": [
    {{
      "image_id": "/path/to/cabinet_with_heavy_dust.jpg",
      "label": "dust bottom of cabinet"
    }}
  ]
}}

### Case 2: Only light dust
{{
  "item": "Seiso",
  "status": "OK",
  "reason": {{
    "en": "The cabinet appears generally clean with only light surface dust on non-critical areas. The minor dust does not affect operation or safety.",
    "vi": "Tủ nhìn chung sạch, chỉ có một lớp bụi mỏng trên các khu vực không quan trọng. Lượng bụi nhỏ này không ảnh hưởng đến vận hành hoặc an toàn.",
    "zh-CN": "机柜整体较为干净，仅在非关键区域有少量表面灰尘。该轻微积尘不影响运行或安全。",
    "zh-TW": "機櫃整體乾淨，僅在非關鍵區域有少量表面灰塵。這些輕微積塵不影響運行或安全。"
  }},
  "defective_objects": []
}}
"""
    return prompt


def prompt_electric_seiri(list_images):
    # Display image list with numbering, but REQUIRE that output must use the exact PATH
    image_list_str = "\n".join([f"- Image no {i+1}: {path}" for i, path in enumerate(list_images, start=1)])

    prompt = f"""You are an **expert electrical safety inspector** specializing in the **6S methodology** for industrial electrical cabinets.  
Analyze the provided images and evaluate only under the **Seiri (Sort)** condition.  
You are given multiple images of electrical cabinets with their file paths:

{image_list_str}
---
## Inspection criteria (Seiri – Sort)
- Focus on identifying and removing unnecessary items, equipment, or components inside the cabinet.  
- Do not consider paper, dust, small debris, or cleanliness-related issues.  
- Do not consider tangled or excess cables; only evaluate unnecessary components and devices.  
- Ensure only the necessary number of components and devices are kept; avoid surplus.  

---
## Output format (JSON rules)
- Return exactly **1 object** with:
  - "item": always "Seiri".
  - "status": "OK" or "NG".
  - "reason": must be an object with 4 language keys: "en", "vi", "zh-CN", "zh-TW".  
    - Each explanation should be concise but detailed (2–4 sentences), clearly stating the evidence in the image and its impact on safety/operation.  
  - "defective_objects": **only when status = "NG"** → an array of objects; otherwise, return [].

### Defective object schema
Each object must include:
- "image_id": exact image path from input.
- "label": specific name of the unnecessary object (e.g., "water bottle", "pliers", ...).  

---
## Example Outputs

### NG example (unnecessary item found)
{{
  "item": "Seiri",
  "status": "NG",
  "reason": {{
    "en": "A plastic water bottle is placed inside the cabinet next to the wiring. This item is unrelated to operation, can obstruct maintenance, and introduces contamination risk; it should be removed.",
    "vi": "Một chai nhựa được đặt trong tủ ngay cạnh hệ thống dây điện. Vật này không liên quan đến vận hành, có thể cản trở bảo trì và gây nguy cơ nhiễm bẩn; cần được loại bỏ.",
    "zh-CN": "在配电柜内靠近电线处放置了一个塑料瓶。该物品与操作无关，可能妨碍维护并带来污染风险，应予以清除。",
    "zh-TW": "在配電櫃內靠近電線處放置了一個塑膠瓶。此物品與操作無關，可能妨礙維護並帶來污染風險，應予以清除。"
  }},
  "defective_objects": [
    {{
      "image_id": "/path/to/cabinet_with_bottle.jpg",
      "label": "water bottle"
    }}
  ]
}}

### OK example (no unnecessary items)
{{
  "item": "Seiri",
  "status": "OK",
  "reason": {{
    "en": "No unrelated items or surplus parts are visible inside or on the cabinet. The contents appear limited to necessary electrical components only.",
    "vi": "Không phát hiện vật dụng không liên quan hoặc linh kiện dư thừa bên trong hoặc trên tủ điện. Nội dung trong tủ chỉ bao gồm các thiết bị điện cần thiết.",
    "zh-CN": "未见柜内或柜上存在无关物品或多余零件。内容仅限于必要的电气元件。",
    "zh-TW": "未見櫃內或櫃上存在無關物品或多餘零件。內容僅限於必要的電氣元件。"
  }},
  "defective_objects": []
}}
"""
    return prompt


def prompt_electric_safety(list_images):
    # Display image list with numbering, but REQUIRE that output must use the exact PATH
    image_list_str = "\n".join([f"- Image no {i+1}: {path}" for i, path in enumerate(list_images, start=1)])

    prompt = f"""You are an **expert electrical safety inspector** specializing in the **6S methodology** for industrial electrical cabinets.  
Analyze the provided images and evaluate only under the **Safety** condition.  
You are given multiple images of electrical cabinets with their file paths:

{image_list_str}

---
## Inspection criteria (Safety – Relaxed)
- Only report **clear and critical safety hazards**.  
- Minor or cosmetic issues should be ignored (do not mark as NG).  
- Safety hazards to check include:
  - Damaged or burned insulation on wires.  
  - Loose connections or exposed live wires.  
  - Missing or improperly installed covers, guards, or protective panels.  
  - Improper grounding/earthing.  

*(Note: Ignore the fact that the cabinet door is open for taking the photo; do not treat it as a hazard.)*  

If none of these clear hazards are found → status = "OK".  

---
## Output format (JSON rules)
- Return exactly **1 object** with:
  - "item": always "Safety".
  - "status": "OK" or "NG".
  - "reason": must be an object with 4 language keys: "en", "vi", "zh-CN", "zh-TW".  
    - Each explanation must be concise (2–3 sentences) describing the evidence and why it is (or is not) a serious hazard.  
  - "defective_objects": 
    - If status = "NG": array with one or more objects.  
    - If status = "OK": return [].

### Defective object schema
Each object must include:
- "image_id": exact image path from input.  
- "label": one of the key hazards, e.g., "exposed live wire", "loose connection", "damaged insulation", "missing protective cover", "improper grounding".  

---
## Example Outputs

### Case 1: Critical hazard detected
{{
  "item": "Safety",
  "status": "NG",
  "reason": {{
    "en": "A wire with damaged insulation is visible near the busbar, creating a risk of electric shock and possible short circuit.",
    "vi": "Một dây dẫn có lớp cách điện bị hư hỏng xuất hiện gần thanh cái, gây nguy cơ điện giật và có thể dẫn đến chập mạch.",
    "zh-CN": "母线附近可见一根绝缘损坏的电线，存在触电和可能短路的风险。",
    "zh-TW": "母線附近可見一條絕緣損壞的電線，存在觸電和可能短路的風險。"
  }},
  "defective_objects": [
    {{
      "image_id": "/path/to/cabinet_with_damaged_wire.jpg",
      "label": "damaged insulation"
    }}
  ]
}}

### Case 2: No critical hazard
{{
  "item": "Safety",
  "status": "OK",
  "reason": {{
    "en": "No serious safety issues detected. All wires are insulated, connections are secure, grounding is correct, and protective covers are in place.",
    "vi": "Không phát hiện vấn đề an toàn nghiêm trọng. Tất cả dây dẫn đều được cách điện, các mối nối chắc chắn, tiếp địa đúng và tấm che bảo vệ đã lắp đặt đầy đủ.",
    "zh-CN": "未发现严重的安全问题。所有电线均已绝缘，连接牢固，接地正确，保护盖已安装到位。",
    "zh-TW": "未發現嚴重的安全問題。所有電線均已絕緣，連接牢固，接地正確，保護蓋已安裝到位。"
  }},
  "defective_objects": []
}}
"""
    return prompt



def prompt_electric_s4_s5():
    prompt = """You are an **expert electrical safety inspector** specializing in the **6S methodology** for industrial electrical cabinets.  
Evaluate the conditions **Seiketsu (Standardize)** and **Shitsuke (Sustain/Discipline)**.  

---
## Inspection criteria
- For image-based inspection, Seiketsu and Shitsuke cannot be directly verified visually.  
- These two principles are more about **maintaining standards** and **discipline in long-term practices**.  
- Therefore, for visual cabinet checks, both Seiketsu and Shitsuke are always considered **OK**.  

---
## Output format (JSON rules)
Return exactly **2 objects** (one for Seiketsu, one for Shitsuke).  

Each object must have:
- "item": "Seiketsu" or "Shitsuke".  
- "status": always "OK".  
- "reason": short explanation (2–3 sentences) why it is considered OK.  

---
## Example Output
[
  {{
    "item": "Seiketsu",
    "status": "OK",
    "reason": "Standardization is ensured because cabinets follow consistent labeling, organization, and inspection practices. This criterion cannot be visually violated in a single image check."
  }},
  {{
    "item": "Shitsuke",
    "status": "OK",
    "reason": "Sustain is maintained by continuous training, discipline, and adherence to procedures, which are assumed to be followed. This is always marked as OK in visual inspections."
  }}
]
"""
    return prompt


def prompt_checklist(inspection_location, inspection_items_details, inspection_methods_standards):
    prompt = f"""
You are an equipment inspection engineer.

I will provide you with:
- Inspection location
- Inspection items & details
- Inspection methods & standards
- Image(s)

Your task:
- **Language requirement:** For every "reason", return a 4-language object with exact keys: "en", "vi", "zh-CN", "zh-TW".
- Always write the English explanation first, then provide translations in Vietnamese, Simplified Chinese, and Traditional Chinese.
- Output **ONLY** a valid JSON object (no extra text, no markdown, no code fences).

Inspection location: {inspection_location}

Inspection items & details:
{inspection_items_details}

Inspection methods & standards:
{inspection_methods_standards}

Evaluation format (STRICT):
Return ONLY a JSON object with exactly these keys:
{{
  "item": "{inspection_location}",
  "status": "OK" or "Not OK",
  "reason": {{
    "en": "[Concise but comprehensive explanation in English (2-3 sentences). Reference the standards and describe clearly what is visible in the images.]",
    "vi": "[Bản dịch Tiếng Việt ngắn gọn, đầy đủ]",
    "zh-CN": "[简体中文翻译，简明扼要]",
    "zh-TW": "[繁體中文翻譯，簡明扼要]"
  }}
}}

Rules:
- The "status" must be "OK" or "Not OK".
- Each "reason" must have 2–3 sentences maximum in English, then accurate translations.
- Focus only on the most important findings and main issues.
- DO NOT include any image URLs or file paths in the reason.
- Output ONLY the JSON object. No explanations or additional text.
"""
    return prompt

