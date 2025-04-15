import cv2
from model.estimator import CrowdDensityEstimation
import supervision as sv

def main():
    estimator = CrowdDensityEstimation()
    
    dot_annotator = sv.DotAnnotator()
    
    cap = cv2.VideoCapture(0)
    
    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # out = cv2.VideoWriter('crowd-density-estimation.mp4', 
    #                     fourcc, fps, (frame_width, frame_height))
    
    
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame, density_info, results = estimator.process_frame(frame)
        
        detections = sv.Detections.from_ultralytics(results[0]) if results and len(results) > 0 else sv.Detections()
        
        dot_annotator.annotate(
            scene=frame,
            detections=detections,
        )
        
        estimator.display_output(processed_frame, density_info)
        # out.write(processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()