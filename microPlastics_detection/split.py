import os
import random
import shutil

image_dir = 'images'
label_dir = 'labels'

images = os.listdir(image_dir)
random.shuffle(images)

split = int(0.8 * len(images))

train_images = images[:split]
val_images = images[split:]

# Move files
for img in train_images:
    shutil.copy(os.path.join(image_dir, img), 'dataset/train/images/' + img)
    
    label = img.replace('.jpg', '.txt')
    shutil.copy(os.path.join(label_dir, label), 'dataset/train/labels/' + label)

for img in val_images:
    shutil.copy(os.path.join(image_dir, img), 'dataset/val/images/' + img)
    
    label = img.replace('.jpg', '.txt')
    shutil.copy(os.path.join(label_dir, label), 'dataset/val/labels/' + label)