import os
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import time
import uuid

data = [
  {
    "item": "Seiri",
    "status": "OK",
    "reason": "Only necessary equipment and components are present inside the cabinet. No unrelated items, scrap, or excessive spare parts are visible.",
    "defective_objects": []
  },
  {
    "item": "Seiton",
    "status": "NG",
    "reason": "Cables are not routed neatly; several are loose, untidy, and lack proper management, especially at the bottom of the cabinet. The excess cable length for the yellow/black conduit is not properly managed.",
    "defective_objects": [
      {
        "image_id": "static/images/raw/6S/6S_raw_1755243263_0.jpg",
        "label": "untidy_cable_routing",
        "box_2d": [
          700,
          250,
          950,
          750
        ],
        "issue": "Cables emerging from the bottom conduit are not neatly routed and appear excessively loose."
      },
      {
        "image_id": "static/images/raw/6S/6S_raw_1755243263_0.jpg",
        "label": "excess_cable_loop",
        "box_2d": [
          750,
          600,
          950,
          850
        ],
        "issue": "Excess cable length in the yellow/black flexible conduit is not managed, creating an untidy loop."
      }
    ]
  },
  {
    "item": "Seiso",
    "status": "OK",
    "reason": "The cabinet interior and exterior appear clean, free from dust, cobwebs, grease, or debris. No signs of moisture, rust, or corrosion are visible.",
    "defective_objects": []
  },
  {
    "item": "Seiketsu",
    "status": "NG",
    "reason": "Critical components such as circuit breakers, busbars, and terminals lack clear, durable identification labels. The existing handwritten label is not standardized.",
    "defective_objects": [
      {
        "image_id": "static/images/raw/6S/6S_raw_1755243263_0.jpg",
        "label": "missing_breaker_labels",
        "box_2d": [
          350,
          100,
          700,
          800
        ],
        "issue": "No clear, durable functional labels are present for the circuit breakers."
      },
      {
        "image_id": "static/images/raw/6S/6S_raw_1755243263_0.jpg",
        "label": "non_standard_label",
        "box_2d": [
          450,
          370,
          500,
          550
        ],
        "issue": "The handwritten 'R B Y V' label on the clear plastic cover is not a durable or standardized labeling method."
      },
      {
        "image_id": "static/images/raw/6S/6S_raw_1755243263_1.jpg",
        "label": "missing_terminal_labels",
        "box_2d": [
          100,
          200,
          400,
          800
        ],
        "issue": "Busbars and main terminals lack clear identification labels."
      }
    ]
  },
  {
    "item": "Shitsuke",
    "status": "NG",
    "reason": "The poor cable management and lack of consistent labeling suggest a lack of sustained effort in maintaining the cabinet's order and standardization after installation or maintenance.",
    "defective_objects": [
      {
        "image_id": "static/images/raw/6S/6S_raw_1755243263_0.jpg",
        "label": "lack_of_sustained_order",
        "box_2d": [
          700,
          250,
          950,
          750
        ],
        "issue": "The untidy cable routing indicates a lack of sustained tidiness and adherence to standards."
      }
    ]
  },
  {
    "item": "Safety",
    "status": "OK",
    "reason": "All visible connections appear properly terminated. A clear plastic cover provides protection from accidental contact with live parts. Grounding connections appear correct, and there are no visible signs of damaged insulation, overheating, or open joints.",
    "defective_objects": []
  }
]

def draw_bounding_boxes(detections, url_path, request=None):
    """
    Draw bounding boxes from LLM detections with single color, no labels
    """
    color = "red"  # Single color for all boxes
    image = Image.open(url_path)
    w, h = image.size
    img = image.convert("RGB")
    draw = ImageDraw.Draw(img)
    
    line_width = max(2, min(w, h) // 200)  # Width scales with image size
    
    for det in detections:
        # LLM return normalized coordinates (0-1000), need to scale to actual pixel values
        y1, x1, y2, x2 = det["box_2d"]
        
        # Scale normalized coordinates (0-1000) to actual image dimensions
        y1 = int(y1 / 1000 * h)
        x1 = int(x1 / 1000 * w)
        y2 = int(y2 / 1000 * h)
        x2 = int(x2 / 1000 * w)
        
        # Draw rectangle only, no label
        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)

    # Extract category from URL
    url_parts = url_path.split('/')
    category = url_parts[-2]
    # Extract file extension from original URL
    original_extension = os.path.splitext(url_path)[1]
    if not original_extension:
        original_extension = ".png"  # default extension
    
    # Create directory structure: static/images/results/{category}/
    results_dir = os.path.join("static", "images", "results", category)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Generate filename with category and timestamp
    timestamp = int(time.time())
    unique_id = uuid.uuid4().hex[:8]
    file_name = f"{category}_result_{timestamp}_{unique_id}{original_extension}"
    
    # Save image with bounding boxes
    file_path = os.path.join(results_dir, file_name)
    img.save(file_path)
    
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        image_url = f"{base_url}/static/images/results/{category}/{file_name}"
    else:
        # Fallback URL without request object
        image_url = f"/static/images/results/{category}/{file_name}"
    
    return image_url

# Transform data structure
transformed_data = []

for item in data:
    new_item = {
        "item": item["item"],
        "status": item["status"],
        "reason": item["reason"]
    }
    
    if item["defective_objects"]:
        # Group defective objects by image_id
        image_groups = {}
        for obj in item["defective_objects"]:
            image_id = obj["image_id"]
            if image_id not in image_groups:
                image_groups[image_id] = []
            image_groups[image_id].append({
                "label": obj["label"],
                "box_2d": obj["box_2d"],
                "issue": obj["issue"]
            })
        
        # Process images and collect URLs
        processed_images = []
        for url, detections in image_groups.items():
            # Draw bounding boxes and get the result URL
            result_url = draw_bounding_boxes(detections, url)
            processed_images.append(result_url)
            print(f"Processed image: {result_url}")
        
        # Add images field with processed URLs
        new_item["images"] = processed_images
    else:
        new_item["images"] = []
    
    transformed_data.append(new_item)

# Print final transformed data
print(json.dumps(transformed_data, indent=2))