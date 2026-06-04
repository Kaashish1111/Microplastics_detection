import os
import cv2
import numpy as np
import pandas as pd

ROOT = "data_set"

CLASS_TO_SIZE = {
    "1mm": 1.0,
    "2mm": 2.0,
    "3mm": 3.0,
    "4mm": 4.0,
    "5mm": 5.0
}

rows = []

for folder, size in CLASS_TO_SIZE.items():

    image_dir = os.path.join(ROOT, folder, "images")
    label_dir = os.path.join(ROOT, folder, "labels")

    for file in os.listdir(label_dir):

        if not file.endswith(".txt"):
            continue

        label_path = os.path.join(label_dir, file)

        stem = os.path.splitext(file)[0]

        image_path = None
        for ext in [".jpg", ".jpeg", ".png"]:
            p = os.path.join(image_dir, stem + ext)
            if os.path.exists(p):
                image_path = p
                break

        if image_path is None:
            continue

        img = cv2.imread(image_path)
        h_img, w_img = img.shape[:2]

        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:

            vals = list(map(float, line.strip().split()))

            pts = np.array(vals[1:]).reshape(-1, 2)

            pts[:, 0] *= w_img
            pts[:, 1] *= h_img

            pts = pts.astype(np.float32)

            area = cv2.contourArea(pts)

            perimeter = cv2.arcLength(pts, True)

            x, y, w, h = cv2.boundingRect(pts)

            aspect_ratio = w / (h + 1e-6)

            rows.append([
                area,
                perimeter,
                w,
                h,
                aspect_ratio,
                size
            ])

df = pd.DataFrame(
    rows,
    columns=[
        "area",
        "perimeter",
        "width",
        "height",
        "aspect_ratio",
        "target_size"
    ]
)

df.to_csv("regression_dataset_v2.csv", index=False)

print(df.head())
print()
print(df.describe())
print()
print("Samples:", len(df))