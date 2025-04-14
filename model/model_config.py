from ultralytics import YOLO

def load_model(model_path: str):
    """
    Load the YOLO model from the specified path.
    
    Args:
        model_path (str): Path to the YOLO model file.
    
    Returns:
        YOLO: Loaded YOLO model.
    """
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None