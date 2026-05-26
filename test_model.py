from ultralytics import YOLO

# Load trained model
model = YOLO("runs/obb/train/weights/best.pt")

# Evaluate on test set
metrics = model.val(
    data="data.yaml",
    split="test"
)

print(metrics)