from ultralytics import YOLO

def main():
    # Load the segmentation model
    # It will automatically download 'yolo11n-seg.pt' on the first run
    model = YOLO("yolo11n-seg.pt")

    # Start training
    results = model.train(
        data="fruit_config.yaml",  # Points to your yaml file
        epochs=100,                # 100 is good for 121 images
        imgsz=640,                 # Standard YOLO image size
        device="cpu",              # Change to "0" if you have an NVIDIA GPU
        project="fruit_ai",        # Folder name for results
        name="fruit_segmentation", # Specific run name
        save=True
    )

if __name__ == "__main__":
    main()