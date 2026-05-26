import os

# =========================
# LABELS FOLDER PATH
# =========================

LABELS_PATH = "export/labels"

# =========================
# CHECK EMPTY LABELS
# =========================

empty_files = []

for root, dirs, files in os.walk(LABELS_PATH):

    for file in files:

        if file.endswith(".txt"):

            path = os.path.join(root, file)

            # Read file
            with open(path, "r") as f:
                content = f.read().strip()

            # If empty
            if content == "":
                empty_files.append(path)

# =========================
# RESULTS
# =========================

print("\n==========================")
print("EMPTY LABEL FILES")
print("==========================\n")

for file in empty_files:
    print(file)

print(f"\nTotal Empty Labels: {len(empty_files)}")