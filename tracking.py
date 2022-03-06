from email.mime import image
import numpy as np
import cv2
import math

class tracking:
        def __init__(self, values):
                self.colorL = np.array([values[0], values[1], values[2]])
                self.colorU = np.array([values[3], values[4], values[5]])
                self.fov_x = 0
                self.fov_y = 0
                self.zed_mounting_height = 0
                self.ball_radius = 0 
                self.stereo_lens_dist = 0 
                self.focal_length_px = 0
                self.mounting_angle = 0 #angle to ground
                self.res_x = 0
                self.res_y = 0

        def ball_tracking(self, image1, image2, hsv_filter):

                height, width, channel = image1.shape

                try:
                        assert image1.shape == image2.shape and (height is not 0 or width is not 0)
                except:
                        return

                image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
                image1 = cv2.inRange(image1, self.colorL, self.colorU)

                image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
                image2 = cv2.inRange(image2, self.colorL, self.colorU)

                circles1 = cv2.HoughCircles(image1, cv2.HOUGH_GRADIENT, 1, height, param1=0, param2=0, minRadius=10, maxRadius=height)
                circles2 = cv2.HoughCircles(image2, cv2.HOUGH_GRADIENT, 1, height, param1=0, param2=0, minRadius=10, maxRadius=height)

                return this.match(circles1, circles2, height, width)

        def approx_dist(self, x1, y1, x2, y2, img_height, img_width):
                horizontal_angle = x1 / (img_width) * self.fov_x
                vertical_angle = y1 / (img_height) * self.fov_y

                approx_dist = (self.ball_radius - self.zed_mounting_height) / math.tan(vertical_angle + self.mounting_angle) * math.cos(horizontal_angle)
                return approx_dist

        def real_dist(self, x1, x2):
                real_dist = self.stereo_lens_dist * self.focal_length / (math.abs(x2 - x1))
                return real_dist

        def match(self, circles1, circles2, img_height, img_width):
                matches = []
                min_real_dist = 99999
                for circle1 in circles1[0, :]:
                        x1, y1, r1 = circle1[0], circle1[1], circle1[2]
                        for circle2 in circles2[0, :]:
                                x2, y2, r2 = circle1[0], circle1[1], circle1[2]
                                
                                y_offset_tune = 0
                                radius_disparity_tune = 0
                                dist_diff_tune = 0
                                if (math.abs(y1 - y2) > y_offset_tune):
                                        pass
                                if (math.abs(r1 - r2) > radius_disparity_tune):
                                        pass
                                approx_dist = self.approx_dist(self, x1, y1, x2, y2, img_height, img_width)
                                real_dist = self.real_dist(self, x1, x2)
                                if ( math.abs(approx_dist - real_dist) > dist_diff_tune):
                                        pass
                                if(real_dist < min_real_dist):
                                        matches = [(x1, y1), (x2, y2), real_dist]
                x1, y1 = matches[0]
                x2, y2 = matches[1]
                real_dist = matches[2]

                horizontal_angle = ((x1+x2)/2 - self.res_x/2) / self.res_x * self.fov_x
                vertical_angle = (y1 - self.res_y/2)/self.res_y * self.fov_y + self.mounting_angle

                x = real_dist * math.sin(horizontal_angle) * math.cos(vertical_angle)
                y = real_dist * math.sin(horizontal_angle) * math.sin(vertical_angle)

                return x, y