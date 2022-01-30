import numpy as np
import math
import cv2

def find_distance(image_right, image_left, position_right, position_left):
        baseline = 9
        f_pixel = 6
        alpha = 56.6
        height_right, width_right= image_right.shape
        height_left, width_left = image_left.shape

        if width_right == width_left:
                f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
        else:
                print('Left and right camera frames do not have the same pixel width')

        x_right = position_right[0]
        x_left = position_left[0]
        disparity = x_left-x_right 
        zDepth = (baseline*f_pixel)/disparity

        distance = abs(zDepth)*0.303881-0.43233

        if math.isinf(distance):
                distance = -1

        return distance

def find_angle(fov, height, width, position_right, position_left):
        xr, yr = position_right
        xl, yl = position_left

        return fov/width*((xr+xl)/2-height)