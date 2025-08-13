data = {
  "overview": {
    "cleanliness": {
      "status": "NG",
      "reason": "The interior of the cabinet is extremely dirty, with significant accumulation of dust, dirt, and debris on the bottom shelf and inside walls. The fire hose itself is heavily soiled. The exterior of the cabinet also shows some dust and grime, particularly on the top surface and around the glass panel."
    },
    "organization": {
      "status": "NG",
      "reason": "While the fire hose is coiled and placed on the upper shelf, and the fire valve is positioned on the bottom, the overall organization is compromised by the excessive dirt and debris present inside the cabinet, especially on the bottom shelf near the valve, which includes a piece of paper. This detracts from a neat and properly arranged appearance."
    }
  },
  "fire_hose": {
    "status": "NG",
    "reason": "The fire hose is heavily covered in dust and dirt, indicating poor maintenance. While no major cracks or tears are clearly visible, the significant accumulation of grime raises concerns about its long-term integrity and readiness for immediate use. The coiling is generally in place but not perfectly neat."
  },
  "fire_valve": {
    "status": "NG",
    "reason": "The fire valve is heavily covered in dust and dirt, particularly around its base and operating mechanism. While no obvious physical damage or leaks are visible, the substantial amount of dirt can impede its proper operation and indicates a lack of regular maintenance. Its operational capability cannot be confirmed from a static image."
  },
  "fire_nozzle": {
    "status": "NG",
    "reason": "The fire nozzle, attached to the hose, is also heavily soiled with dust and dirt, similar to the hose itself. Its detailed physical condition, including potential blockages or specific damage, cannot be clearly assessed due to the amount of dirt and the viewing angle."
  },
  "cabinet_lock": {
    "status": "OK",
    "reason": "The cabinet appears to utilize a simple latch mechanism, likely designed for quick emergency access without a key. There is no visible damage to the latch mechanism on either the exterior or interior of the cabinet door, suggesting it is physically intact and capable of securing the door while allowing for ease of emergency access."
  },
  "id": 5
}

image_results = {'cabinet_lock': ['static/images/results/FIRE/CABINET_result_cabinet_lock_1755048398_2ed0a4d8.jpg', 'static/images/results/FIRE/CABINET_result_cabinet_lock_1755048398_494f7f9d.jpg'], 'fire_valve': ['static/images/results/FIRE/CABINET_result_fire_valve_1755048398_c8878682.jpg'], 'fire_hose': ['static/images/results/FIRE/CABINET_result_fire_hose_1755048398_a5483ec1.jpg']}
list_images = ['static/images/raw/FIRE/FIRE_raw_1755048397_0.jpg', 'static/images/raw/FIRE/FIRE_raw_1755048397_1.jpg']


def transform_cabinet_data(data, image_results, list_images):
    transformed_results = []
    
    # Vietnamese names mapping
    vietnamese_names = {
        "overview": "Tổng quan",
        "cleanliness": "Vệ sinh",
        "organization": "Sắp xếp",
        "fire_hose": "Vòi bạc chữa cháy",
        "fire_valve": "Van mở chữa cháy", 
        "fire_nozzle": "Lăng phun chữa cháy",
        "cabinet_lock": "Chốt khóa tủ"
    }
    
    # 1. Handle overview (special case with nested structure)
    if "overview" in data:
        overview_item = {
            "item": "overview",
            "name": vietnamese_names["overview"],
            "images": list_images,
            "details": []
        }
        
        # Add cleanliness and organization as details
        for sub_item in ["cleanliness", "organization"]:
            if sub_item in data["overview"]:
                overview_item["details"].append({
                    "item": sub_item,
                    "name": vietnamese_names[sub_item],
                    "status": data["overview"][sub_item]["status"],
                    "reason": data["overview"][sub_item]["reason"]
                })
        
        transformed_results.append(overview_item)
    
    # 2. Handle other components (fire_hose, fire_valve, fire_nozzle, cabinet_lock)
    components = ["fire_hose", "fire_valve", "fire_nozzle", "cabinet_lock"]
    
    for component in components:
        if component in data:
            component_item = {
                "item": component,
                "name": vietnamese_names[component],
                "images": image_results.get(component, []),  # Get images from image_results
                "status": data[component]["status"],
                "reason": data[component]["reason"]
            }
            
            transformed_results.append(component_item)
    
    return transformed_results

# Transform the data
result = transform_cabinet_data(data, image_results, list_images)

# Print the result
import json
print(json.dumps(result, indent=2, ensure_ascii=False))