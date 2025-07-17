import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import numpy as np
import cv2

def read_image(url_image):
    """
    Reads an image from a URL and returns width, height, and the image object.
    """
    response = requests.get(url_image)
    image = Image.open(BytesIO(response.content)).convert("RGBA")
    w, h = image.size
    return w, h, image

# Example usage
data ={
    "box_2d": [
      380,
      368,
      499,
      520
    ],
    "mask": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAAAAAB5Gfe6AAACUUlEQVR42u3dQW7bUBTF0Lv/TbMdBkjRSWTpK+RdgXmgkWHrbe3Z8WXC5G8buuR/O0i7fw0CV81d/04Drp86/kUGfHby/NMFuGfu+lMNuHkByPtRxx/mAG4Bnp48/2EBDpk8/yECcANw3Oz99xKAWwDcAhw8ef4dAhw/e/9nBXjH7P3Y+z9FAG4B5AC8bfb+iwVALmAH4KWz918lAG4BkAsgFwC3ALgFkAOAWwDkAtgFkAuAXAC5AAG4BcAtAHIBOwDIBZALEIBbADkAuAVALmAHALmAHQDkAnYAkAsEEICbgADcAgQgF7ADgFsAO4BegAACcAsEYBcIQC5AAAG4BewAIBcIoH63QAAByAUCkAMQgBsA5AIBBCAXCCAANwABBBBAAGaBAAIIIIAAAgjAKxBAAAEEEEAAAQQQQAABBBBAAAEEoAPoO7EA5P0B6AH6lVQAAQSg7g9gAQQQQAABmAH652RPQADu/gD0AL1Dwt4fgB5gAcj7A+iVigHI+3uxbgB6gF4vbu/vyEQA9n6TQLeWAujgWhf3OroYgFWg07MBdH87ALHAAnALbG6ByQE2uYAdYHMLbG6BBeAW2NwCkwNsboFNLjC5wOQAm1tgkwvYAfaj2fsnz3+/wNwCu2T2/tn7X0uwuQUmB5gcYFfP3v82gckF5gbYp2bvf4nA3AD78OT5hwvsltn7jxXYjbP3Hyiw2yfPP0pgj00PcATBnp67/lmBnTJ3/TMEO3Dy/BsJdvD+fjpr+ucfhL1p5vbLEfbm/eSg337ftOH/91h7cn8AtJYl1sdGPXMAAAAASUVORK5CYII=",
    "label": "clock of fire extinguisher"
  }
url = "http://0.0.0.0:8080/images/fire8.png"  # Replace with your actual image URL
w, h, image = read_image(url)

draw = ImageDraw.Draw(image)
y1, x1, y2, x2 = data["box_2d"]
y1 = int(y1 / 1000 * h)
x1 = int(x1 / 1000 * w)
y2 = int(y2 / 1000 * h)
x2 = int(x2 / 1000 * w)
draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

mask_data = data["mask"].split(",")[1]  # Remove data:image/png;base64,
mask_bytes = base64.b64decode(mask_data)
mask_pil = Image.open(BytesIO(mask_bytes))
mask = np.array(mask_pil)
box_width = x2 - x1
box_height = y2 - y1
mask_resized = cv2.resize(mask, (box_width, box_height))
# Tạo ảnh RGBA cho mặt nạ (với alpha)
rgba_mask = Image.fromarray(np.dstack((
    np.zeros_like(mask_resized),
    np.full_like(mask_resized, 255),  # G -> màu xanh lá
    np.zeros_like(mask_resized),
    (mask_resized > 10).astype(np.uint8) * 128  # Alpha: trong suốt vừa phải
)), mode="RGBA")

# Dán mask lên ảnh tại đúng vị trí box_2d
image.paste(rgba_mask, (x1, y1), mask=rgba_mask)


# Vẽ label
label = data["label"]

# Cố gắng sử dụng font mặc định, nếu không có thì dùng font cơ bản
try:
    # Sử dụng font có kích thước phù hợp
    # font_size = max(12, min(box_width // 10, 24))  # Tự động điều chỉnh kích thước font
    font_size = w // 50

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
except (OSError, IOError):
    # Nếu không tìm thấy font, sử dụng font mặc định
    font = ImageFont.load_default()

# Tính toán kích thước text
bbox = draw.textbbox((0, 0), label, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Tính toán vị trí để vẽ text (phía trên bounding box)
text_x = x1
text_y = max(0, y1 - text_height - 5)  # 5 pixel padding

# Vẽ background cho text (tùy chọn)
padding = 2
bg_x1 = text_x - padding
bg_y1 = text_y - padding
bg_x2 = text_x + text_width + padding
bg_y2 = text_y + text_height + padding

# Vẽ background màu đen với độ trong suốt
draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=(0, 0, 0, 180))

# Vẽ text màu trắng
draw.text((text_x, text_y), label, fill=(255, 255, 255, 255), font=font)

output_path = "images/result_with_bbox.png"
image.save(output_path)
image.show()