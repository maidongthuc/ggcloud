
prompt_cut_dry_chemical_fire_extinguisher_2 = "Detect the *dry chemical fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels."
prompt_cut_co2_fire_extinguisher_2 = "Detect the *co2 fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels."
prompt_cut_fire_extinguisher_2 = "Detect the *dry chemical fire extinguisher* and *co2 fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format."
prompt_cut_hose_co2_extinguisher_2 = "Detect the *hose of co2 fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format such as *hose_of_co2_fire_extinguisher*."
prompt_cut_fire_extinguisher_tray_2 = "Detect the *double fire extinguisher tray* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format such as *double_fire_extinguisher_tray*."
prompt_cut_pressure_gauge_fire_extinguisher_2 = "Detect the *pressure gauge of fire extinguisher* in the image. Output a JSON list of bounding boxes where each entry contains the 2D bounding box in the key \"box_2d\", and the text label in the key \"label\". Use descriptive labels in snake_case format such as *pressure_gauge*."
prompt_system_cut_fire_extinguisher_2 = "Large dry chemical fire extinguishers are bigger than co2 fire extinguishers."
def prompt_classification_2(list_images):
    PROMPT = (
        "You will receive a list of image URLs below. "
        "Please identify which images are photos of the fire extinguisher pressure gauge, "
        "which images are overview photos of the fire extinguisher from the front (overview_front), "
        "which images are overview photos of the fire extinguisher from the back (overview_back), "
        "and which images are of other types (other). "
        "Return the result as a JSON array, each entry containing the correct image URL and the image type with values: "
        "\"pressure_gauge\", \"overview_front\", \"overview_back\", or \"other\". "
        "Example: [{\"image_url\": \"...\", \"type\": \"pressure_gauge\"}, {\"image_url\": \"...\", \"type\": \"overview_front\"}, {\"image_url\": \"...\", \"type\": \"overview_back\"}, ...]\n"
        "List of images:\n"
        + "\n".join(list_images)
    )
    return PROMPT