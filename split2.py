import os
import shutil
from PIL import Image
import imagehash

# =====================================================
# PATHS
# =====================================================

IMAGE_DIR = "export/images"
LABEL_DIR = "export/labels"

OUTPUT_DIR = "dataset2"

# =====================================================
# SETTINGS
# =====================================================

HASH_THRESHOLD = 1

TRAIN_RATIO = 0.7
VALID_RATIO = 0.2
TEST_RATIO  = 0.1

# =====================================================
# CREATE OUTPUT FOLDERS
# =====================================================

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

# =====================================================
# LOAD IMAGE FILES
# =====================================================

image_files = sorted([
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

print(f"\nTotal images found: {len(image_files)}")

# =====================================================
# COMPUTE HASHES
# =====================================================

print("\nComputing image hashes...")

hashes = {}

for file in image_files:

    path = os.path.join(IMAGE_DIR, file)

    try:

        img = Image.open(path).convert("RGB")

        h = imagehash.phash(img)

        hashes[file] = h

    except:

        print(f"Could not process: {file}")

print("Hash computation completed!")

# =====================================================
# GROUP SIMILAR IMAGES
# =====================================================

print("\nGrouping similar images...")

visited = set()

groups = []

for file1 in image_files:

    if file1 in visited:
        continue

    group = [file1]

    visited.add(file1)

    hash1 = hashes[file1]

    for file2 in image_files:

        if file2 in visited:
            continue

        hash2 = hashes[file2]

        distance = hash1 - hash2

        if distance <= HASH_THRESHOLD:

            group.append(file2)

            visited.add(file2)

    groups.append(group)

print(f"\nTotal groups created: {len(groups)}")

# =====================================================
# SPLIT GROUPS
# =====================================================

total_groups = len(groups)

train_end = int(TRAIN_RATIO * total_groups)

valid_end = int((TRAIN_RATIO + VALID_RATIO) * total_groups)

train_groups = groups[:train_end]

valid_groups = groups[train_end:valid_end]

test_groups = groups[valid_end:]

# =====================================================
# COPY FUNCTION
# =====================================================

def copy_group(group_list, split_name):

    print(f"\nCopying {split_name} data...")

    total = 0

    for group in group_list:

        for image_file in group:

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

            if os.path.exists(src_label):

                shutil.copy(src_label, dst_label)

            total += 1

    return total

# =====================================================
# COPY DATA
# =====================================================

train_count = copy_group(train_groups, "train")

valid_count = copy_group(valid_groups, "valid")

test_count = copy_group(test_groups, "test")

# =====================================================
# FINAL SUMMARY
# =====================================================

print("\n====================================")
print("SIMILARITY-AWARE SPLIT COMPLETED")
print("====================================")

print(f"Train Images : {train_count}")
print(f"Valid Images : {valid_count}")
print(f"Test Images  : {test_count}")

print(f"\nTotal Groups : {len(groups)}")

print("\nDataset ready!")