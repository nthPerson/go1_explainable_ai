from time import sleep
import cv2

class Snapper:
    def __init__(self):
        self.cam = cv2.VideoCapture("http://146.244.98.19:5000/video_feed")
    def get_frame(self):
            CURRENT_FRAME = "current_frame.jpg"
            ret, frame = self.cam.read()
            cv2.imwrite(CURRENT_FRAME, frame)

if __name__ == "__main__":
    snapper = Snapper()
    while True:
         snapper.get_frame()
         sleep(.001)