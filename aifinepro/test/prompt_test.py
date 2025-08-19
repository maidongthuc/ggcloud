def prompt_electric_6s(list_images):
    # Hiển thị danh sách ảnh kèm số để tiện đọc, nhưng YÊU CẦU output phải dùng PATH
    image_list_str = "\n".join([f"- Image #{i+1}: {path}" for i, path in enumerate(list_images)])
    example_path =  "/path/to/example.jpg"

    prompt = f"""You are an **expert electrical safety inspector** specializing in the **6S methodology** for industrial electrical cabinets.  
Your task is to analyze the provided images and assess compliance with the following 6S standard conditions.  
You are given multiple images of electrical cabinets with their file paths:
{image_list_str}

---
### 1. Seiri (Sort)  
- Only keep equipment, components, and tools necessary for operation and maintenance.  
- No unrelated, broken, or expired components.  
- No unused cables, spare parts, or scrap stored inside the cabinet.  
- The quantity of necessary spare parts is correct and not excessive.  

### 2. Seiton (Set in Order)  
- All components and wiring are arranged logically, clearly, and accessibly.  
- Cables are routed neatly through proper trays or conduits, without tangling.  
- Equipment is arranged by function and power flow sequence.  
- Nothing blocks access to switches, breakers, or warning labels.  

### 3. Seiso (Shine)  
- No dust, cobwebs, grease, or debris inside the cabinet.  
- No loose screws, wire pieces, or other foreign objects inside.  
- No signs of moisture, rust, or corrosion.  

### 4. Seiketsu (Standardize)  
- All devices, breakers, relays, and terminals have clear, durable labels.  
- Wiring colors, symbols, and diagrams follow industrial standards (IEC, ISO, or local codes).  
- Safety and voltage warning labels are in the correct positions and readable.  

### 5. Shitsuke (Sustain)  
- A regular inspection and maintenance plan is in place.  
- Maintenance and repair history is recorded and accessible.  
- No signs of careless work or leftover materials after maintenance.  

### 6. Safety  
- No damaged insulation, cracks, or melted cable jackets.  
- No loose connections, open joints, or poor soldering.  
- All covers, guards, and shields are properly installed.  
- Grounding is correct and functional.  
- No overheating components or burning smell.  

---

**Output format (JSON rules):**  
- Return exactly **6 objects** in this order: Seiri, Seiton, Seiso, Seiketsu, Shitsuke, Safety.  
- Each object must have:
  - `"item"`: One of the fixed values above.  
  - `"status"`: `"OK"` or `"NG"`.  
  - `"reason"`: Short explanation for the status.  
  - `"defective_objects"`: A JSON array of objects **only if** status is `"NG"`. Each defective object must have:  
    - `"image_id"`: Use the **exact image path** as listed in the input.
    - `"label"`: Object name in snake_case format.  
    - `"box_2d"`: `[ymin, xmin, ymax, xmax]` with **values normalized to 0–1000** relative to the image size.  
    - `"issue"`: Short description of the defect.

**Example Output**:
```json
[
  {{
    "item": "Seiri",
    "status": "OK",
    "reason": "Only necessary components present",
    "defective_objects": []
  }},
  {{
    "item": "Seiton",
    "status": "NG",
    "reason": "Cables tangled and blocking breaker access",
    "defective_objects": [
      {{
        "image_id": "/path/to/example.jpg",
        "label": "tangled_cable_bundle",
        "box_2d": [200, 120, 400, 350],
        "issue": "Cables tangled and obstructing breaker access"
      }}
    ]
  }},
  {{
    "item": "Seiso",
    "status": "OK",
    "reason": "No visible dust or debris",
    "defective_objects": []
  }},
  {{
    "item": "Seiketsu",
    "status": "NG",
    "reason": "Some breakers missing labels",
    "defective_objects": [
      {{
        "image_id": "/path/to/example2.jpg",
        "label": "breaker_missing_label",
        "box_2d": [180, 450, 220, 500],
        "issue": "No identification label present"
      }}
    ]
  }},
  {{
    "item": "Shitsuke",
    "status": "OK",
    "reason": "Consistent maintenance records",
    "defective_objects": []
  }},
  {{
    "item": "Safety",
    "status": "NG",
    "reason": "Exposed wire found near busbar",
    "defective_objects": [
      {{
        "image_id": "/path/to/example2.jpg",
        "label": "exposed_wire",
        "box_2d": [300, 600, 340, 640],
        "issue": "Insulation stripped, conductor visible"
      }}
    ]
  }}
]
"""
    return prompt

list_images = [
    "static/images/raw/6S/6S_raw_1755239295_0.jpeg",
    "static/images/raw/6S/6S_raw_1755239295_1.jpg"
  ]
print(prompt_electric_6s(list_images))