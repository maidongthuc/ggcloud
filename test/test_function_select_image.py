import requests
from PIL import Image
from io import BytesIO

urls_image = ['http://0.0.0.0:8080/static/images/results/6S/6S_2_1752630280.png', 'http://0.0.0.0:8080/static/images/results/6S/6S_2_1752630276.png', 'http://0.0.0.0:8080/static/images/results/6S/6S_0_1752630284.png']

def read_image(url_image):
    """
    Reads an image from a URL and return width and height.
    """
    response = requests.get(url_image)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    w, h = image.size[:2]
    
    return w, h, image

def select_image_clock(image_urls):
    """
    Selects the image URL that contains a clock from the list of image URLs.
    Args:
        image_urls: List of image URLs
    Returns: The URL of the image containing a clock, or None if not found
    """
    max_area = 0
    selected_url = None
    for url in image_urls:
        w, h, _ = read_image(url)
        area = w * h
        if area > max_area:
            max_area = area
            selected_url = url
    return selected_url

print(select_image_clock(urls_image))