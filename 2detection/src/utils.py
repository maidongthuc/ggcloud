import re
import json
import numpy as np
def parse_json_from_llm_response(llm_content):
    """
    Loại bỏ markdown code block khỏi chuỗi JSON và parse thành dict.
    """
    cleaned_text = re.sub(r'^```json\s*|\s*```$', '', llm_content, flags=re.DOTALL)
    return json.loads(cleaned_text)

def calculate_bbox(detection, w, h):
    for det in detection:
        y1, x1, y2, x2 = det["box_2d"]
        label = det["label"]

        # Nếu bbox là tọa độ chuẩn hóa (0-1000), scale về pixel thực tế
        x1 = int(x1 / 1000 * w)
        y1 = int(y1 / 1000 * h)
        x2 = int(x2 / 1000 * w)
        y2 = int(y2 / 1000 * h)

        # Cập nhật lại vào json
        det["box_2d"] = [x1, y1, x2, y2]
    return detection

def get_union_bbox_by_prefix(data, prefix, total_label):
    """
    Trả về bbox tổng hợp cho các object có label bắt đầu bằng prefix.
    """
    objects = [obj for obj in data if obj['label'].startswith(prefix)]
    if not objects:
        return None
    bbox = calculate_union_bbox(objects)
    return {'box_2d': bbox, 'label': total_label}

def calculate_union_bbox(objects):
    """
    Tính bbox bao phủ tất cả các box trong danh sách.
    """
    if not objects:
        return []
    boxes = np.array([obj['box_2d'] for obj in objects])
    x_min = boxes[:, 0].min()
    y_min = boxes[:, 1].min()
    x_max = boxes[:, 2].max()
    y_max = boxes[:, 3].max()
    return [int(x_min), int(y_min), int(x_max), int(y_max)]

def build_detection_results(data):
    """
    Trả về danh sách kết quả detection gồm bbox tổng hợp và tray nếu có.
    """
    results = []
    co2_result = get_union_bbox_by_prefix(data, 'co2_fire_extinguisher', 'co2_fire_extinguisher_total')
    dry_result = get_union_bbox_by_prefix(data, 'dry_chemical_fire_extinguisher', 'dry_chemical_fire_extinguisher_total')
    if co2_result:
        results.append(co2_result)
    if dry_result:
        results.append(dry_result)
    tray = next((obj for obj in data if obj['label'] == 'fire_extinguisher_tray'), None)
    if tray:
        results.append(tray)
    return results