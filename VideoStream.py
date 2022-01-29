from threading import Thread
import numpy as np
import cv2

class VideoStream:
    def __init__(self, src):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        
    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
            
    def read(self):
        return np.copy(self.frame)

    def available(self):
        return self.grabbed
    
    def stop(self):
        self.stopped = True
        self.stream.release()


