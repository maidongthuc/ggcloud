data= [
  {
    "item": "Seiri",
    "status": "NG",
    "reason": "Image 3 shows a water bottle and pliers placed on top of the electrical cabinet. These items are unrelated to the cabinet's operation or maintenance and pose a risk of falling into the cabinet or causing an electrical hazard if liquid spills. They should be removed to ensure a safe and organized workspace.",
    "defective_objects": [
      {
        "image_id": "static/images/raw/6S/6S_raw_1755509960_1.png",
        "label": [
          "water bottle",
          "pliers"
        ]
      }
    ],
    "images": [
      {
        "result": "http://0.0.0.0:8080/static/images/results/6S/Seiri_1755509970_7ae0e2f5.png",
        "raw": {
          "label": [
            "water bottle",
            "pliers"
          ],
          "image_id": "static/images/raw/6S/6S_raw_1755509960_1.png"
        }
      }
    ]
  },
  {
    "item": "Seiso",
    "status": "NG",
    "reason": "Image 2 shows significant dust accumulation on the top surface of the electrical cabinet, indicating a lack of regular cleaning. This accumulation can lead to component overheating and potential electrical hazards.",
    "defective_objects": [
      {
        "image_id": "static/images/raw/6S/6S_raw_1755509960_1.png",
        "label": [
          "dust on top surface of cabinet"
        ]
      }
    ],
    "images": [
      {
        "result": "http://0.0.0.0:8080/static/images/results/6S/Seiso_1755509968_78384157.png",
        "raw": {
          "label": [
            "dust on top surface of cabinet"
          ],
          "image_id": "static/images/raw/6S/6S_raw_1755509960_1.png"
        }
      }
    ]
  },
  {
    "item": "Seiton",
    "status": "NG",
    "reason": "In Image no 2, there are several instances of tangled cables, particularly at the bottom of the cabinet where cables are not properly routed or secured. This disorganization can hinder maintenance, troubleshooting, and pose a safety risk.",
    "defective_objects": [
      {
        "image_id": "static/images/raw/6S/6S_raw_1755509960_0.jpg",
        "label": [
          "tangled cable bundle"
        ]
      }
    ],
    "images": [
      {
        "result": "http://0.0.0.0:8080/static/images/results/6S/Seiton_1755509972_07f60543.jpg",
        "raw": {
          "label": [
            "tangled cable bundle"
          ],
          "image_id": "static/images/raw/6S/6S_raw_1755509960_0.jpg"
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
        "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1755509960_0.jpg",
        "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1755509960_1.png"
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
        "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1755509960_0.jpg",
        "http://0.0.0.0:8080/static/images/raw/6S/6S_raw_1755509960_1.png"
      ],
      "raw": {}
    }
  },
  {
    "item": "Safety",
    "status": "NG",
    "reason": "Image 2 shows a missing protective cover over the main busbar on the right side of the cabinet, exposing live parts. This poses a significant risk of accidental contact and electric shock.",
    "defective_objects": [
      {
        "image_id": "static/images/raw/6S/6S_raw_1755509960_0.jpg",
        "label": [
          "missing protective cover"
        ]
      }
    ],
    "images": [
      {
        "result": "http://0.0.0.0:8080/static/images/results/6S/Safety_1755509983_eba9264b.jpg",
        "raw": {
          "label": [
            "missing protective cover"
          ],
          "image_id": "static/images/raw/6S/6S_raw_1755509960_0.jpg"
        }
      }
    ]
  }
]
import json

# Remove defective_objects from each item
cleaned_data = []
for item in data:
    cleaned_item = {key: value for key, value in item.items() if key != 'defective_objects'}
    cleaned_data.append(cleaned_item)

print(json.dumps(cleaned_data, indent=2))