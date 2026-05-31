import os

IMAGE_DIR = "export/images"
LABEL_DIR = "export/labels"

# ==========================================
# GET IMAGE + LABEL BASENAMES
# ==========================================

images = set(
    os.path.splitext(f)[0]
    for f in os.listdir(IMAGE_DIR)
)

labels = set(
    os.path.splitext(f)[0]
    for f in os.listdir(LABEL_DIR)
)

# ==========================================
# FIND MISSING IMAGE LABELS
# ==========================================

missing = labels - images

print(f"\nMissing Images: {len(missing)}\n")

# ==========================================
# DELETE EMPTY LABELS ONLY
# ==========================================

deleted = 0

for name in sorted(missing):

    label_path = os.path.join(
        LABEL_DIR,
        name + ".txt"
    )

    # Delete only if empty
    if os.path.exists(label_path):

        if os.path.getsize(label_path) == 0:

            os.remove(label_path)

            print(f"Deleted: {label_path}")

            deleted += 1

print(f"\nTotal Empty Labels Deleted: {deleted}")