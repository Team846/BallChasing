from VideoStream import VideoStream
from tracking import tracking
from drawer import drawer
from calculations import *
from functions import *
import cv2
import socket
import sys

depth = angle = 0

hsv_values = [100, 100, 20, 255, 255, 255]

track = tracking(hsv_values)
draw = drawer()

localIP = ""
localPort = 8468
bufferSize = 4096
roboRIOIP = "10.8.46.2"

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))
print(f"UDP server running on port {localPort}")


def main():
    global angle, depth

    while find_port() == -1: pass
    camera = VideoStream(find_port()).start()

    # vidcap = cv2.VideoCapture('zed1.mov')
    i = 0
    output = cv2.VideoWriter('vid.avi', cv2.VideoWriter_fourcc(*'MJPG'), 60, (640, 360), 0)

    while True:
        # success, img = vidcap.read()
        # print(img.shape)
        img = camera.read()

        # output.write(img1)
        # i+=1
        print("flsdkjf")
        print()
        if camera.available():
            img1, img2, matches, x, y = track.ball_tracking(img[0:360, 0:640], img[0:360, 640:], i)
            UDPServerSocket.sendto(bytearray([int(x), int(y)]), roboRIOIP)

main()
