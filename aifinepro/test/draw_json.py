data = [
  {
    "item": "Seiri",
    "status": "OK",
    "reason": "The cabinet is free of unnecessary items, tools, or debris. Only essential electrical components are present.",
    "defective_objects": []
  },
  {
    "item": "Seiton",
    "status": "NG",
    "reason": "Wire management is poor. Incoming and outgoing cables are messy and not neatly routed.",
    "defective_objects": [
      {
        "label": "messy_incoming_wires",
        "box_2d": [139, 396, 245, 597],
        "issue": "Incoming power cables are not neatly bundled or routed, creating a disorganized appearance."
      },
      {
        "label": "tangled_outgoing_wires",
        "box_2d": [785, 348, 977, 611],
        "issue": "Outgoing three-phase wires are tangled and excessively long instead of being routed neatly to their exit point."
      }
    ]
  },
  {
    "item": "Seiso",
    "status": "NG",
    "reason": "There is visible debris and metal shavings on the bottom of the cabinet, which can be a conductivity hazard.",
    "defective_objects": [
      {
        "label": "debris_in_cabinet",
        "box_2d": [880, 161, 998, 843],
        "issue": "Small particles, likely metal shavings from installation, are present on the cabinet floor."
      }
    ]
  },
  {
    "item": "Seiketsu",
    "status": "NG",
    "reason": "Standardization is lacking; labeling is non-durable (handwritten), and an incorrect wire color is used for grounding.",
    "defective_objects": [
      {
        "label": "non_standard_labeling",
        "box_2d": [447, 308, 484, 492],
        "issue": "Handwritten markings on the protective shield are not a durable or standard method for labeling."
      },
      {
        "label": "unlabeled_breakers",
        "box_2d": [492, 186, 706, 804],
        "issue": "Circuit breakers are not labeled to identify the circuits they protect."
      },
      {
        "label": "improper_grounding_wire_color",
        "box_2d": [121, 584, 287, 782],
        "issue": "A white wire is used for the main equipment ground, which violates standard color codes (should be green or green/yellow)."
      }
    ]
  },
  {
    "item": "Shitsuke",
    "status": "NG",
    "reason": "The poor quality of workmanship, including messy wiring and damaged insulation, indicates a lack of discipline and failure to sustain standards.",
    "defective_objects": [
      {
        "label": "careless_workmanship",
        "box_2d": [139, 396, 245, 597],
        "issue": "The combination of messy wiring, damaged insulation, and leftover debris points to a lack of adherence to quality and safety standards."
      }
    ]
  },
  {
    "item": "Safety",
    "status": "NG",
    "reason": "There are critical safety hazards, including damaged wire insulation on a main conductor and improper color-coding for the ground wire.",
    "defective_objects": [
      {
        "label": "damaged_wire_insulation",
        "box_2d": [140, 462, 219, 563],
        "issue": "The insulation on the main incoming white wire is frayed, exposing the inner layers and creating a severe shock or short circuit risk."
      },
      {
        "label": "improper_grounding_wire",
        "box_2d": [121, 584, 287, 782],
        "issue": "Using a white wire (typically neutral) for grounding can lead to dangerous confusion and miswiring during maintenance, posing a serious safety risk."
      }
    ]
  }
]

for i in data:
    if len(i['defective_objects']) > 0:
        for j in i['defective_objects']:
            print(j)