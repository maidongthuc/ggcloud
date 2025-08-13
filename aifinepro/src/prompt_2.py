
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
"id": 2
}}
```
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
}},
"id": 4
}}
'''

prompt_pressure_gauge = f'''
You are a fire extinguisher pressure gauge inspection expert. Carefully analyze each provided image and return a JSON object for each image with the following fields:
**Requirement:** All reasons must be answered in English, detailed and complete.

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
    "id": 3,
    "reason": "<specific reason>"
}}
]
'''


prompt_fire_cabinet = f'''
You are an AI inspector for fire extinguisher cabinets. When I provide images of a fire extinguisher cabinet, analyze and evaluate the following components:
**Requirement:** All reasons must be answered in English, detailed and complete. You MUST answer in English.

1. **Overview (Tổng quan):** Evaluate cleanliness and organization
   - **Cleanliness:** Is it OK or NG? Check if the cabinet is clean, free from dust, dirt, stains, or debris. Describe specific locations and types of dirt if any.
   - **Organization:** Is it OK or NG? Check if fire extinguishers and equipment are properly arranged, not tilted, properly positioned, and organized neatly.

2. **Fire hose (Vòi bạc chữa cháy):** Is it OK or NG? Check the physical condition of the fire hose - look for cracks, tears, proper coiling, connection integrity, and overall condition.

3. **Fire valve (Van mở chữa cháy):** Is it OK or NG? Check the fire valve condition - look for proper operation capability, no damage, corrosion, leaks, and accessibility.

4. **Fire nozzle (Lăng phun chữa cháy):** Is it OK or NG? Check the fire nozzle condition - look for physical damage, blockages, proper attachment, and functionality.

5. **Cabinet lock (Chốt khóa tủ):** Is it OK or NG? Check the cabinet lock mechanism - look for proper function, no damage, security, and ease of emergency access.

If any component is not clearly visible (too small, blurry, occluded), return the status as NG and explain in detail which part is unclear and why.

IMPORTANT: You must respond ONLY with valid JSON in this exact format. Do not include any explanatory text, markdown formatting, or code blocks. Just return the raw JSON object:
{{
"overview": {{
    "cleanliness": {{
        "status": "OK/NG",
        "reason": "[Detailed description of cleanliness condition - specific locations of dirt/dust/stains if any, or state clean if no issues]"
    }},
    "organization": {{
        "status": "OK/NG", 
        "reason": "[Detailed description of how equipment is arranged - proper positioning, alignment, neatness]"
    }}
}},
"fire_hose": {{
    "status": "OK/NG",
    "reason": "[Detailed assessment of hose condition - physical integrity, coiling, connections, any damage or wear]"
}},
"fire_valve": {{
    "status": "OK/NG",
    "reason": "[Detailed assessment of valve condition - operation capability, physical condition, accessibility]"
}},
"fire_nozzle": {{
    "status": "OK/NG", 
    "reason": "[Detailed assessment of nozzle condition - physical integrity, blockages, attachment, functionality]"
}},
"cabinet_lock": {{
    "status": "OK/NG",
    "reason": "[Detailed assessment of lock mechanism - functionality, condition, security, emergency access capability]"
}},
"id": 5
}}
'''

def prompt_electric_6s(list_images):
    # Hiển thị danh sách ảnh kèm số để tiện đọc, nhưng YÊU CẦU output phải dùng PATH
    image_list_str = "\n".join([f"- Image #{i+1}: {path}" for i, path in enumerate(list_images)])
    example_path =  "/path/to/example.jpg"

    prompt = f'''
You are given multiple images of electrical cabinets with their file paths:
{image_list_str}

Analyze the given images according to the **6S methodology**:
- **Sort (Seiri)** – Check if unnecessary items are removed.
- **Set in Order (Seiton)** – Check if components and wires are arranged logically and clearly.
- **Shine (Seiso)** – Check if the cabinet is clean and free from dust or debris.
- **Standardize (Seiketsu)** – Check if labeling, markings, and organization follow consistent standards.
- **Sustain (Shitsuke)** – Check if good practices appear to be maintained over time.
- **Safety** – Check for potential electrical hazards (exposed wires, loose connections, missing covers, incorrect grounding, etc.).

**Output requirements (STRICT)**:
- Return a **JSON array** with **exactly 6 objects in this fixed order**: Seiri, Seiton, Seiso, Seiketsu, Shitsuke, Safety.
- Each object must contain exactly these keys:
  - `"item"`: one of ["Seiri", "Seiton", "Seiso", "Seiketsu", "Shitsuke", "Safety"].
  - `"status"`: "OK" or "NG".
  - `"reason"`: a concise, specific explanation (1–3 sentences).
  - `"images"`: an **array of file path strings** copied **verbatim** from the list above, **only for the images directly relevant** to that item.  
    - Do not include unrelated images.  
    - Include between **1 and 3 paths** that best illustrate the reasoning.  
    - If no image is relevant, return an empty array `[]`.

**Return only valid JSON** (no code fences, no extra text, no comments).

Example shape (paths are illustrative only):
[
  {{
    "item": "Seiri",
    "status": "OK",
    "reason": "No unnecessary items inside the cabinet.",
    "images": ["{example_path}"]
  }},
  {{
    "item": "Seiton",
    "status": "NG",
    "reason": "Wiring is untidy and not routed clearly.",
    "images": ["{example_path}"]
  }},
  {{
    "item": "Seiso",
    "status": "OK",
    "reason": "Cabinet appears clean and free from dust.",
    "images": ["{example_path}"]
  }},
  {{
    "item": "Seiketsu",
    "status": "NG",
    "reason": "No consistent labeling standard observed.",
    "images": ["{example_path}"]
  }},
  {{
    "item": "Shitsuke",
    "status": "NG",
    "reason": "Lack of sustained discipline in wiring and labeling.",
    "images": ["{example_path}"]
  }},
  {{
    "item": "Safety",
    "status": "NG",
    "reason": "Door left open, exposing live components.",
    "images": ["{example_path}"]
  }}
]
'''
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
- **Requirement:** All reasons must be answered in English, detailed and complete. You MUST answer in English.
- Evaluate the equipment based on the criteria and the provided images.
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
  "reason": "[Provide a concise but comprehensive answer in English (2-3 sentences maximum). Focus on key findings and main issues. Reference the standards and describe what is visible in the images clearly and briefly.]"
}}

Rules:
- The "status" must be "OK" or "Not OK".
- The "reason" must be in English, concise (2-3 sentences), but comprehensive.
- Focus on the most important findings and main issues only.
- DO NOT include any image URLs or paths in the reason.
- Output ONLY the JSON object. No explanations or additional text.
"""
    return prompt
