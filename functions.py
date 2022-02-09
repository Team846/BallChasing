import numpy as np
from VideoStream import VideoStream


def find_port():
    for i in range(0, 4):
        camera = VideoStream(i).start()
        if camera.available():
            if len(camera.read()) == 376:
                return i
        camera.stop()
    return -1