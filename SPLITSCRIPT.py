import os, random, shutil

base_path = "fruit_dataset"
# Changed "Image" to "images" to match YOLO standards
images_path = os.path.join(base_path, "images") 
labels_path = os.path.join(base_path, "labels")

train_images = os.path.join(images_path, "train")
val_images   = os.path.join(images_path, "val")
train_labels = os.path.join(labels_path, "train")
val_labels   = os.path.join(labels_path, "val")

for folder in [train_images, val_images, train_labels, val_labels]:
    os.makedirs(folder, exist_ok=True)

# Get all image files
images = [f for f in os.listdir(images_path)
          if os.path.isfile(os.path.join(images_path, f))
          and f.lower().endswith((".jpg", ".jpeg", ".png"))]

random.seed(42)
random.shuffle(images)

split_index = int(0.8 * len(images))
train_files = images[:split_index]
val_files   = images[split_index:]

missing = []

def move_pair(img_file, img_dst_dir, lbl_dst_dir):
    stem = os.path.splitext(img_file)[0]
    src_img = os.path.join(images_path, img_file)
    src_lbl = os.path.join(labels_path, stem + ".txt")

    # Move the image
    shutil.move(src_img, os.path.join(img_dst_dir, img_file))

    # Move the label if it exists
    if os.path.exists(src_lbl):
        shutil.move(src_lbl, os.path.join(lbl_dst_dir, stem + ".txt"))
    else:
        missing.append(img_file)

for f in train_files:
    move_pair(f, train_images, train_labels)

for f in val_files:
    move_pair(f, val_images, val_labels)

print(f"Split complete: {len(train_files)} train / {len(val_files)} val")
if missing:
    print(f"⚠️ Warning: Found {len(missing)} images without labels.")