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
    image = Image.open(BytesIO(response.content)).convert("RGB")
    w, h = image.size
    return w, h, image

url = "http://3.92.221.185:8080/static/images/raw/6S/6S_raw_1752283775.jpg"  # Replace with your actual image URL
w, h, image = read_image(url)
image.show()