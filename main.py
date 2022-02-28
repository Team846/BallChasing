from VideoStream import VideoStream
from tracking import tracking
from drawer import drawer
from calculations import *
from functions import *
import cv2
import socket

depth = angle = 0

hsv_values = [0, 0, 0, 255, 255, 255]

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

    #while find_port() == -1: pass
    camera = VideoStream(find_port()).start()

    hsv_index = 0

    while True:
        image = camera.read()

        track.update(hsv_values)

        if camera.available():
            height, width, _ = image.shape

            imageR = image[:, :width//2]
            imageL = image[:, width//2:]

            imageR = cv2.flip(imageR, 0)
            imageL = cv2.flip(imageL, 0)

            posR, rR, imageRT = track.ball(imageR)
            posL, rL, imageLT = track.ball(imageL)

            depth = find_distance(imageRT, imageLT, posR, posL)
            angle = -find_angle(90, height, width/2, posR, posL)
            
            display_image = imageRT

            if posR != (0,0) and rR!= 0: 
                is_ball = track.find_circle(track.crop(imageR, posR, rR), rR, 50,30)
                if is_ball == True: display_image = draw.dot(display_image, posR, 5)
                else: depth = angle = 0

            display_image = cv2.resize(display_image, (int(1344/4), int(376/2)))

            data = str("("+depth+","+angle+")").encode("utf-8")

            UDPServerSocket.sendto(data, roboRIOIP)