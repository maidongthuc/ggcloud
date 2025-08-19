data = [
      "excess_cable_length(bottom-right corner of the cabinet interior)",
      "debris_inside_cabinet(bottom-left area of the cabinet floor)",
      "improper_cable_routing(bottom-right corner of the cabinet interior)",
      "improper_cable_routing(bottom-center to bottom-left area, below the lower row of breakers)",
      "debris_inside_cabinet(entire bottom surface of the cabinet interior)",
      "non_standard_label(center of the clear plastic protective shield, below the main breakers)",
      "missing_circuit_labels(throughout the wiring, especially at terminal points and where wires enter breakers)",
      "signs_of_careless_work(bottom-left and bottom-right of the cabinet interior)",
      "exposed_conductor(bottom-left breaker, bottom terminal, blue wire)",
      "exposed_conductor(bottom-left breaker, second from left, bottom terminal, black wire)",
      "exposed_conductor(bottom-left breaker, third from left, bottom terminal, red wire)",
      "exposed_conductor(bottom-left breaker, fourth from left, bottom terminal, yellow wire)"
    ]

def detection_object(list_label):
    # Wrap each object with **object**
    wrapped_objects = [f"**{label}**" for label in list_label]
    objects = ", ".join(wrapped_objects)
    prompt = f"""- Only detect the {objects} in the image.  
- Output the result as a **JSON list** of bounding boxes, where each entry contains:
  - `box_2d`: [y1, x1, y2, x2]
  - `label`: object name in `snake_case` format."""
    return prompt

print(detection_object(data))