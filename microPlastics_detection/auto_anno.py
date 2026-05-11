from ultralytics import YOLO

model = YOLO('runs/obb/train/weights/best.pt')

results = model.predict(
    source='dataset_final/5mm',
    save=True,
    save_txt=True,
    conf=0.5,
    show_labels=False,
    show_conf=False
)