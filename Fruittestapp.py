import gradio as gr
from ultralytics import YOLO
import PIL.Image as Image
import numpy as np

# 1. Load your model (ensure this path matches your trained file)
# If you moved best.pt to your app folder, just use model = YOLO("best.pt")
model = YOLO("fruit_ai/fruit_segmentation/weights/best.pt")

def predict_fruit(img):
    # Run detection with super low confidence (0.10) to force a guess
    # This ensures that even if the AI is unsure, it will try to label the fruit.
    results = model(img, conf=0.10) 
    
    # --- TERMINAL LOGGING (This prints the 'Values' to your VS Code console) ---
    print("\n--- NEW DETECTION ---")
    if len(results[0].boxes) == 0:
        print("Result: No fruit detected.")
    else:
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            confidence = float(box.conf[0])
            print(f"Detected: {label} | Confidence: {confidence:.2%}")
    # --------------------------------------------------------------------------

    # 2. Draw the 'Values' onto the image
    # We force labels=True and conf=True so you see "FreshApple 85%" on the screen
    res_plotted = results[0].plot(
        conf=True,        # Show the confidence percentage
        labels=True,      # Show the class name (Fresh vs Rotten)
        boxes=True,       # Show the bounding box
        masks=True        # Show the colored polygon area
    )
    
    # 3. Convert BGR (OpenCV format) to RGB (Web format)
    # This ensures your fruit isn't blue/weird colors
    res_rgb = res_plotted[:, :, ::-1]
    
    return Image.fromarray(res_rgb)

# 4. Create the Gradio Interface
interface = gr.Interface(
    fn=predict_fruit,
    inputs=gr.Image(type="numpy", label="Upload Fruit Photo"),
    outputs=gr.Image(type="pil", label="AI Result (Fresh/Rotten Status)"),
    title="🍓 Fruit Quality AI Scanner",
    description="This AI analyzes the shape and texture of fruit to determine if it is Fresh or Rotten. Results will show the class name and confidence score."
)

if __name__ == "__main__":
    # Setting share=True will give you a public link you can open on your phone!
    interface.launch(share=False)