# modules/vision.py
from ultralytics import YOLO
from .utils import capture_frame
import os

# 1. LOAD THE OPTIMIZED ONNX MODEL
# We check if the ONNX file exists; if not, fallback to .pt (safety first)
model_path = "yolov8n.onnx" if os.path.exists("yolov8n.onnx") else "yolov8n.pt"
print(f"🚀 Loading Vision Model: {model_path} (Optimized)")

# task='detect' is required for ONNX inference
yolo_model = YOLO(model_path, task='detect')

# Indoor objects to detect
indoor_objects = [
    "person", "chair", "table", "sofa", "lamp", "bed", "shelf", "tv", "monitor",
    "laptop", "keyboard", "mouse", "door", "window", "fan", "plant", "cupboard",
    "mirror", "stool", "bookshelf", "microwave", "refrigerator"
]

def detect_objects_and_direction(camera_url):
    frame = capture_frame(camera_url)
    if frame is None:
        return {"error": "Could not capture frame from camera."}

    # Run inference
    results = yolo_model(frame)
    detections = results[0].boxes.data.cpu().numpy()

    objects = []
    frame_width = frame.shape[1]
    left_blocked = False
    right_blocked = False

    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        label = yolo_model.names[int(cls)]

        if label in indoor_objects:
            # 2. FIX THE API RESPONSE FORMAT
            # Frontend expects 'name', not 'label'
            objects.append({
                "name": label,
                "confidence": float(conf)
            })
            
            # Logic for direction
            center_x = (x1 + x2) / 2
            if center_x < frame_width / 2:
                left_blocked = True
            else:
                right_blocked = True

    direction = "Clear path ahead"
    if left_blocked and not right_blocked:
        direction = "Move Right"
    elif right_blocked and not left_blocked:
        direction = "Move Left"
    elif left_blocked and right_blocked:
        direction = "Stop! Path Blocked"

    # 3. RETURN EXACTLY WHAT FRONTEND EXPECTS
    return {
        "objects": objects,
        "direction": direction
    }