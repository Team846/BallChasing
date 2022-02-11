from flask import Flask, Response, render_template, request
#from networktables import NetworkTables
from VideoStream import VideoStream
from tracking import tracking
from drawer import drawer
from calculations import *
from functions import *
import keyboard
import time
import math
import cv2

app = Flask(__name__)

depth = angle = 0

hsv_values = [0, 0, 0, 255, 255, 255]

#NetworkTables.initialize(server='192.168.0.10')
#table = NetworkTables.getTable('SmartDashboard')

track = tracking(hsv_values)
draw = drawer()

def code():
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

            posR, rR, imageRT = track.ball(imageR)
            posL, rL, imageLT = track.ball(imageL)

            #depth = find_distance(imageRT, imageLT, posR, posL)
            #angle = find_angle(90, height, width/2, posR, posL)

            #true_x = depth*math.sin(angle * math.pi/180)
            #true_y = depth*math.cos(angle * math.pi/180)

            #table.putNumber('distance_to_ball', depth)
            #table.putNumber('angle_to_ball', angle)
            
            display_image = imageR #color
            #display_image = imageRT #mask
            #display_image = cv2.bitwise_and(imageR, imageR, mask= imageRT) #mask + color

            display_image = draw.dot(display_image, posR, 5)
            #display_image = cv2.resize(display_image, (int(1344/2), int(376)))

            if posR != (0,0) and rR!= 0: 
                display_image = track.crop(display_image, posR, rR)
                is_ball = track.find_circle(display_image, rR)
                if is_ball == False: display_image = imageR

            yield (b'--frame\r\n' 
                b'Content-type: text/plain\r\n\r\n' + cv2.imencode('.jpg', display_image)[1].tostring() + b'\r\n')

        if keyboard.is_pressed("enter"): camera.stop()
        elif keyboard.is_pressed("1"): hsv_index = 0
        elif keyboard.is_pressed("2"): hsv_index = 1
        elif keyboard.is_pressed("3"): hsv_index = 2
        elif keyboard.is_pressed("4"): hsv_index = 3
        elif keyboard.is_pressed("5"): hsv_index = 4
        elif keyboard.is_pressed("6"): hsv_index = 5
        elif keyboard.is_pressed("up arrow"): 
            hsv_values[hsv_index] = hsv_values[hsv_index] + 1
            track.update(hsv_values)
        elif keyboard.is_pressed("down arrow"):
            hsv_values[hsv_index] = hsv_values[hsv_index] - 1
            track.update(hsv_values)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        values = [request.form.get("hsv_value_1"), request.form.get("hsv_value_2"), request.form.get("hsv_value_3"), request.form.get("hsv_value_4"), request.form.get("hsv_value_5"), request.form.get("hsv_value_6")]
        for i in range(len(values)):
            if values[i] != None:
                hsv_values[i] = int(values[i])
        video_feed()
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
   return Response(code(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/current_depth')
def current_depth(): 
    return str(int(depth)) + " inches"

@app.route('/current_angle')
def current_angle(): 
    return str(int(angle)) + " degrees"

@app.route('/current_hsv')
def current_hsv(): 
    return str(hsv_values)

if __name__ == '__main__':
   app.run('0.0.0.0', debug = True, port = 5802)



