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

        cv2.rectangle(im0, (0, 0), (350, 150), (0, 0, 0), -1)
        cv2.putText(im0, f'Density Level: {density_level}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(im0, f'Person Count: {person_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(im0, f'Density Value: {density_value:.2f}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
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