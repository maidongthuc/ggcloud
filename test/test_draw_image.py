import cv2

# Đường dẫn ảnh
image_path = "./images/chim.jpg"

# Tọa độ bounding box (có thể điều chỉnh cho phù hợp)
box_2d = [433, 86, 908, 550]  # [x1, y1, x2, y2]
x1, y1, x2, y2 = box_2d

# Đọc ảnh
image = cv2.imread(image_path)

if image is None:
    print("Không thể tải ảnh. Kiểm tra lại đường dẫn.")
else:
    # In thông tin ảnh gốc
    original_height, original_width = image.shape[:2]
    print(f"Kích thước ảnh gốc: {original_width}x{original_height}")
    print(f"Bounding box hiện tại: [{x1}, {y1}, {x2}, {y2}]")
    
    # Kiểm tra tọa độ có hợp lệ không
    if x1 >= 0 and y1 >= 0 and x2 <= original_width and y2 <= original_height and x1 < x2 and y1 < y2:
        print("Tọa độ bounding box hợp lệ")
    else:
        print("CẢNH BÁO: Tọa độ bounding box có thể không hợp lệ!")
        print(f"Giới hạn ảnh: width={original_width}, height={original_height}")
    
    # Vẽ bounding box trên ảnh gốc để kiểm tra
    image_copy = image.copy()
    cv2.rectangle(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.putText(image_copy, "Bird", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Hiển thị ảnh gốc với bounding box
    cv2.imshow("Original Image with Bounding Box", image_copy)
    
    # Resize ảnh thành 1000x1000
    target_size = 1000
    image_resized = cv2.resize(image, (target_size, target_size))
    
    # Tính tỷ lệ scale
    scale_x = target_size / original_width
    scale_y = target_size / original_height
    
    # Scale bounding box coordinates
    x1_scaled = int(x1 * scale_x)
    y1_scaled = int(y1 * scale_y)
    x2_scaled = int(x2 * scale_x)
    y2_scaled = int(y2 * scale_y)
    
    # Vẽ bounding box trên ảnh đã resize
    cv2.rectangle(image_resized, (x1_scaled, y1_scaled), (x2_scaled, y2_scaled), (0, 255, 0), 3)
    cv2.putText(image_resized, "Bird", (x1_scaled, y1_scaled-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Hiển thị ảnh resized
    cv2.imshow("Resized Image (1000x1000)", image_resized)
    
    print(f"Tỷ lệ scale: x={scale_x:.3f}, y={scale_y:.3f}")
    print(f"Bounding box sau khi scale: [{x1_scaled}, {y1_scaled}, {x2_scaled}, {y2_scaled}]")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Lưu cả hai kết quả
    cv2.imwrite("result_original_with_bbox.jpg", image_copy)
    cv2.imwrite("result_resized_1000x1000.jpg", image_resized)
    print("Đã lưu kết quả:")
    print("- result_original_with_bbox.jpg (ảnh gốc)")
    print("- result_resized_1000x1000.jpg (ảnh 1000x1000)")