import os

folder = "images" # The folder where your 240 images are
for filename in os.listdir(folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        new_name = filename.replace(" ", "_").lower()
        os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
print("Done! All images are now lowercase with underscores.")