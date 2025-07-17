import cv2
import numpy as np
import base64
from PIL import Image
from io import BytesIO

# Load image
img = cv2.imread('images/fire8.png')
h, w = img.shape[:2]

# Data
data =  {"box_2d": [470, 0, 1000, 836], "mask": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAAAAAB5Gfe6AAACGklEQVR42u3YwWrDQBQDQP//T6uXQmkJJYm94a01ugekYbNxfBwyPflO+/5WgvzOjgPOffyvwHYGJxs/ANjG4JK6jwHGE1xXNv+k5OJKNkO4umQ2E8iHAYYRXN8wz2T0/IW34CyDReWSHQjWVUvmC6xsltcyc/6Jank9M+e/VyzvZeb+N3olwwUWF8uJzNz/UrWcy9T5z1bL+Uzdn4+sX06wslkyX2BVw1yc6ft/SmZR5s9fnvL5lwtkw7Tvv5AgqQbIzqkHuIAg6RZIOUBSLZB7pH1/2ve/KZA7pX3/J99M30Qg6RYIgG6BpFsg5QBJt0DKAZJugaRbIOkWCIBugZQDJN0CKQdIygXaAZJygXaAAOgWCIBugAAoF2gHCIBugQDoBkjKBQAA6AZIygUAlAPECXACAAAA0AsQAAAAACgWCAAAAAAAAND7HOAAAAAAAAAAAAAAAAAAAAAAAF4HAAAAAAAAAPYDAAAAgL9CAAC4AgAAcAUAAADAHQgAAAAAAAAAuNl+AAAAAADQvB8AAAAAAAAAAAAAAAAAAAAA0LcfAAAAAAAAAAAAQOt+AAAAAAAAAAAAAAAAdO4HAAAAAAAAAAAAAAAAgE6Ao33/4QAA8BVwAgAAcAfU7gcAAAAAAAAAAAAAAACAyv0AAAAAAAAAAM9BAHwFAAAAAKBwPwAAAAAAAOAxAAAAAAA6fwQOAAAAAGjeD6Ac4Auvvl3Tm2CgUAAAAABJRU5ErkJggg==", "label": "dust on the fire extinguisher wall"}

# Decode mask from base64
mask_data = data["mask"].split(",")[1]  # Remove data:image/png;base64,
mask_bytes = base64.b64decode(mask_data)
mask_pil = Image.open(BytesIO(mask_bytes))
mask = np.array(mask_pil)

# Get bounding box coordinates and scale to image size
y1, x1, y2, x2 = data["box_2d"]
y1 = int(y1 / 1000 * h)
x1 = int(x1 / 1000 * w)
y2 = int(y2 / 1000 * h)
x2 = int(x2 / 1000 * w)

# Draw bounding box
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Add label
cv2.putText(img, data["label"], (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Resize mask to fit bounding box
box_width = x2 - x1
box_height = y2 - y1
mask_resized = cv2.resize(mask, (box_width, box_height))

# Apply mask overlay (if mask has transparency)
if len(mask_resized.shape) == 3:
    mask_gray = cv2.cvtColor(mask_resized, cv2.COLOR_BGR2GRAY)
else:
    mask_gray = mask_resized

# Create colored mask overlay
mask_colored = np.zeros((box_height, box_width, 3), dtype=np.uint8)
mask_colored[:,:,0] = mask_gray  # Blue channel
mask_overlay = cv2.addWeighted(img[y1:y2, x1:x2], 0.4, mask_colored, 0.3, 0)
img[y1:y2, x1:x2] = mask_overlay

height, width = img.shape[:2]
scale = 800 / max(height, width)  # Scale to max 800px
new_width = int(width * scale)
new_height = int(height * scale)
img_resized = cv2.resize(img, (new_width, new_height))

# Show result
cv2.imshow('Result', img_resized)
cv2.waitKey(0)