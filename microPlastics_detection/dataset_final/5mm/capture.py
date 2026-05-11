import cv2
import os

save_dir = "."

pipeline = (
    "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! "
    "nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! appsink"
)

cap = cv2.VideoCapture(pipeline)

# warmup
for _ in range(20):
    cap.read()

count = 0

print("Press j to capture")
print("Press q to quit")

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Frame not ready")
        continue

    cv2.imshow("Live", frame)

    key = cv2.waitKey(1)

    if key == ord('j'):
        filename = f"img_{count}.jpg"
        cv2.imwrite(filename, frame)
        print("Saved:", filename)
        count += 1

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
