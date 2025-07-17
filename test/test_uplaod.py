import requests

# Upload ảnh từ file local
def upload_image(file_path, server_url="http://0.0.0.0:8080"):
    with open(file_path, "rb") as f:
        files = {"file": ("image.jpg", f, "image/jpeg")}
        response = requests.post(f"{server_url}/upload_image/", files=files)
        return response.json()

# Sử dụng
result = upload_image("/home/acer/Downloads/tien.jpg")
print(result)
# Output: {"message": "success", "url": "http://0.0.0.0:8080/images/image.jpg", "filename": "image.jpg"}