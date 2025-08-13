data= {
  "item": "Check the air pressure of the air filter, which should be between 0.5 and 0.7",
  "status": "OK",
  "reason": "The pressure gauge on the air filter clearly shows the needle pointing to approximately 0.55 MPa. This reading falls within the specified acceptable range of 0.5 to 0.7 MPa, indicating the air pressure is satisfactory according to the inspection standards."
}
list_url_image = ['static/images/raw/CL/CL_raw_1755060978_0.jpg']

def add_images_with_base_url(data, list_url_image, request=None):
    """
    Function to add images field to data with base URL
    """
    # Create a copy of data to avoid modifying original
    updated_data = data.copy()
    
    # Add base URL to images if request is provided
    if request:
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        full_urls = [f"{base_url}/{image_path}" for image_path in list_url_image]
        updated_data["images"] = full_urls
    else:
        # If no request, use original paths
        updated_data["images"] = list_url_image.copy()
    
    return updated_data

# Mock request for testing
class MockRequest:
    def __init__(self, scheme="http", netloc="localhost:8000"):
        self.url = MockURL(scheme, netloc)

class MockURL:
    def __init__(self, scheme, netloc):
        self.scheme = scheme
        self.netloc = netloc

# Test with mock request
mock_request = MockRequest("http", "0.0.0.0:8080")

# Transform the data
result = add_images_with_base_url(data, list_url_image, mock_request)

# Print result
import json
print(json.dumps(result, indent=2, ensure_ascii=False))