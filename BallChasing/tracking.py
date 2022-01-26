import cv2
import numpy as np
import math

class tracking:
        def __init__(self, values, parameters):
                self.colorL = np.array([values[0], values[1], values[2]])
                self.colorU = np.array([values[3], values[4], values[5]])

                self.params = cv2.SimpleBlobDetector_Params()
                self.params.minThreshold = 0;
                self.params.maxThreshold = 100;
                self.params.filterByArea = True
                self.params.minArea = 1000
                self.params.maxArea = 1000000
                self.params.filterByCircularity = True
                self.params.minCircularity = 0.3 #parameters[0]
                self.params.filterByConvexity = True
                self.params.minConvexity = 0.3 #parameters[1]
                self.params.filterByInertia = True
                self.params.minInertiaRatio = 0.3 #parameters[2]

                self.detector = cv2.SimpleBlobDetector_create(self.params)
        def ball(self, image):
                cx = 0
                cy = 0
                r = 0

                imageT = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                imageT = cv2.inRange(imageT, self.colorL, self.colorU)
                imageT = cv2.erode(imageT, None, iterations=2)
                imageT = cv2.dilate(imageT, None, iterations=2)
                reverse_imageT = 255 - imageT

                keypoints = self.detector.detect(reverse_imageT)
                if len(keypoints) != 0: 
                        cx = keypoints[0].pt[0]
                        cy = keypoints[0].pt[1]
                        r =  keypoints[0].size / 2

                return (cx, cy), r, imageT

        def update(self, values, parameters):
                self.colorL = np.array([values[0], values[1], values[2]])
                self.colorU = np.array([values[3], values[4], values[5]])
                
                self.params.minCircularity = parameters[0]
                self.params.minConvexity = parameters[1]
                self.params.minInertiaRatio = parameters[2]
                self.detector = cv2.SimpleBlobDetector_create(self.params)

