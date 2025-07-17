import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.llm_gemini import llm
import threading
import time

def worker(name, message, results, results_lock, index):
    """Hàm worker với khả năng lưu kết quả"""
    try:
        ai_msg = llm.invoke(message)
        result = {
            "worker": name,
            "index": index,
            "status": "success",
            "translation": ai_msg.content
        }
        
        # Thread-safe thêm kết quả
        with results_lock:
            results.append(result)
            
    except Exception as e:
        # Thread-safe thêm lỗi
        with results_lock:
            results.append({
                "worker": name,
                "index": index,
                "status": "error",
                "error": str(e)
            })

# Shared list để lưu kết quả
results = []
results_lock = threading.Lock()

# Tạo và chạy threads
threads = []
messages = [
    [
        ("system", "You are a helpful assistant that translates English to French. Translate the user sentence."),
        ("human", "I love programming."),
    ],
    [
        ("system", "You are a helpful assistant that translates English to Viet Nam. Translate the user sentence."),
        ("human", "I love programming."),
    ],
    [
        ("system", "You are a helpful assistant that translates English to Japan. Translate the user sentence."),
        ("human", "I love programming."),
    ]
]

for i, message in enumerate(messages):
    thread = threading.Thread(
        target=worker, 
        args=(f"Worker-{i+1}", message, results, results_lock, i)
    )
    threads.append(thread)
    thread.start()

# Chờ tất cả threads hoàn thành
for thread in threads:
    thread.join()

# Sắp xếp kết quả theo index
results.sort(key=lambda x: x["index"])

print("Tất cả threads đã hoàn thành!")
print("Kết quả:")
for result in results:
    if result["status"] == "success":
        print(result)
    else:
        print(f"{result['worker']}: Error - {result['error']}")