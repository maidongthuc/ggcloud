data = [
  {
    "box_2d": [
      176,
      364,
      422,
      627
    ],
    "label": "clock of fire extinguisher"
  }
]

import sys
import os
import cv2

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Load image
image_path = "./images/binh-chua-chay-chi-vach-vang.jpg"
img = cv2.imread(image_path)
h, w, _ = img.shape

print(f"Image dimensions: {w}x{h}")

# Draw bounding boxes from data
for detection in data:
    y1, x1, y2, x2 = detection["box_2d"]
    label = detection["label"]
    
    print(f"Drawing box: ({x1}, {y1}) to ({x2}, {y2}) - {label}")
    
    # Draw rectangle
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Add label with background
    text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
    cv2.rectangle(img, (x1, y1-25), (x1 + text_size[0], y1), (0, 255, 0), -1)
    cv2.putText(img, label, (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

# Save result
os.makedirs("images", exist_ok=True)
output_path = "images/detection_result.jpg"
cv2.imwrite(output_path, img)

print(f"Detection result saved to: {output_path}")
print(f"Drew {len(data)} bounding boxes")

# Display image (optional - uncomment if you want to see it)
# cv2.imshow('Detection Result', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()