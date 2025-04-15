import cv2
from model.estimator import CrowdDensityEstimation
from utils.camera_utils import initialize_camera, process_video_frame
import supervision as sv

def main():
    estimator = CrowdDensityEstimation()
    dot_annotator = sv.DotAnnotator()
    cap = initialize_camera()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        process_video_frame(estimator, dot_annotator, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()