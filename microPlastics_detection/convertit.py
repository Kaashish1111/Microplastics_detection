import os
import json

# ==========================================
# GITHUB DETAILS
# ==========================================

USERNAME = "Kaashish1111"
REPO = "Microplastics_detection"

# ==========================================
# LOCAL FOLDER PATH
# ==========================================

# Your folders:
# runs/obb/predict-6
# runs/obb/predict-7
# etc.

LOCAL_BASE_PATH = "runs/obb"

# ==========================================
# GITHUB PATH
# ==========================================

# GitHub repo structure:
# runs/obb/predict-6/image_1.jpg

BASE_GITHUB_PATH = "runs/obb"

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
            # CREATE RAW GITHUB IMAGE URL
            # ==========================================

            image_url = (
                f"https://raw.githubusercontent.com/"
                f"{USERNAME}/{REPO}/main/"
                f"{BASE_GITHUB_PATH}/{folder}/{img}"
            )

            # ==========================================
            # CREATE LABEL STUDIO TASK
            # ==========================================

            task = {
                "data": {
                    "image": image_url,
                    "group": folder
                },

                # Placeholder for semi-auto predictions
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
# SAVE JSON FILE
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