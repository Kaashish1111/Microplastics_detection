import os
import shutil
from PIL import Image
import imagehash

# -----------------------------
# PATHS
# -----------------------------
TRAIN_PATH = "dataset/images/train"
VAL_PATH = "dataset/images/valid"
TEST_PATH = "dataset/images/test"

# Similarity threshold
# Lower = stricter
HASH_THRESHOLD = 5

# -----------------------------
# FUNCTION TO GET IMAGE HASH
# -----------------------------
def get_hash(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        return imagehash.phash(img)
    except:
        return None

# -----------------------------
# LOAD IMAGE HASHES
# -----------------------------
def load_hashes(folder):
    hashes = {}

    for file in os.listdir(folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):

            path = os.path.join(folder, file)

            h = get_hash(path)

            if h is not None:
                hashes[file] = h

    return hashes

print("Loading hashes...")

train_hashes = load_hashes(TRAIN_PATH)
val_hashes = load_hashes(VAL_PATH)
test_hashes = load_hashes(TEST_PATH)

print("Hashes loaded!")

# -----------------------------
# CHECK DUPLICATES
# -----------------------------
duplicates = []

# VALID vs TRAIN
for val_file, val_hash in val_hashes.items():

    for train_file, train_hash in train_hashes.items():

        distance = val_hash - train_hash

        if distance <= HASH_THRESHOLD:

            duplicates.append(
                ("VALID", val_file, "TRAIN", train_file, distance)
            )

# TEST vs TRAIN
for test_file, test_hash in test_hashes.items():

    for train_file, train_hash in train_hashes.items():

        distance = test_hash - train_hash

        if distance <= HASH_THRESHOLD:

            duplicates.append(
                ("TEST", test_file, "TRAIN", train_file, distance)
            )

# TEST vs VALID
for test_file, test_hash in test_hashes.items():

    for val_file, val_hash in val_hashes.items():

        distance = test_hash - val_hash

        if distance <= HASH_THRESHOLD:

            duplicates.append(
                ("TEST", test_file, "VALID", val_file, distance)
            )

# -----------------------------
# PRINT RESULTS
# -----------------------------
print("\nPossible duplicates found:\n")

for dup in duplicates:

    print(
        f"{dup[0]}: {dup[1]}  <-->  "
        f"{dup[2]}: {dup[3]}  | Distance = {dup[4]}"
    )

print(f"\nTotal possible duplicates: {len(duplicates)}")