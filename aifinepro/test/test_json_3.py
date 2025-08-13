data = [
  {
    "item": "Seiri",
    "status": "OK",
    "reason": "The cabinet appears to contain only necessary electrical components and wiring. No unnecessary items or clutter are visible inside.",
    "images": [
      "static/images/raw/6S/6S_raw_1755058488_1.jpg"
    ]
  },
  {
    "item": "Seiton",
    "status": "NG",
    "reason": "While components are mounted, some wiring at the bottom of the cabinet is not neatly bundled or routed, appearing somewhat disorganized.",
    "images": [
      "static/images/raw/6S/6S_raw_1755058488_1.jpg"
    ]
  },
  {
    "item": "Seiso",
    "status": "OK",
    "reason": "Both the interior and exterior of the electrical cabinet appear clean and free from significant dust or debris.",
    "images": [
      "static/images/raw/6S/6S_raw_1755058488_1.jpg",
      "static/images/raw/6S/6S_raw_1755058488_0.jpg"
    ]
  },
  {
    "item": "Seiketsu",
    "status": "NG",
    "reason": "There is a lack of clear and consistent labeling for individual circuits, components, or bus bar phases within the cabinet.",
    "images": [
      "static/images/raw/6S/6S_raw_1755058488_1.jpg"
    ]
  },
  {
    "item": "Shitsuke",
    "status": "NG",
    "reason": "The unorganized wiring and lack of comprehensive labeling suggest that some good practices might not be consistently sustained. The cabinet door is also left partially ajar in two images.",
    "images": [
      "static/images/raw/6S/6S_raw_1755058488_1.jpg",
      "static/images/raw/6S/6S_raw_1755058488_0.jpg"
    ]
  },
  {
    "item": "Safety",
    "status": "NG",
    "reason": "The cabinet door is left unsecured and partially open in images, posing a risk of unauthorized access or accidental contact. Some internal wiring appears loose and unmanaged, which could lead to damage or accidental contact.",
    "images": [
      "static/images/raw/6S/6S_raw_1755058488_0.jpg",
      "static/images/raw/6S/6S_raw_1755058488_1.jpg",
      "static/images/raw/6S/6S_raw_1755058488_2.jpg"
    ]
  }
]

def add_base_url_to_images(data, request):
    """
    Function to add base URL to all image paths in the data
    """
    if not request:
        return data
    
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    
    # Create a copy of data to avoid modifying original
    updated_data = []
    
    for item in data:
        updated_item = item.copy()  # Shallow copy of the item
        
        # Update images with base URL
        if "images" in updated_item and updated_item["images"]:
            updated_images = []
            for image_path in updated_item["images"]:
                # Add base URL if not already present
                if not image_path.startswith(('http://', 'https://')):
                    full_url = f"{base_url}/{image_path}"
                else:
                    full_url = image_path
                updated_images.append(full_url)
            updated_item["images"] = updated_images
        
        updated_data.append(updated_item)
    
    return updated_data

# Test với mock request
class MockRequest:
    def __init__(self, scheme="http", netloc="localhost:8000"):
        self.url = MockURL(scheme, netloc)

class MockURL:
    def __init__(self, scheme, netloc):
        self.scheme = scheme
        self.netloc = netloc

# Create mock request
mock_request = MockRequest("http", "0.0.0.0:8080")

# Transform the data
result = add_base_url_to_images(data, mock_request)

# Print result
import json
print(json.dumps(result, indent=2, ensure_ascii=False))