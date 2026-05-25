import os
import random
import shutil

# ==========================================
# INPUT FOLDERS
# ==========================================

IMAGE_DIR = "export/images"
LABEL_DIR = "export/labels"

# ==========================================
# OUTPUT DATASET FOLDER
# ==========================================

OUTPUT_DIR = "dataset"

# ==========================================
# SPLIT RATIOS
# ==========================================

TRAIN_RATIO = 0.7
VALID_RATIO = 0.2
TEST_RATIO = 0.1

# ==========================================
# CREATE OUTPUT FOLDERS
# ==========================================

splits = ["train", "valid", "test"]

for split in splits:

    os.makedirs(
        os.path.join(OUTPUT_DIR, "images", split),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_DIR, "labels", split),
        exist_ok=True
    )

# ==========================================
# GET ALL IMAGE FILES
# ==========================================

image_files = []

for file in os.listdir(IMAGE_DIR):

    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        image_files.append(file)

# ==========================================
# SHUFFLE IMAGES
# ==========================================

random.shuffle(image_files)

# ==========================================
# CALCULATE SPLITS
# ==========================================

total_images = len(image_files)

train_count = int(total_images * TRAIN_RATIO)
valid_count = int(total_images * VALID_RATIO)

train_files = image_files[:train_count]

valid_files = image_files[
    train_count : train_count + valid_count
]

test_files = image_files[
    train_count + valid_count :
]

# ==========================================
# COPY FUNCTION
# ==========================================

def copy_files(files, split_name):

    for image_file in files:

        # IMAGE PATHS
        src_image = os.path.join(
            IMAGE_DIR,
            image_file
        )

        dst_image = os.path.join(
            OUTPUT_DIR,
            "images",
            split_name,
            image_file
        )

        shutil.copy(src_image, dst_image)

        # LABEL FILE
        label_file = os.path.splitext(image_file)[0] + ".txt"

        src_label = os.path.join(
            LABEL_DIR,
            label_file
        )

        dst_label = os.path.join(
            OUTPUT_DIR,
            "labels",
            split_name,
            label_file
        )

        # COPY LABEL IF EXISTS
        if os.path.exists(src_label):

            shutil.copy(src_label, dst_label)

        else:

            print(f"Missing label: {label_file}")

# ==========================================
# COPY TRAIN / VALID / TEST
# ==========================================

copy_files(train_files, "train")
copy_files(valid_files, "valid")
copy_files(test_files, "test")

# ==========================================
# FINAL OUTPUT
# ==========================================

print("\n====================================")
print("DATASET SPLIT COMPLETED SUCCESSFULLY")
print("====================================")

print(f"Total Images : {total_images}")
print(f"Train Images : {len(train_files)}")
print(f"Valid Images : {len(valid_files)}")
print(f"Test Images  : {len(test_files)}")

print("====================================")

print("\nDataset structure created:")

print("""
dataset/
├── images/
│   ├── train/
│   ├── valid/
│   └── test/
│
├── labels/
│   ├── train/
│   ├── valid/
│   └── test/
""")