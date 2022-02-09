import numpy as np
import cv2

class tracking:
        def __init__(self, values):
                self.colorL = np.array([values[0], values[1], values[2]])
                self.colorU = np.array([values[3], values[4], values[5]])

        def ball(self, image):
                cx = 0
                cy = 0
                r = 0

                imageT = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                imageT = cv2.inRange(imageT, self.colorL, self.colorU)
                imageT = cv2.erode(imageT, None, iterations=2)
                imageT = cv2.dilate(imageT, None, iterations=2)
                imageT = cv2.bilateralFilter(imageT, 5, 175, 175)
                cnts = cv2.findContours(imageT.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                if len(cnts) > 0:
                        c = max(cnts, key=cv2.contourArea)
                        ((cx, cy), r) = cv2.minEnclosingCircle(c)

                return (cx, cy), r, imageT

        def update(self, values):
                self.colorL = np.array([values[0], values[1], values[2]])
                self.colorU = np.array([values[3], values[4], values[5]])

