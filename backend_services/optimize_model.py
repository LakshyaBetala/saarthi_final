from ultralytics import YOLO
import os

def export_to_onnx():
    #if model path found in current directory, use it;
    model_path = "yolov8n.pt"
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' not found in the current directory.")
    
    
    print(f"Loading model from {model_path}...")
    model = YOLO(model_path)
    
    print("Exporting model to ONNX format...")
    
    success =model.export(format="onnx",dynamic=True)
    
    if success:
        print("Model successfully exported to ONNX format as 'yolov8n.onnx'.")  
    else:
        print("Failed to export the model to ONNX format.")
        
if __name__ == "__main__":
    export_to_onnx()