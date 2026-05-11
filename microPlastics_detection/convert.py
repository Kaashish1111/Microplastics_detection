import os
import json
from PIL import Image

predict_folders = {
    'runs/obb/predict-6':   'plastic_1mm',
    'runs/obb/predict-7': 'plastic_2mm',
    'runs/obb/predict-8': 'plastic_3mm',
    'runs/obb/predict-9': 'plastic_4mm',
    'runs/obb/predict-': 'plastic_5mm',
}

output_file = 'label_studio_import.json'
tasks = []

for predict_dir, class_name in predict_folders.items():
    labels_dir = os.path.join(predict_dir, 'labels')

    if not os.path.exists(predict_dir):
        print(f"❌ Missing: {predict_dir}")
        continue

    print(f"Processing {class_name} from {predict_dir}...")

    # Images are directly in predict folder
    for img_file in sorted(os.listdir(predict_dir)):
        if not img_file.endswith(('.jpg', '.png', '.jpeg')):
            continue

        img_path = os.path.join(predict_dir, img_file)
        with Image.open(img_path) as img:
            img_width, img_height = img.size

        label_file = img_file.rsplit('.', 1)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_file)

        task = {
            "data": {
                "image": f"/data/local-files/?d=/Users/coder_kashish/Downloads/microPlastics_detection/{predict_dir}/{img_file}"
            },
            "predictions": []
        }

        if os.path.exists(label_path):
            results = []
            with open(label_path) as f:
                for line in f:
                    values = line.strip().split()
                    if len(values) < 9:
                        continue

                    coords = [float(v) for v in values[1:9]]
                    x_coords = [coords[i] * 100 for i in range(0, 8, 2)]
                    y_coords = [coords[i] * 100 for i in range(1, 8, 2)]

                    x_min = min(x_coords)
                    y_min = min(y_coords)
                    width = max(x_coords) - x_min
                    height = max(y_coords) - y_min

                    results.append({
                        "type": "rectanglelabels",
                        "from_name": "label",
                        "to_name": "image",
                        "original_width": img_width,
                        "original_height": img_height,
                        "value": {
                            "x": x_min,
                            "y": y_min,
                            "width": width,
                            "height": height,
                            "rotation": 0,
                            "rectanglelabels": [class_name]
                        }
                    })

            if results:
                task["predictions"] = [{
                    "result": results,
                    "score": 0.9
                }]

        tasks.append(task)

    print(f"✅ {class_name} done!")

with open(output_file, 'w') as f:
    json.dump(tasks, f, indent=2)

print(f"\n✅ Total converted: {len(tasks)} images!")
print(f"📁 Saved to: {output_file}")