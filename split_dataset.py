import os
import random
import shutil

source_dir = r"C:\Users\elabi\Downloads\photo_scan_ai\data\Plant_leave_diseases_dataset"

output_dir = r"C:\Users\elabi\Downloads\photo_scan_ai\data\plant_images"

train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

for folder in ["train", "val", "test"]:
    os.makedirs(os.path.join(output_dir, folder), exist_ok=True)

classes = os.listdir(source_dir)

for c in classes:

    class_path = os.path.join(source_dir, c)

    if not os.path.isdir(class_path):
        continue

    images = os.listdir(class_path)
    random.shuffle(images)

    total = len(images)

    train_end = int(total * train_ratio)
    val_end = int(total * (train_ratio + val_ratio))

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    print(f"\nClasse : {c}")
    print(f"Total images : {total}")
    print(f"Train : {len(train_images)}")
    print(f"Val : {len(val_images)}")
    print(f"Test : {len(test_images)}")

    splits = {
        "train": train_images,
        "val": val_images,
        "test": test_images
    }

    for split, imgs in splits.items():

        split_class_dir = os.path.join(output_dir, split, c)
        os.makedirs(split_class_dir, exist_ok=True)

        for i, img in enumerate(imgs):

            src = os.path.join(class_path, img)
            dst = os.path.join(split_class_dir, img)

            shutil.move(src, dst)

            if i % 100 == 0:
                print(f"{c} - {split} : {i}/{len(imgs)}")

print("\nDataset split terminé !")