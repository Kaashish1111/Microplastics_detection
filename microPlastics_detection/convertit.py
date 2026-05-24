import os
import json

# ==========================================
# GITHUB DETAILS
# ==========================================

USERNAME = "Kaashish1111"
REPO = "Microplastics_detection"

# ==========================================
# LOCAL PATH
# ==========================================

# Your actual local folders are inside:
# microPlastics_detection/runs/obb/

LOCAL_BASE_PATH = "microPlastics_detection/runs/obb"

# ==========================================
# GITHUB PATH
# ==========================================

# Your GitHub repo path is:
# microPlastics_detection/runs/obb/predict-6/image_01.jpg

BASE_GITHUB_PATH = "microPlastics_detection/runs/obb"

# ==========================================
# FOLDERS TO INCLUDE
# ==========================================

FOLDERS = [
    "predict-6",
    "predict-7",
    "predict-8",
    "predict-9",
    "predict-10"
]

# ==========================================
# OUTPUT FILE
# ==========================================

OUTPUT_JSON = "labelstudio_tasks.json"

# ==========================================
# CREATE TASKS
# ==========================================

tasks = []

for folder in FOLDERS:

    local_folder_path = os.path.join(LOCAL_BASE_PATH, folder)

    # Check if folder exists
    if not os.path.exists(local_folder_path):

        print(f"Folder not found: {local_folder_path}")
        continue

    print(f"\nProcessing folder: {folder}")

    # Read all images
    for img in os.listdir(local_folder_path):

        # Only image files
        if img.lower().endswith((".jpg", ".jpeg", ".png")):

            # ==========================================
            # CREATE RAW GITHUB URL
            # ==========================================

            image_url = (
                f"https://raw.githubusercontent.com/"
                f"{USERNAME}/{REPO}/main/"
                f"{BASE_GITHUB_PATH}/{folder}/{img}"
            )

            # ==========================================
            # LABEL STUDIO TASK
            # ==========================================

            task = {
                "data": {
                    "image": image_url,
                    "group": folder
                },

                # Placeholder predictions
                "predictions": [
                    {
                        "model_version": "microplastics-v1",
                        "result": []
                    }
                ]
            }

            tasks.append(task)

            print(f"Added: {img}")

# ==========================================
# SAVE JSON
# ==========================================

with open(OUTPUT_JSON, "w") as f:

    json.dump(tasks, f, indent=2)

# ==========================================
# DONE
# ==========================================

print("\n===================================")
print(f"DONE! Created {len(tasks)} tasks")
print(f"Saved as: {OUTPUT_JSON}")
print("===================================")