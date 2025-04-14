import cv2
import requests

URL = ("http://192.168.100.130")

# def set_resolution(url: str, index: int=1, verbose: bool=False):
#     try:
#         if verbose:
#             resolutions = "10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)"
            
#             print("available resolutions\n{}".format(resolutions))

#         if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
#             requests.get(url + "/control?var=framesize&val={}".format(index))
#         else:
#             print("Wrong index")
#     except:
#         print("SET_RESOLUTION: something went wrong")



def main():
    # set_resolution(URL, 8)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow('Camera Feed', frame)
        
        print(frame.shape)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    
if __name__ == "__main__":
    main()