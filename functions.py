import numpy as np
from VideoStream import VideoStream


def find_port():
    for i in range(-1, 5):
        camera = VideoStream(i)
        if camera.available():
            height, width, _ = camera.read().shape
            print(height, width)
            if height == 720:
                print(i)
                return i
        camera.stop()
    return -1