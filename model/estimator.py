import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
from typing import List, Tuple, Union

class CrowdDensityEstimation:
    def __init__(self, model_path: str = './model/yolo11n.pt', conf_threshold: float = 0.3):
        """
        Initializes the crowd density estimation model.
        
        Args:
            model_path (str): Path to the YOLO model file.
            conf_threshold (float): Confidence threshold for detections.
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.track_history = defaultdict(list)
        self.density_levels = {
            'Low': (0, 0.2),
            'Medium': (0.2, 0.5),
            'High': (0.5, 0.8),
            'Very High': (0.8, float('inf'))
        }

    def extract_tracks(self, im0: np.ndarray) -> List:
        """
        Extracts tracking results from the YOLO model.
        
        Args:
            im0 (numpy.ndarray): The input image/frame.
        
        Returns:
            list: The tracking results from the model.
        """
        return self.model.track(im0, persist=True, conf=self.conf_threshold, classes=[0])

    def calculate_density(self, results: List, frame_area: int) -> Tuple[float, str, int]:
        """
        Calculates the density of people in the frame.
        
        Args:
            results (list): The tracking results from the model.
            frame_area (int): The area of the frame in pixels.
        
        Returns:
            tuple: A tuple containing the density value, density level, and person count.
        """
        if not results or len(results) == 0:
            return 0, 'Low', 0

        person_count = len(results[0].boxes)
        density_value = person_count / frame_area * 10000  # Convert to persons/m²

        for level, (min_val, max_val) in self.density_levels.items():
            if min_val <= density_value < max_val:
                return density_value, level, person_count

        return density_value, 'Low', person_count

    def display_output(self, im0: np.ndarray, density_info: Tuple[float, str, int]) -> None:
        """
        Displays the output on the frame.

        Args:
            im0 (numpy.ndarray): The input image/frame.
            density_info (tuple): A tuple containing the density value, level, and person count.
        """
        density_value, density_level, person_count = density_info

        # Adjust rectangle size and position for smaller frames
        cv2.rectangle(im0, (0, 0), (100, 80), (0, 0, 0), -1)

        # Adjust font size and position for smaller frames
        font_scale = 0.4  # Smaller font size
        thickness = 1     # Thinner text
        color = (0, 255, 0)  # Green text

        cv2.putText(im0, f'Density: {density_level}', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        cv2.putText(im0, f'Count: {person_count}', (5, 40), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        cv2.putText(im0, f'Value: {density_value:.2f}', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

        # Display the frame
        cv2.imshow('Crowd Density Estimation', im0)

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Tuple[float, str, int], List]:
        """
        Processes a single frame to estimate crowd density.
        
        Args:
            frame (numpy.ndarray): The input video frame.
        
        Returns:
            tuple: A tuple containing the processed frame, density information, and detection results.
        """
        results = self.extract_tracks(frame)
        frame_area = frame.shape[0] * frame.shape[1]
        density_info = self.calculate_density(results, frame_area)
        return frame, density_info, results