import json
data = {
  "item": "Seiri",
  "status": "NG",
  "reason": "Trên nóc tủ điện có đặt một chai nước và một chiếc kìm. Đây là các vật dụng không liên quan đến vận hành hoặc bảo trì thường xuyên, gây lộn xộn, cản trở việc tiếp cận và tiềm ẩn rủi ro an toàn như đổ nước hoặc rơi dụng cụ.",
  "defective_objects": [
    {
      "image_id": "static/images/raw/6S/6S_raw_1755488921_1.png",
      "label": "water bottle"
    },
    {
      "image_id": "static/images/raw/6S/6S_raw_1755488921_1.png",
      "label": "pliers"
    },
     {
      "image_id": "static/images/raw/6S/6S_raw_1755488921_0.png",
      "label": "water bottle"
    },
  ]
}
# ...existing code...

def group_defective_objects_by_image(data):
    """
    Group defective objects by image_id and combine labels into arrays
    """
    if not data.get("defective_objects"):
        return data
    
    # Group by image_id
    image_groups = {}
    for obj in data["defective_objects"]:
        image_id = obj["image_id"]
        label = obj["label"]
        
        if image_id not in image_groups:
            image_groups[image_id] = []
        
        image_groups[image_id].append(label)
    
    # Convert back to defective_objects format
    new_defective_objects = []
    for image_id, labels in image_groups.items():
        new_defective_objects.append({
            "image_id": image_id,
            "label": labels
        })
    
    # Update data
    new_data = data.copy()
    new_data["defective_objects"] = new_defective_objects
    
    return new_data

# Process the data
processed_data = group_defective_objects_by_image(data)

print(json.dumps(processed_data, indent=2))