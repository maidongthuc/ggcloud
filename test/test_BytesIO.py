import requests
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import numpy as np
import cv2

def read_image(url_image):
    """
    Reads an image from a URL and returns the image, width, and height.
    """
    response = requests.get(url_image)
    image = Image.open(BytesIO(response.content)).convert("RGBA")
    w, h = image.size
    return image, w, h

def draw_annotation(image, data):
    """
    Draw box_2d and mask on the image.
    """
    draw = ImageDraw.Draw(image)

    for item in data:
        # Draw bounding box
        xmin, ymin, xmax, ymax = item["box_2d"]
        draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=3)

        # Decode mask
        mask_base64 = item["mask"].split(",")[1]  # Remove header "data:image/png;base64,"
        mask_bytes = base64.b64decode(mask_base64)
        mask_image = Image.open(BytesIO(mask_bytes)).convert("L")  # grayscale mask

        # Resize mask to image size if needed
        mask_array = np.array(mask_image)
        mask_resized = cv2.resize(mask_array, image.size)

        # Create transparent mask overlay
        rgba_mask = Image.fromarray(np.dstack((
            np.zeros_like(mask_resized),
            np.zeros_like(mask_resized),
            np.full_like(mask_resized, 255),  # blue mask
            (mask_resized > 10).astype(np.uint8) * 100  # transparency
        )), mode='RGBA')

        image.alpha_composite(rgba_mask)

    return image

# === MAIN EXECUTION ===
url_image = 'http://0.0.0.0:8080/images/binh-chua-chay-chi-vach-vang.jpg'  # 👉 Thay bằng URL thật
json_data = [
  {
    "box_2d": [299, 399, 601, 596],
    "mask": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAAAAAB5Gfe6AAACc0lEQVR42u3dy07DQBQE0f7/n25eYcMiCortueOqlhBLVIcBCZR4EucWr9/7+vz5kZ8PQPSj++nu++1+eeD0X4GC429xCnrEwOn7CvTgwfP3EugpY9fvYtCzB8+fLdBrBs8fy9DLB88fJdBVg+ePQOj6wfNXCnTO8AArEDpu8PwLCTp49P7zCbrB6P0nCnSb2Q8HOIegZQu0aIHuN3r/oQItW6BlC7RwgaIFuvng+e8KtGyBli3QwgUKF7C/bILCBVq4QOkChQu0cIHCBVq4QAsnoAO0cIHSBQSAC/Tmo/cLUAHoAMUDlN7/VIAOUDhAPQCeADRABRAADdDCBegARU0AAdj9AggA7xcAD1ABBIADVAAB2P1/BOgALVugdABPgAACsAUEgAN4ADwBcAEBBBBAALJABRBAAAUEEEAALIAHQAAB4H8NCeDPgAAC+DtAAAG4AP5bWAABBBAADeBLJAQQQAB0vwD0fl8vL4AAAgiA7hfAt44KQAfw7eN0AJ+gQO/3SUIVwB8BAdD9PlISJkAHiAA+WtmniwvgFQteMyOAV00J4HVrXrjnpZPeOioACQB/865XL3v7NhkgL04AOkDo/QLQ+28qELhAwhaIAAKgBSIAGyACoAkSAdACgQMkbIEIwBZI4AKBCyRsgQQuELZADhq9f1eBBC4QuEAOHr1/N4HAARK2QMIWSNgCCVsgpw4PEHj+eIGELZCwBRK2QIIWyKXDA4wjyILB8ycJZNno/TMIErRABozev1IgU8auX2KQeYPnX0mQuYPnX0GQDcauP5MgQQtkr6HjD1bI3oPnv2eQ+wye/0+D3HvY8OcUK77+B05jKX5Fawu2AAAAAElFTkSuQmCC",
    "label": "clock of fire extinguisher"
  }
]

image, w, h = read_image(url_image)
image_with_annotations = draw_annotation(image, json_data)

# Show image (or save to file)
image_with_annotations.show()
# image_with_annotations.save("output.png")
