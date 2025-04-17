# Crowd Density Estimation with ESP32 and YOLO

This project is a **Crowd Density Estimation System** that uses an ESP32 camera module and a YOLO-based machine learning model to detect and estimate the density of people in a video stream. The system also integrates with **Ubidots** for data visualization and provides a **Streamlit dashboard** for real-time monitoring.

---

## Features

- **Crowd Density Estimation**: Uses a YOLO model to detect people and calculate crowd density.
- **ESP32 Camera Integration**: Streams video from an ESP32 camera module.
- **Real-Time Dashboard**: Displays live video feed and crowd density metrics using Streamlit.
- **Data Visualization**: Sends density data to Ubidots for further analysis and visualization.
- **Customizable Settings**: Adjust detection thresholds and other parameters via the Streamlit interface.

---

## Project Structure
```bash
project/
├── CameraWebServer/ # ESP32 camera firmware
│ ├── app_httpd.cpp # HTTP server implementation for camera
│ ├── camera_index.h # HTML interface for the camera stream
│ ├── camera_pins.h # Pin configuration for the ESP32 camera
│ ├── CameraWebServer.ino # Main Arduino sketch for the ESP32 camera
│ ├── ci.json # CI/CD configuration (if applicable)
│ ├── partitions.csv # Partition table for ESP32 flash memory
│
├── model/ # YOLO model and crowd density estimation logic
│ ├── estimator.py # Crowd density estimation logic
│ ├── yolo11n.pt # Pre-trained YOLO model weights
│
├── utils/ # Utility scripts
│ ├── camera_utils.py # Camera initialization and helper functions
│ ├── visualization.py # Ubidots integration and data handling
│
├── app.py # Streamlit dashboard for real-time monitoring
├── README.md # Project documentation
├── requirements.txt # Python dependencies

```

---

## How It Works

1. **ESP32 Camera**:
   - Streams video to the Python application.
   - Configured using the `CameraWebServer` firmware.

2. **YOLO Model**:
   - Detects people in the video stream.
   - Calculates crowd density based on the number of detected people and the frame area.

3. **Streamlit Dashboard**:
   - Displays the live video feed with annotated detections.
   - Shows real-time metrics such as density level, person count, and density value.

4. **Ubidots Integration**:
   - Sends crowd density data to Ubidots for visualization and analysis.
   - Data includes density value, density level, and person count.