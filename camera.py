import cv2
import model.model_config as model

URL = ("http://192.168.100.130")

def main():
    
    cap = cv2.VideoCapture(0)
    
    yolo_model = model.load_model("./model/yolo11n.pt")
    
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        result = yolo_model(frame)

        cv2.imshow('Camera Feed', frame)
        break
        
        # if cv2.waitKey(30) & 0xFF == ord('q'):
        #     break
    
    
if __name__ == "__main__":
    main()