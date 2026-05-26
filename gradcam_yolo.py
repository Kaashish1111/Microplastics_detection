from ultralytics import YOLO

import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt

from pytorch_grad_cam import EigenCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

# =========================================
# WRAPPER MODEL
# =========================================

class YOLOWrapper(torch.nn.Module):

    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x):

        outputs = self.model(x)

        # YOLO returns tuple
        if isinstance(outputs, tuple):
            outputs = outputs[0]

        return outputs

# =========================================
# LOAD MODEL
# =========================================

yolo = YOLO("runs/obb/train/weights/best.pt")

net = YOLOWrapper(yolo.model)

net.eval()

# =========================================
# IMAGE PATH
# =========================================

image_path = "dataset2/images/test/ff4e192d__image_160.jpg"
# =========================================
# LOAD IMAGE
# =========================================

img = cv2.imread(image_path)

if img is None:
    raise ValueError(f"Cannot load image: {image_path}")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_resized = cv2.resize(img, (640, 640))

img_float = img_resized.astype(np.float32) / 255.0

# =========================================
# PREPARE INPUT TENSOR
# =========================================

tensor = np.transpose(img_float, (2, 0, 1))

tensor = np.expand_dims(tensor, axis=0)

tensor = torch.from_numpy(tensor).float()

# =========================================
# TARGET LAYER
# =========================================

target_layers = [net.model.model[-2]]

# =========================================
# CAM
# =========================================

cam = EigenCAM(
    model=net,
    target_layers=target_layers
)

# IMPORTANT FIX
grayscale_cam = cam(
    input_tensor=tensor,
    targets=None
)

grayscale_cam = grayscale_cam[0]

# =========================================
# OVERLAY
# =========================================

visualization = show_cam_on_image(
    img_float,
    grayscale_cam,
    use_rgb=True
)

# =========================================
# SAVE
# =========================================

cv2.imwrite(
    "gradcam_output.jpg",
    cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR)
)

print("\nSaved: gradcam_output2.jpg")

# =========================================
# DISPLAY
# =========================================

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(visualization)
plt.title("EigenCAM")
plt.axis("off")

plt.tight_layout()

plt.show()