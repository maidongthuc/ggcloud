from PIL import Image, ImageDraw, ImageFont
# Đường dẫn ảnh gốc
image_path = "static/images/raw/checklist/checklist_clock_0_1752133474.png"

# Danh sách các điểm và nhãn
# points = [
#   {"point": [497, 530], "label": "base_of_the_gauge_needle"},
#   {"point": [620, 250], "label": "tip_of_the_gauge_needle"}
# ]
points = [
  {"point": [300, 200], "label": "0.4"},
  # {"point": [420, 290], "label": "0.5"},
  # {"point": [370, 490], "label": "0.6"},
  # {"point": [420, 290], "label": "0.7"},
  # {"point": [420, 290], "label": "0.8"},
  # {"point": [370, 490], "label": "needle tip"},
  # {"point": [420, 290], "label": "needle base"},
]

try:
    # Sử dụng font hệ thống (nếu có)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=30)
except:
    # Fallback sang font mặc định với size
    font = ImageFont.load_default()

# Mở ảnh
img = Image.open(image_path)
w,h = img.size[:2]
print(f"Image size: {w}x{h}")
draw = ImageDraw.Draw(img)

# Vẽ các điểm và nhãn
for item in points:
    x, y = item["point"]
    x = int(x / 1000 * w)  # Chuyển đổi tỷ lệ x
    y = int(y / 1000 * h)  # Chuyển đổi tỷ
    label = item["label"]
    r = 6
    draw.ellipse((x - r, y - r, x + r, y + r), fill="red")
    draw.text((x - 25, y - 40), label, fill="red", font=font)

# Hiển thị ảnh thay vì lưu
img.show()