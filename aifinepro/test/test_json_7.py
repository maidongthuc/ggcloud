data = [
    {
      "item": "Seiton",
      "status": "NG",
      "reason": "Several cable bundles inside the cabinet are tangled and not properly routed or secured, particularly at the bottom right. This disorganization obstructs maintenance and increases the risk of accidental damage or misidentification of cables.",
      "images": [
        {
          "result": "http://0.0.0.0:8080/static/images/results/6S/Seiton_1755567932_f88da5be.jpg",
          "raw": {
            "label": [
              "tangled cable bundle"
            ],
            "image_id": "static/images/raw/6S/6S_raw_1755567923_0.jpg"
          }
        }
      ]
    },
    {
      "item": "Seiketsu",
      "status": "OK",
      "reason": "Seiketsu (Săn sóc/Chuẩn hóa) liên quan đến việc thiết lập các thực hành nhất quán về tổ chức, vệ sinh và kiểm soát trực quan trên nhiều hệ thống. Trong hình ảnh, các yếu tố nhìn thấy được có vẻ gọn gàng, tuy nhiên việc tuân thủ các quy trình chuẩn hóa tổng thể không thể được xác minh đầy đủ chỉ từ một bức ảnh, vì vậy giả định là đạt yêu cầu trong lần kiểm tra này.",
      "images": {
        "result": [
          "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1755567923_0.jpg",
          "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1755567923_1.png"
        ],
        "raw": {}
      }
    },
    {
      "item": "Shitsuke",
      "status": "OK",
      "reason": "Shitsuke (Sẵn sàng/Kỷ luật) liên quan đến cam kết lâu dài, đào tạo liên tục và việc tuân thủ các nguyên tắc 6S của nhân sự. Khía cạnh duy trì tiêu chuẩn theo thời gian này mang tính hành vi và quy trình, nên không thể đánh giá trực tiếp từ một hình ảnh tĩnh. Do đó, nó được coi là OK trong lần kiểm tra bằng hình ảnh này.",
      "images": {
        "result": [
          "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1755567923_0.jpg",
          "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1755567923_1.png"
        ],
        "raw": {}
      }
    },
    {
      "item": "Safety",
      "status": "NG",
      "reason": "Image 2 shows a critical safety hazard with exposed live wires at the top right busbar connection, posing a serious risk of electric shock. Additionally, the plastic protective cover appears to be improperly installed or missing in certain areas, leaving live components exposed.",
      "images": [
        {
          "result": "http://0.0.0.0:8080/static/images/results/6S/Safety_1755567951_b41a1c03.jpg",
          "raw": {
            "label": [
              "exposed live wires",
              "missing protective cover"
            ],
            "image_id": "static/images/raw/6S/6S_raw_1755567923_0.jpg"
          }
        }
      ]
    },
    {
      "item": "Seiso",
      "status": "NG",
      "reason": "Image 2 shows significant dust accumulation at the bottom of the electrical cabinet, which indicates a lack of cleanliness. This can potentially affect the internal components and overall hygiene of the cabinet.",
      "images": [
        {
          "result": "http://0.0.0.0:8080/static/images/results/6S/Seiso_1755567932_45d9b606.jpg",
          "raw": {
            "label": [
              "dust bottom of cabinet"
            ],
            "image_id": "static/images/raw/6S/6S_raw_1755567923_0.jpg"
          }
        }
      ]
    },
    {
      "item": "Seiri",
      "status": "NG",
      "reason": "A plastic water bottle is placed on top of the electrical cabinet. This item is unnecessary and unrelated to the cabinet's operation, posing a potential spill hazard that could damage the electrical components or create a safety risk if it leaks into the enclosure. It should be removed to maintain a safe and organized environment.",
      "images": [
        {
          "result": "http://0.0.0.0:8080/static/images/results/6S/Seiri_1755567931_2755d052.png",
          "raw": {
            "label": [
              "water bottle"
            ],
            "image_id": "static/images/raw/6S/6S_raw_1755567923_1.png"
          }
        }
      ]
    }
  ]
def add_vietnamese_names(data):
    # Dictionary mapping 6S items to Vietnamese names
    item_name_mapping = {
        "Seiri": "Sàng lọc",
        "Seiton": "Sắp xếp", 
        "Seiso": "Sạch sẽ",
        "Seiketsu": "Săn sóc",
        "Shitsuke": "Sẵn sàng",
        "Safety": "An toàn"
    }
    
    # Add name field to each item
    for item in data:
        if "item" in item:
            item_key = item["item"]
            item["name"] = item_name_mapping.get(item_key, item_key)
    
    return data

# Transform the data
transformed_data = add_vietnamese_names(data)

# Print the result
import json
print(json.dumps(transformed_data, indent=2, ensure_ascii=False))