import os, shutil, random

# Paths
images = os.listdir('images/')
random.shuffle(images)

train = images[:98]      # 70%
val = images[98:119]     # 15%
test = images[119:]      # 15%

for split, files in [('train', train), ('val', val), ('test', test)]:
    os.makedirs(f'dataset/{split}/images', exist_ok=True)
    os.makedirs(f'dataset/{split}/labels', exist_ok=True)
    for f in files:
        shutil.copy(f'images/{f}', f'dataset/{split}/images/{f}')
        label = f.replace('.jpg', '.txt').replace('.png', '.txt')
        shutil.copy(f'labels/{label}', f'dataset/{split}/labels/{label}')

print("Split done!")