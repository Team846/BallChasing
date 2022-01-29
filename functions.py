import numpy as np
from VideoStream import VideoStream


def find_port():
    for i in range(0, 4):
        camera = VideoStream(i).start()
        if camera.available():
            return i
    return -1