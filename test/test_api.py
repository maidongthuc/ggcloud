import requests

url = "http://0.0.0.0:8080/object_detection/"

payload = {
    "objects": "clock of fire extinguisher",
    "url_image": "http://0.0.0.0:8080/images/fire8.png"
}

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status code:", response.status_code)
print("Response JSON:", response.json())
