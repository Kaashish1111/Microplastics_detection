import os

image_folder = 'images'
label_folder = 'labels'

for img in os.listdir(image_folder):
    if img.endswith('.jpg') or img.endswith('.png'):
        label_name = img.replace('.jpg', '.txt').replace('.png', '.txt')
        label_path = os.path.join(label_folder, label_name)
        
        if not os.path.exists(label_path):
            open(label_path, 'w').close()
            print(f"Created empty label for {img}")

print("Done!")