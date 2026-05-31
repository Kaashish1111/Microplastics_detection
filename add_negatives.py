import os

IMAGE_DIR = "new_negatives/Non_microplastic"
EXPORT_IMAGES = "export/images"
EXPORT_LABELS = "export/labels"

# ==========================================
# COPY IMAGES + CREATE EMPTY LABELS
# ==========================================

for file in os.listdir(IMAGE_DIR):

    if file.lower().endswith((".jpg", ".jpeg", ".png")):

        # Copy image
        src = os.path.join(IMAGE_DIR, file)

        dst = os.path.join(EXPORT_IMAGES, file)

        import shutil
        shutil.copy2(src, dst)

        # Create empty txt
        txt_name = os.path.splitext(file)[0] + ".txt"

        txt_path = os.path.join(EXPORT_LABELS, txt_name)

        open(txt_path, "w").close()

        print(f"Added negative: {file}")

print("\nDone!")