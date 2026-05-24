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
# LABEL NAME
# ==========================================

CLASS_MAP = {
    0: "Microplastic"
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

                    # ==========================================
                    # YOLO OBB FORMAT
                    # class x1 y1 x2 y2 x3 y3 x4 y4
                    # ==========================================

                    cls = int(parts[0])

                    coords = list(map(float, parts[1:]))

                    points = []

                    for i in range(0, len(coords), 2):

                        x = coords[i] * 100
                        y = coords[i + 1] * 100

                        points.append([x, y])

                    result = {
                        "original_width": img_width,
                        "original_height": img_height,
                        "image_rotation": 0,

                        "value": {
                            "points": points,
                            "polygonlabels": [CLASS_MAP[cls]]
                        },

                        "from_name": "label",
                        "to_name": "image",
                        "type": "polygonlabels"
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