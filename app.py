import streamlit as st
import supervision as sv
import threading

from model.estimator import CrowdDensityEstimation
from utils.camera_utils import initialize_camera
from utils.visualization import build_payload, post_request


def send_data_in_background(payload):
    threading.Thread(
        target=post_request,
        args=(
            payload,
        )
    ).start()
    
def main():
    st.title("Crowd Density Estimation")
    st.write("This application estimates the density of a crowd in a video stream.")
    
    st.sidebar.title("Settings")
    conf_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5)
    
    
    estimator = CrowdDensityEstimation(
        model_path="./model/yolo11n.pt",
        conf_threshold=conf_threshold,
    )
    
    dot_annotator = sv.DotAnnotator()
    
    st.header("Video Stream 🎬")
    cap = initialize_camera()
    
    frame_placeholder = st.empty()
    
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        density_level = st.empty()
    with col2:
        density_value = st.empty()
    with col3:
        person_count = st.empty()
        
    

    
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video.")
            break
        
        processed_frame, density_info, results = estimator.process_frame(frame)
        
        detections = sv.Detections.from_ultralytics(results[0]) if results and len(results) > 0 else sv.Detections()
        dot_annotator.annotate(scene=frame, detections=detections)
        
        frame_placeholder.image(processed_frame, channels="BGR", use_container_width=True)
        
        density_level_val = 0
        
        if density_info[1] == "Low":
            density_level_val = 1
        elif density_info[1] == "Medium":
            density_level_val = 2
        elif density_info[1] == "High":
            density_level_val = 3
        elif density_info[1] == "Very High":
            density_level_val = 4
        else:
            density_level_val = 0
        
        payload = build_payload(
            variable_1=f"{density_info[0]:.2f}",
            variable_2=density_level_val,
            variable_3=density_info[2],
        )
        
        send_data_in_background(payload)
        
        density_value.metric("Density Value (persons/m²)", f"{density_info[0]:.2f}", border=True)
        density_level.metric("Density Level", density_info[1], border=True)
        person_count.metric("Person Count", density_info[2], border=True)

    cap.release()
    

if __name__ == "__main__":
    main()