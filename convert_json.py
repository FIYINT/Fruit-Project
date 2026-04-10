import json
import os

# CONFIG - This matches your uploaded file exactly
json_file = "labels_project.json" 
output_folder = "labels_output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(json_file, 'r') as f:
    data = json.load(f)

# Map Image IDs to details
images = {img['id']: img for img in data['images']}
# This line ensures Class ID 1 becomes 0, ID 2 becomes 1, etc.
categories = {cat['id']: i for i, cat in enumerate(data['categories'])}

print(f"Converting {len(data['annotations'])} polygons...")

for ann in data['annotations']:
    image_id = ann['image_id']
    if image_id not in images: continue
    
    img_w = images[image_id]['width']
    img_h = images[image_id]['height']
    img_filename = os.path.splitext(images[image_id]['file_name'])[0]

    if 'segmentation' in ann and len(ann['segmentation']) > 0:
        # COCO polygons are [x1, y1, x2, y2...]
        seg = ann['segmentation'][0]
        normalized_coords = []
        for i in range(0, len(seg), 2):
            # Normalize x and y to be between 0 and 1
            nx = seg[i] / img_w
            ny = seg[i+1] / img_h
            normalized_coords.append(f"{nx:.6f} {ny:.6f}")

        yolo_class = categories[ann['category_id']]
        yolo_line = f"{yolo_class} " + " ".join(normalized_coords) + "\n"

        # 'a' means append, so multiple fruits in one image all get saved
        with open(os.path.join(output_folder, f"{img_filename}.txt"), 'a') as f_txt:
            f_txt.write(yolo_line)

print(f"✅ Success! Your .txt files are in '{output_folder}'.")