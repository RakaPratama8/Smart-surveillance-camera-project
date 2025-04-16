import streamlit as st
from model.estimator import CrowdDensityEstimation
from utils.camera_utils import initialize_camera
import supervision as sv
from utils.visualization import build_payload, post_request


def main():
    st.title("Crowd Density Estimation")
    st.write("This application estimates the density of a crowd in a video stream.")
    
    st.sidebar.title("Settings")
    conf_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5)
    
    density_level = st.sidebar.empty()
    person_count = st.sidebar.empty()
    density_value = st.sidebar.empty()
    
    estimator = CrowdDensityEstimation(
        model_path="./model/yolo11n.pt",
        conf_threshold=conf_threshold,
    )
    
    dot_annotator = sv.DotAnnotator()
    
    st.header("Video Stream 🎬")
    cap = initialize_camera()
    
    frame_placeholder = st.empty()
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video.")
            break
        
        processed_frame, density_info, results = estimator.process_frame(frame)
        
        detections = sv.Detections.from_ultralytics(results[0]) if results and len(results) > 0 else sv.Detections()
        dot_annotator.annotate(scene=frame, detections=detections)
        
        frame_placeholder.image(processed_frame, channels="BGR", use_container_width=True)
        
        payload = build_payload(
            variable_1=f"{density_info[0]:.2f}",
            variable_2=density_info[1],
            variable_3=density_info[2],
        )
        
        post_request(payload)
        
        density_value.metric("Density Value (persons/m²)", f"{density_info[0]:.2f}")
        density_level.metric("Density Level", density_info[1])
        person_count.metric("Person Count", density_info[2])

    cap.release()
    

if __name__ == "__main__":
    main()