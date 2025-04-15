import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict

class CrowdDensityEstimation:
    def __init__(self, model_path='./model/yolo11n.pt', conf_threshold=0.3):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.track_history = defaultdict(lambda: [])
        self.density_levels = {
            'Low': (0, 0.2), # 0-0.2 persons/m²
            'Medium': (0.2, 0.5), # 0.2-0.5 persons/m²
            'High': (0.5, 0.8), # 0.5-0.8 persons/m²
            'Very High': (0.8, float('inf')) # >0.8 persons/m²
        }

    def extract_tracks(self, im0):
        """
        Extracts tracking results from the model.
        Args:
            im0 (numpy.ndarray): The input image/frame.
        Returns:
            list: The tracking results from the model.
        """
        results = self.model.track(
            im0, persist=True, 
            conf=self.conf_threshold, 
            classes=[0],
        )
        return results

    def calculate_density(self, results, frame_area):
        """
        Calculate the density of people in the frame.
        Args:
            results (list): The tracking results from the model.
            frame_area (int): The area of the frame in pixels.
        Returns:
            tuple: A tuple containing the density value, density level, and person count.
        """
        
        if not results or len(results) == 0:
            return 0, 'Low', 0

        person_count = len(results[0].boxes)
        density_value = person_count / frame_area * 10000  

        density_level = 'Low'
        for level, (min_val, max_val) in self.density_levels.items():
            if min_val <= density_value < max_val:
                density_level = level
                break
                
        return density_value, density_level, person_count
    
    def display_output(self, im0, density_info):
        """
        Displays the output on the frame.
        Args:
            im0 (numpy.ndarray): The input image/frame.
            density_info (tuple): A tuple containing the density value, level, and person count.
        """
        density_value, density_level, person_count = density_info

        cv2.rectangle(im0, (0, 0), (350, 150), (0, 0, 0), -1)
        
        cv2.putText(im0, f'Density Level: {density_level}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(im0, f'Person Count: {person_count}', (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(im0, f'Density Value: {density_value:.2f}', (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow('Crowd Density Estimation', im0)
    
    def process_frame(self, frame):
        """
        Processes a single frame to estimate crowd density.

        Args:
            frame (numpy.ndarray): The input video frame.

        Returns:
            tuple: A tuple containing the processed frame (numpy.ndarray)
            and density information (tuple with density value, level, and person count).
        """
        results = self.extract_tracks(frame)

        frame_area = frame.shape[0] * frame.shape[1]

        density_info = self.calculate_density(results, frame_area)

        self.display_output(frame, density_info)

        return frame, density_info, results