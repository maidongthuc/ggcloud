import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import numpy as np
import base64
import cv2
import os
import math
import time
import uuid
def read_image(url_image):
    """
    Reads an image from a URL and return width and height.
    """
    response = requests.get(url_image)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    w, h = image.size[:2]
    
    return w, h, image

def draw_bounding_boxes(detections, w, h, img, url_image, request=None):
    """
    retrurn bounding boxes from LLM detections
    """
    colors = ["green", "blue", "red", "orange", "purple", "yellow", "cyan", "magenta", "lime", "pink"]

    draw = ImageDraw.Draw(img)

    line_width = max(1, min(w, h) // 200)  # Width scales with image size
    font_size = max(12, min(w, h) // 50)   # Font size scales with image size
    
    # Try to load a font with the calculated size
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            # For Windows
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    for i, det in enumerate(detections):
        # LLM return normalized coordinates (0-1000), need to scale to actual pixel values
        y1, x1, y2, x2 = det["box_2d"]
        label = det["label"]
        
        # Scale normalized coordinates (0-1000) to actual image dimensions
        y1 = int(y1 / 1000 * h)
        x1 = int(x1 / 1000 * w)
        y2 = int(y2 / 1000 * h)
        x2 = int(x2 / 1000 * w)
        print([x1, y1, x2, y2])
        # Draw
        color = colors[i % len(colors)]

        text_offset = max(font_size + 5, 15)  # Dynamic offset based on font size
        
        # Calculate text position - ensure it's within image bounds
        text_x = x1
        text_y = y1 - text_offset
        
        # If text would go above image, place it below the box
        if text_y < 0:
            text_y = y2 + 5  # Place below the bounding box
        
        # If text would go beyond right edge, adjust x position
        try:
            text_bbox = draw.textbbox((text_x, text_y), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_x + text_width > w:
                text_x = w - text_width - 5
        except:
            # Fallback if textbbox not available
            text_x = min(text_x, w - len(label) * font_size // 2)

        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)
        draw.text((text_x, text_y), label, fill=color, font=font)

    # Extract category from URL
    url_parts = url_image.split('/')
    category = url_parts[-2]
    # Extract file extension from original URL
    original_extension = os.path.splitext(url_image)[1]
    if not original_extension:
        original_extension = ".png"  # default extension
    # Create directory structure: static/images/results/{category}/
    results_dir = os.path.join("static", "images", "results", category)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Generate filename with category and timestamp
    timestamp = int(time.time())
    file_name = f"{category}_result_{timestamp}{original_extension}"
    
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

def draw_bounding_boxes_Tien(detections, w, h, img, url_image, request=None, object_to_criteria=None):
    """
    Vẽ bounding box lên ảnh PIL với màu theo tiêu chí 6S (nếu có).
    """
    return detections
    # Màu tiêu chuẩn cho từng tiêu chí
    criteria_colors = {
        "Seiri - Sàng lọc": "green",
        "Seiton - Sắp xếp": "orange",
        "Seiso - Sạch sẽ": "blue",
        "Safety - An toàn": "red",
        "Seiketsu - Săn sóc": "purple",
        "Shitsuke - Sẵn sàng": "magenta"
    }
    default_colors = ["cyan", "lime", "pink", "yellow", "gray"]

    draw = ImageDraw.Draw(img)
    line_width = max(1, min(w, h) // 200)
    font_size = max(12, min(w, h) // 50)

    # Font chữ
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # === Vẽ từng bounding box ===
    for i, det in enumerate(detections):
        y1, x1, y2, x2 = det["box_2d"]
        label = det["label"]

        # Scale tọa độ từ 1000 → px
        y1 = int(y1 / 1000 * h)
        x1 = int(x1 / 1000 * w)
        y2 = int(y2 / 1000 * h)
        x2 = int(x2 / 1000 * w)

        # Lấy tiêu chí tương ứng object (nếu có)
        criteria = object_to_criteria.get(label) if object_to_criteria else None
        color = criteria_colors.get(criteria, default_colors[i % len(default_colors)])
        full_label = f"{label} ({criteria})" if criteria else label

        # Tính vị trí ghi chữ
        text_offset = max(font_size + 5, 15)
        text_x, text_y = x1, y1 - text_offset
        if text_y < 0: text_y = y2 + 5

        # Canh lề để chữ không bị tràn
        try:
            text_bbox = draw.textbbox((text_x, text_y), full_label, font=font)
            if text_bbox[2] > w:
                text_x = w - (text_bbox[2] - text_bbox[0]) - 5
        except:
            pass

        # Vẽ box và text
        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)
        draw.text((text_x, text_y), full_label, fill=color, font=font)

    # === Lưu ảnh kết quả ===
    file_name = os.path.basename(url_image)  # ex: 6S20250719114001.jpg
    result_path = os.path.join("static", "img", "result")
    os.makedirs(result_path, exist_ok=True)

    file_path = os.path.join(result_path, file_name)
    img.save(file_path)

    # Trả lại URL ảnh kết quả
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        image_url = f"{base_url}/static/img/result/{file_name}"
    else:
        image_url = f"/static/img/result/{file_name}"

    return image_url

def get_mask_center(det, w, h):
    """
    det: dict chứa keys 'box_2d', 'mask'
    w, h: kích thước ảnh gốc
    Trả về (center_x, center_y) trên ảnh gốc - đảm bảo điểm nằm trong vùng segmentation
    """
    import base64
    import numpy as np
    from PIL import Image
    from io import BytesIO

    # Lấy box và scale về pixel gốc
    y1, x1, y2, x2 = det["box_2d"]
    y1 = int(y1 / 1000 * h)
    x1 = int(x1 / 1000 * w)
    y2 = int(y2 / 1000 * h)
    x2 = int(x2 / 1000 * w)
    box_width = x2 - x1
    box_height = y2 - y1

    # Decode mask
    mask_data = det["mask"].split(",")[1]
    mask_bytes = base64.b64decode(mask_data)
    mask_pil = Image.open(BytesIO(mask_bytes)).convert("L")
    mask_np = np.array(mask_pil)
    # Resize mask về đúng kích thước box
    mask_resized = cv2.resize(mask_np, (box_width, box_height))

    # Tìm các pixel thuộc vùng mask
    ys, xs = np.where(mask_resized > 10)
    if len(xs) == 0 or len(ys) == 0:
        return None  # Không có vùng mask

    # Tính centroid có trọng số
    mask_pixels = mask_resized[ys, xs]
    weighted_x = np.average(xs, weights=mask_pixels)
    weighted_y = np.average(ys, weights=mask_pixels)
    
    centroid_x = int(round(weighted_x))
    centroid_y = int(round(weighted_y))
    
    # Kiểm tra xem centroid có nằm trong mask không
    if (0 <= centroid_y < box_height and 0 <= centroid_x < box_width and 
        mask_resized[centroid_y, centroid_x] > 10):
        center_x_in_box = centroid_x
        center_y_in_box = centroid_y
    else:
        # Tìm điểm gần nhất với centroid trong mask
        distances = (xs - centroid_x)**2 + (ys - centroid_y)**2
        closest_idx = np.argmin(distances)
        
        center_x_in_box = xs[closest_idx]
        center_y_in_box = ys[closest_idx]

    # Đổi về toạ độ ảnh gốc
    center_x = x1 + center_x_in_box
    center_y = y1 + center_y_in_box

    return center_x, center_y

def draw_arrow_to_center(detections, w, h, img, url_image, request=None):
    # Chuyển đổi ảnh PIL sang numpy array (BGR cho OpenCV)
    img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    for i, det in enumerate(detections):
        center_x,  center_y = get_mask_center(det, w, h)
        end_point = (center_x, center_y)

        # Chọn góc xiên, ví dụ 45 độ (hoặc random)
        angle_deg = 45 + i * 30  # mỗi mũi tên lệch nhau 30 độ
        angle_rad = math.radians(angle_deg)
        arrow_length = w / 4

        start_x = int(center_x + arrow_length * math.cos(angle_rad))
        start_y = int(center_y + arrow_length * math.sin(angle_rad))
        start_point = (start_x, start_y)

        color = (57, 255, 20)
        thickness = 8
        tipLength = 0.18
        cv2.arrowedLine(img_np, start_point, end_point, color, thickness, tipLength=tipLength)
    # Chuyển lại sang PIL để lưu
    img_arrow = Image.fromarray(cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))

    # ...phần lưu file giữ nguyên...
    url_parts = url_image.split('/')
    category = url_parts[-2]
    original_extension = os.path.splitext(url_image)[1]
    if not original_extension:
        original_extension = ".png"
    results_dir = os.path.join("static", "images", "results", category)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    timestamp = int(time.time())
    file_name = f"{category}_result_{timestamp}{original_extension}"
    file_path = os.path.join(results_dir, file_name)
    img_arrow.save(file_path)
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        image_url = f"{base_url}/static/images/results/{category}/{file_name}"
    else:
        image_url = f"/static/images/results/{category}/{file_name}"
    return image_url

def cut_bounding_boxes(detections, w, h, img, url_image, request=None):
    """
    Cut and save individual bounding boxes from LLM detections
    """
    
    # Extract category from URL
    url_parts = url_image.split('/')
    category = url_parts[-2]
    # Extract file extension from original URL
    original_extension = os.path.splitext(url_image)[1]
    if not original_extension:
        original_extension = ".png"  # default extension
    
    # Create directory structure: static/images/results/{category}/
    results_dir = os.path.join("static", "images", "results", category)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    saved_images = []
    
    for i, det in enumerate(detections):
        # LLM return normalized coordinates (0-1000), need to scale to actual pixel values
        y1, x1, y2, x2 = det["box_2d"]
        label = det["label"]
        
        # Scale normalized coordinates (0-1000) to actual image dimensions
        y1 = int(y1 / 1000 * h)
        x1 = int(x1 / 1000 * w)
        y2 = int(y2 / 1000 * h)
        x2 = int(x2 / 1000 * w)
        
        # Ensure coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        # Cut the bounding box from the image
        cropped_img = img.crop((x1, y1, x2, y2))
        
        # Generate filename for cropped image
        timestamp = int(time.time())
        unique_id = uuid.uuid4().hex[:8] 
        file_name = f"{category}_{i}_{timestamp}_{unique_id}{original_extension}"
        
        # Save cropped image
        file_path = os.path.join(results_dir, file_name)
        cropped_img.save(file_path)
        
        # Generate URL for the saved image
        if request:
            base_url = f"{request.url.scheme}://{request.url.netloc}"
            image_url = f"{base_url}/static/images/results/{category}/{file_name}"
        else:
            image_url = f"/static/images/results/{category}/{file_name}"
        
        saved_images.append({
            "label": label,
            "url": image_url
        })
    
    return saved_images

def function_draw_segmentation(detections, w, h, img, url_image, request=None):
    """
    retrurn bounding boxes from LLM detections
    """
    colors = ["green", "blue", "red", "orange", "purple", "yellow", "cyan", "magenta", "lime", "pink"]
    
    # Map color names to RGB values
    color_rgb = {
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "red": (255, 0, 0),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "lime": (0, 255, 0),
        "pink": (255, 192, 203)
    }

    draw = ImageDraw.Draw(img)

    line_width = max(1, min(w, h) // 200)  # Width scales with image size
    font_size = max(12, min(w, h) // 50)   # Font size scales with image size
    
    # Try to load a font with the calculated size
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            # For Windows
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    for i, det in enumerate(detections):
        # LLM return normalized coordinates (0-1000), need to scale to actual pixel values
        y1, x1, y2, x2 = det["box_2d"]
        label = det["label"]
        
        # Scale normalized coordinates (0-1000) to actual image dimensions
        y1 = int(y1 / 1000 * h)
        x1 = int(x1 / 1000 * w)
        y2 = int(y2 / 1000 * h)
        x2 = int(x2 / 1000 * w)
        
        # Draw
        color = colors[i % len(colors)]
        rgb_color = color_rgb.get(color, (0, 255, 0))  # Default to green if color not found

        text_offset = max(font_size + 5, 15)  # Dynamic offset based on font size
        
        # Calculate text position - ensure it's within image bounds
        text_x = x1
        text_y = y1 - text_offset
        
        # If text would go above image, place it below the box
        if text_y < 0:
            text_y = y2 + 5  # Place below the bounding box
        
        # If text would go beyond right edge, adjust x position
        try:
            text_bbox = draw.textbbox((text_x, text_y), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_x + text_width > w:
                text_x = w - text_width - 5
        except:
            # Fallback if textbbox not available
            text_x = min(text_x, w - len(label) * font_size // 2)
        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)
        draw.text((text_x, text_y), label, fill=color, font=font)

        mask_data = det["mask"].split(",")[1]  # Remove data:image/png;base64,
        mask_bytes = base64.b64decode(mask_data)
        mask_pil = Image.open(BytesIO(mask_bytes))
        mask = np.array(mask_pil)
        box_width = x2 - x1
        box_height = y2 - y1
        mask_resized = cv2.resize(mask, (box_width, box_height))
        
        # Tạo ảnh RGBA cho mặt nạ với màu tương ứng
        rgba_mask = Image.fromarray(np.dstack((
            np.full_like(mask_resized, rgb_color[0]),  # R
            np.full_like(mask_resized, rgb_color[1]),  # G
            np.full_like(mask_resized, rgb_color[2]),  # B
            (mask_resized > 10).astype(np.uint8) * 128  # Alpha: trong suốt vừa phải
        )), mode="RGBA")

        # Dán mask lên ảnh tại đúng vị trí box_2d
        img.paste(rgba_mask, (x1, y1), mask=rgba_mask)

    # Extract category from URL
    url_parts = url_image.split('/')
    category = url_parts[-2]
    # Extract file extension from original URL
    original_extension = os.path.splitext(url_image)[1]
    if not original_extension:
        original_extension = ".png"  # default extension
    # Create directory structure: static/images/results/{category}/
    results_dir = os.path.join("static", "images", "results", category)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Generate filename with category and timestamp
    timestamp = int(time.time())
    file_name = f"{category}_result_{timestamp}{original_extension}"
    
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
