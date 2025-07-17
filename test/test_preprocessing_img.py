import cv2
import numpy as np
import math

# Load ảnh và xử lý
img = cv2.imread('/home/acer/Work/ai-research/detection/static/images/raw/checklist/checklist_clock_0_1752133474.png')
original = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Tăng cường tương phản
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)

# Blur và edge detection
blur = cv2.GaussianBlur(enhanced, (3, 3), 0)
edges = cv2.Canny(blur, 30, 100)

# Phát hiện đường tròn (đồng hồ)
circles = cv2.HoughCircles(enhanced, cv2.HOUGH_GRADIENT, 1, 100,
                           param1=50, param2=30, minRadius=80, maxRadius=200)

if circles is not None:
    x_center, y_center, radius = np.uint16(np.around(circles[0, 0]))
    
    # Vẽ đường tròn đồng hồ
    cv2.circle(img, (x_center, y_center), radius, (255, 0, 0), 2)
    cv2.circle(img, (x_center, y_center), 3, (0, 255, 0), -1)
    
    # Phát hiện các đường thẳng
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=30, 
                           minLineLength=5, maxLineGap=3)
    
    major_ticks = []
    minor_ticks = []
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Tính khoảng cách từ 2 đầu đường thẳng đến tâm
            dist1 = np.hypot(x1 - x_center, y1 - y_center)
            dist2 = np.hypot(x2 - x_center, y2 - y_center)
            length = np.hypot(x2 - x1, y2 - y1)
            
            # Tính góc của đường thẳng
            angle = math.atan2(y2 - y1, x2 - x1) * 180 / np.pi
            
            # Kiểm tra xem đường thẳng có phải là vạch chia không
            # Điều kiện 1: Một đầu gần tâm, một đầu xa tâm (radial line)
            min_dist = min(dist1, dist2)
            max_dist = max(dist1, dist2)
            
            # Điều kiện 2: Vạch phải nằm trong vùng đồng hồ
            if (min_dist > radius * 0.6 and max_dist < radius * 1.1 and 
                length > 8 and length < radius * 0.4):
                
                # Phân loại vạch chính và vạch phụ
                if length > 15:  # Vạch chính (12, 3, 6, 9 giờ)
                    major_ticks.append((x1, y1, x2, y2, angle, length))
                    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Đỏ
                else:  # Vạch phụ
                    minor_ticks.append((x1, y1, x2, y2, angle, length))
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1)  # Vàng
    
    # Sắp xếp các vạch theo góc
    major_ticks.sort(key=lambda x: x[4])  # Sắp xếp theo góc
    minor_ticks.sort(key=lambda x: x[4])
    
    print(f"Tìm thấy {len(major_ticks)} vạch chính")
    print(f"Tìm thấy {len(minor_ticks)} vạch phụ")
    
    # In thông tin các vạch chính
    for i, (x1, y1, x2, y2, angle, length) in enumerate(major_ticks):
        hour_position = (angle + 90) % 360 / 30  # Chuyển đổi góc thành vị trí giờ
        print(f"Vạch chính {i+1}: Góc={angle:.1f}°, Độ dài={length:.1f}, Vị trí≈{hour_position:.1f}h")

else:
    print("Không tìm thấy đồng hồ!")

# Hiển thị kết quả
cv2.imshow("Original", original)
cv2.imshow("Enhanced", enhanced)
cv2.imshow("Edges", edges)
cv2.imshow("Clock Tick Marks", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Lưu kết quả
cv2.imwrite('/home/acer/Work/ai-research/detection/static/images/processed/clock_ticks_detected.png', img)
print("Đã lưu kết quả vào clock_ticks_detected.png")