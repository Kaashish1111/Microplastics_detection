import os

images = set(
    os.path.splitext(f)[0]
    for f in os.listdir("export/images")
)

labels = set(
    os.path.splitext(f)[0]
    for f in os.listdir("export/labels")
)

missing = labels - images

print(f"\nMissing Images: {len(missing)}\n")

for x in sorted(missing):
    print(x)