import os
import json
from PIL import Image

# ==========================================
# GITHUB DETAILS
# ==========================================

USERNAME = "Kaashish1111"
REPO = "Microplastics_detection"

# ==========================================
# PATHS
# ==========================================

BASE_PATH = "microPlastics_detection/runs/obb"

FOLDERS = [
    "predict-6",
    "predict-7",
    "predict-8",
    "predict-9",
    "predict-10"
]

OUTPUT_JSON = "labelstudio_tasks.json"

# ==========================================
# LABEL
# ==========================================

CLASS_MAP = {
    0: "plastic"
}

# ==========================================
# CREATE TASKS
# ==========================================

tasks = []

for folder in FOLDERS:

    image_folder = os.path.join(BASE_PATH, folder)
    label_folder = os.path.join(image_folder, "labels")

    if not os.path.exists(image_folder):
        print(f"Folder not found: {image_folder}")
        continue

    print(f"\nProcessing: {folder}")

    for img_name in os.listdir(image_folder):

        if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(image_folder, img_name)

        # ==========================================
        # IMAGE SIZE
        # ==========================================

        image = Image.open(img_path)
        img_width, img_height = image.size

        # ==========================================
        # RAW GITHUB URL
        # ==========================================

        image_url = (
            f"https://raw.githubusercontent.com/"
            f"{USERNAME}/{REPO}/main/"
            f"{BASE_PATH}/{folder}/{img_name}"
        )

        # ==========================================
        # LABEL FILE
        # ==========================================

        label_name = os.path.splitext(img_name)[0] + ".txt"
        label_path = os.path.join(label_folder, label_name)

        results = []

        if os.path.exists(label_path):

            with open(label_path, "r") as f:

                lines = f.readlines()

                for line in lines:

                    parts = line.strip().split()

                    cls = int(parts[0])

                    coords = list(map(float, parts[1:]))

                    xs = coords[0::2]
                    ys = coords[1::2]

                    # ==========================================
                    # CONVERT POLYGON TO RECTANGLE
                    # ==========================================

                    min_x = min(xs)
                    max_x = max(xs)

                    min_y = min(ys)
                    max_y = max(ys)

                    x = min_x * 100
                    y = min_y * 100

                    width = (max_x - min_x) * 100
                    height = (max_y - min_y) * 100

                    result = {
                        "original_width": img_width,
                        "original_height": img_height,
                        "image_rotation": 0,

                        "value": {
                            "x": x,
                            "y": y,
                            "width": width,
                            "height": height,
                            "rotation": 0,
                            "rectanglelabels": [CLASS_MAP[cls]]
                        },

                        "from_name": "label",
                        "to_name": "image",
                        "type": "rectanglelabels"
                    }

                    results.append(result)

        # ==========================================
        # LABEL STUDIO TASK
        # ==========================================

        task = {
            "data": {
                "image": image_url,
                "group": folder
            },

            "predictions": [
                {
                    "model_version": "yolov8-obb",
                    "result": results
                }
            ]
        }

        tasks.append(task)

        print(f"Added: {img_name}")

# ==========================================
# SAVE JSON
# ==========================================

with open(OUTPUT_JSON, "w") as f:

    json.dump(tasks, f, indent=2)

print("\n===================================")
print(f"DONE! Created {len(tasks)} tasks")
print(f"Saved as: {OUTPUT_JSON}")
print("===================================")