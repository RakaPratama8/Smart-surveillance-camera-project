import cv2
import model.model_config as model
import supervision as sv

URL = ("http://192.168.100.130")

def main():
    
    cap = cv2.VideoCapture(0)
    
    yolo_model = model.load_model("./model/yolo11n.pt")
    
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return
    
    tracker = sv.ByteTrack()
    
    box_annotator = sv.BoundingBoxAnnotator()
    
    label_annotator = sv.LabelAnnotator(
        text_position=sv.Position.TOP_LEFT,
        text_color=sv.Color.BLACK,
    )
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        results = yolo_model(frame)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = tracker.update_with_detections(detections)
        
        labels = [
            f"{tracker_id} {results.names[class_id]} {confidence:.2f}"
            for class_id, tracker_id, confidence
            in zip(detections.class_id, detections.tracker_id, detections.confidence)
        ]
        
        frame = label_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )
        
        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
        )
        
        cv2.imshow("YOLOv8 Detection", frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
if __name__ == "__main__":
    main()