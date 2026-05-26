from ultralytics import YOLO

# =========================================
# LOAD TRAINED MODEL
# =========================================

model = YOLO("runs/obb/train/weights/best.pt")

print("\n===================================")
print("MODEL LOADED SUCCESSFULLY")
print("===================================")

# =========================================
# VALIDATION / TESTING
# =========================================

metrics = model.val(
    data="data.yaml",
    split="test"
)

print("\n===================================")
print("TESTING COMPLETED")
print("===================================")

print(metrics)

# =========================================
# RUN PREDICTIONS
# =========================================

results = model.predict(
    source="dataset/images/test",
    save=True,
    conf=0.25
)

print("\n===================================")
print("PREDICTIONS COMPLETED")
print("===================================")