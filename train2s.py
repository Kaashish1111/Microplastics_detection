from ultralytics import YOLO
import time
# =========================================
# START TIMER
# =========================================
start_time = time.time()
# =========================================
# LOAD MODEL
# =========================================
model = YOLO("yolov8s-obb.pt")
# =========================================
# TRAIN MODEL
# =========================================
model.train(
    data="data2.yaml",
    epochs=100,
    patience=10,
    imgsz=640,
    batch=8,
    device="mps",
    resume=False, 
    exist_ok=False
)
# =========================================
# END TIMER
# =========================================
end_time = time.time()
# =========================================
# CALCULATE TIME
# =========================================
total_seconds = end_time - start_time
minutes = total_seconds / 60
hours = minutes / 60
# =========================================
# PRINT RESULTS
# =========================================
print("\n===================================")
print("TRAINING COMPLETED")
print("===================================")
print(f"\nTotal Time (seconds): {total_seconds:.2f}")
print(f"Total Time (minutes): {minutes:.2f}")
print(f"Total Time (hours): {hours:.2f}")