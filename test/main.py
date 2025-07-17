from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Model dữ liệu gửi qua POST
class Item(BaseModel):
    name: str
    description: str = None
    price: float

# Route GET cơ bản
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# Route GET có tham số
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# Route POST cơ bản
@app.post("/items/")
def create_item(item: Item):
    return {"received_item": item}

# Khởi động ứng dụng khi chạy bằng python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
