import cv2
import numpy as np

class drawer():
    def __init__(self):
        return

    def dot(self, image, location, radius):
        image = cv2.circle(image, (int(location[0]),int(location[1])), radius, (0,0,255), -1)
        return image

    def text(self, image, location, text):
        image = cv2.putText(image, str(text), (int(location[0]),int(location[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, 2)
        return image

    def circle(self, image, location, radius):
        image = cv2.circle(image, (int(location[0]),int(location[1])), radius, (0,0,255), radius)
        return image

    def line(self, image, location, location2, thickness):
        image = cv2.line(image, (int(location[0]),int(location[1])), (int(location2[0]),int(location2[1])), (0,0,255), thickness) 
        return image

    def triangle(self, image, location, location2, location3):
        triangle = np.array( [location, location2, location3])
        image = cv2.drawContours(image, [triangle], 0, (0,0,255), -1)
        return image