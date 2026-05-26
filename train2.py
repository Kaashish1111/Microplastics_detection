from ultralytics import YOLO

model = YOLO("yolov8n-obb.pt")

model.train(
    data="data2.yaml",
    epochs=100,
    patience=10,
    imgsz=640,
    batch=8,
    device="mps"
)