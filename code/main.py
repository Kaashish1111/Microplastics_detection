from ultralytics import YOLO
import joblib
import cv2
import numpy as np
import pandas as pd
import json

# -----------------------------
# PATHS
# -----------------------------

YOLO_MODEL = r"D:\Microplastic Final Model\models\best.pt"

RF_MODEL = r"D:\Microplastic Final Model\models\size_rf.pkl"

# -----------------------------
# CLASS NAMES
# -----------------------------

CLASS_MAP = {
    0: "1mm",
    1: "2mm",
    2: "3mm",
    3: "4mm",
    4: "5mm"
}

# -----------------------------
# LOAD MODELS
# -----------------------------

model = YOLO(YOLO_MODEL)
rf = joblib.load(RF_MODEL)


def extract_features(mask):

    pts = mask.astype(np.float32)

    area = cv2.contourArea(pts)

    perimeter = cv2.arcLength(
        pts,
        True
    )

    x, y, w, h = cv2.boundingRect(
        pts
    )

    aspect_ratio = w / (h + 1e-6)

    features = pd.DataFrame(
        [[
            area,
            perimeter,
            w,
            h,
            aspect_ratio
        ]],
        columns=[
            "area",
            "perimeter",
            "width",
            "height",
            "aspect_ratio"
        ]
    )

    return features


def predict_image(image_path):

    results = model.predict(
        source=image_path,
        conf=0.25,
        verbose=False
    )

    output = {
        "particle_count": 0,
        "particles": []
    }

    for r in results:

        if r.masks is None:
            continue

        masks = r.masks.xy
        boxes = r.boxes

        for i, mask in enumerate(masks):

            features = extract_features(mask)

            size_pred = rf.predict(
                features
            )[0]

            cls = int(
                boxes.cls[i].cpu().numpy()
            )

            class_name = CLASS_MAP.get(
                cls,
                f"class_{cls}"
            )

            conf = float(
                boxes.conf[i].cpu().numpy()
            )

            box = (
                boxes.xyxy[i]
                .cpu()
                .numpy()
                .tolist()
            )

            output["particles"].append(
                {
                    "class_name": class_name,
                    "size_mm": round(
                        float(size_pred),
                        3
                    ),
                    "confidence": round(
                        conf,
                        3
                    ),
                    "bbox": box
                }
            )

    output["particle_count"] = len(
        output["particles"]
    )

    return output


if __name__ == "__main__":

    IMAGE = r"C:\Mtraining\dataset\test\images\2mm_4db0a084__image_288.jpg"

    result = predict_image(IMAGE)

    print(
        json.dumps(
            result,
            indent=4
        )
    )