import cv2
import supervision as sv

URL = ""

def initialize_camera():
    """Initializes the camera and returns the VideoCapture object."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Failed to open the camera.")
    return cap

def process_video_frame(estimator, dot_annotator, frame):
    """
    Processes a single video frame, annotates it, and returns the processed frame.
    
    Args:
        estimator (CrowdDensityEstimation): The crowd density estimator.
        dot_annotator (sv.DotAnnotator): The dot annotator for visualizing detections.
        frame (numpy.ndarray): The input video frame.

    Returns:
        numpy.ndarray: The annotated frame.
    """
    processed_frame, density_info, results = estimator.process_frame(frame)
    detections = sv.Detections.from_ultralytics(results[0]) if results and len(results) > 0 else sv.Detections()
    dot_annotator.annotate(scene=frame, detections=detections)
    estimator.display_output(processed_frame, density_info)
    return processed_frame