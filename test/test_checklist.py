import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import base64
from src.llm_gemini import llm
from langchain_core.messages import HumanMessage, SystemMessage


# encoded_image = "http://3.92.221.185:8080/static/images/results/checklist/checklist_clock_0_1752133850.png"
encoded_image = "http://3.92.221.185:8080/static/images/raw/checklist/checklist_raw_1752227465.png"

messages = [
    # SystemMessage(content="""Bạn là một trợ lý AI chuyên nhận diện vị trí cây kim trên đồng hồ checklist từ hình ảnh. Hãy xác định rõ cây kim đang nằm giữa hai giá trị nào trên đồng hồ, ví dụ: "Cây kim đang nằm giữa giá trị 1 và 2." Chỉ trả lời bằng hai giá trị gần nhất mà cây kim nằm giữa, không giải thích thêm."""),
    HumanMessage(
        content=[
            {"type": "text", "text": "trả cho tôi tọa độ các điểm màu đỏ, [x,y] label"},
            {"type": "image_url", "image_url": f"{encoded_image}"},
        ]
    )
]
# ...existing code...
# ...existing

ai_msg = llm.invoke(messages)
print(ai_msg.content)