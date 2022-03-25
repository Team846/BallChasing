from VideoStream import VideoStream
from tracking import tracking
from drawer import drawer
from calculations import *
from functions import *
import cv2
import socket
import sys
import time

depth = angle = 0
#todo shohuldn't crash when no ball is present, clean up all of it, and add a flag for reading a camera stream vs video
hsv_values = [95, 130, 38, 116, 255, 255]

#red
# hsv_values = [0, 200, 63, 21, 255, 255]

track = tracking(hsv_values)
draw = drawer()

localIP = ""
localPort = 8468
bufferSize = 64

roboRIOIP = "10.8.46.2"
roboRIOPort = 9719

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))
print(f"UDP server running on port {localPort}")

def nothing(x):
    pass

def threshold():
    vidcap = cv2.VideoCapture('zed1.mov')
    ret, image = vidcap.read()
    cv2.namedWindow('image')

    # Create trackbars for color change
    # Hue is from 0-179 for Opencv
    cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    # Initialize HSV min/max values
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    while(1):
        # Get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')
        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')

        # Set minimum and maximum HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Convert to HSV format and color threshold
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)

        # Print if there is a change in HSV value
        if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display result image
        cv2.imshow('image', result)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
def main():
    global angle, depth

    while find_port() == -1: pass
    camera = VideoStream(find_port()).start()

    # vidcap = cv2.VideoCapture('zed2.mov')
    i = 0
    # output = cv2.VideoWriter('vid.avi', cv2.VideoWriter_fourcc(*'MJPG'), 60, (640, 360), 0)
    # output2 = cv2.VideoWriter('canny.avi', cv2.VideoWriter_fourcc(*'MJPG'), 60, (640, 360), 0)

    success = True
    while success:
        success, img = camera.read()
        # print(img.shape)
        # img = camera.read()
        start = time.time()
        try:
            img1, img2, x, y, z, canny = track.ball_tracking(img[0:360, 0:640], img[0:360, 640:], 1)
            # output.write(img2)
            # output2.write(canny)
        except:
            pass
        end = time.time()

        # print("flsdkjf")
        if camera.available():
            img1, img2, matches, x, y = track.ball_tracking(img[0:360, 0:640], img[0:360, 640:], i)
            UDPServerSocket.sendto(bytes([x, y]), (roboRIOIP, roboRIOPort))
main()
