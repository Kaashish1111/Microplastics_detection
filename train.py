from ultralytics import YOLO

# Load OBB model
model = YOLO("yolov8n-obb.pt")

# Train
model.train(
    data="data.yaml",
    epochs=100,
    patience=10,
    imgsz=640,
    batch=8,
    device="mps"
)