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
                imageT = cv2.erode(imageT, None, iterations=1)
                imageT = cv2.dilate(imageT, None, iterations=1)
                imageT = cv2.bilateralFilter(imageT, 5, 175, 175)
                cnts = cv2.findContours(imageT.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                if len(cnts) > 0:
                        c = max(cnts, key=cv2.contourArea)
                        ((cx, cy), r) = cv2.minEnclosingCircle(c)

                return (cx, cy), r, imageT

        def update(self, values):
                self.colorL = np.array([values[0], values[1], values[2]])
                self.colorU = np.array([values[3], values[4], values[5]])

        def crop(self, image, pos, r):
                height, width, _ = image.shape
                scalar = 25

                x1 = int(pos[0] - r - scalar)
                x2 = int(pos[0] + r + scalar)
                y1 = int(pos[1] - r - scalar)
                y2 = int(pos[1] + r + scalar)

                if x1 < 0: x1 = 0
                if x2 > width: x2 = width
                if y1 < 0: y1 = 0
                if y2 > height: y2 = height

                imageT = image[y1: y2,x1: x2]

                return imageT

        def find_circle(self, image, r, p1, p2):
                height, width, _ = image.shape
                if height == 0 or width == 0: return False

                scalar = 25

                lower_r = int(r - scalar)
                upper_r = int(r + scalar)
                if lower_r <= 0: lower_r = 0

                imageT = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                imageT = cv2.medianBlur(imageT, 5)

                circles = cv2.HoughCircles(imageT, cv2.HOUGH_GRADIENT, 1, height / 1, param1=p1, param2=p2, minRadius=lower_r, maxRadius=upper_r)
                if circles is not None: return True
                else: return False

