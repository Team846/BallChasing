from flask import Flask, Response, render_template, request
from datatransfer import datatransfer
from VideoStream import VideoStream
from tracking import tracking
from drawer import drawer
from calculations import *
from functions import *
import keyboard
import cv2
import time

app = Flask(__name__)

depth = angle = 0

hsv_values = [0, 0, 0, 255, 255, 255]
parameter_values = [0, 0, 0]

#table = datatransfer(ip="10.8.46.108", table_name="FunkyDashboard")
track = tracking(hsv_values, parameter_values)
draw = drawer()

def code():
    global angle, depth

    while find_port() == -1: pass
    camera = VideoStream(find_port()).start()

    hsv_index = parameter_index = 0

    while True:
        image = camera.read()

        track.update(hsv_values, parameter_values)

        if camera.available():
            height, width, _ = image.shape

            imageR = image[:, :width//2]
            imageL = image[:, width//2:]

            posR, _, imageRT = track.ball(imageR)
            posL, _, imageLT = track.ball(imageL)

            depth = find_distance(imageRT, imageLT, posR, posL)
            angle = find_angle(90, height, width, posR, posL)
            
            #table.send('distance_to_ball', depth)
            #table.send('angle_to_ball', angle)

            display_image = draw.circle(imageRT, posR, 5)
            display_image = cv2.resize(imageRT, (int(640*0.9), int(360*0.9)))

            yield (b'--frame\r\n' 
                b'Content-type: text/plain\r\n\r\n' + cv2.imencode('.jpg', display_image)[1].tostring() + b'\r\n')

        if keyboard.is_pressed("enter"): pass
        elif keyboard.is_pressed("1"): hsv_index = 0
        elif keyboard.is_pressed("2"): hsv_index = 1
        elif keyboard.is_pressed("3"): hsv_index = 2
        elif keyboard.is_pressed("4"): hsv_index = 3
        elif keyboard.is_pressed("5"): hsv_index = 4
        elif keyboard.is_pressed("6"): hsv_index = 5
        elif keyboard.is_pressed("7"): parameter_index = 0
        elif keyboard.is_pressed("8"): parameter_index = 1
        elif keyboard.is_pressed("9"): parameter_index = 2
        elif keyboard.is_pressed("up arrow"): 
            hsv_values[hsv_index] = hsv_values[hsv_index] + 1
            track.update(hsv_values, parameter_values)
        elif keyboard.is_pressed("down arrow"):
            hsv_values[hsv_index] = hsv_values[hsv_index] - 1
            track.update(hsv_values, parameter_values)
        elif keyboard.is_pressed("w"):
            parameter_values[parameter_index] = parameter_values[parameter_index] + 0.05
            if parameter_values[parameter_index] > 1:
                parameter_values[parameter_index] = 1
            track.update(hsv_values, parameter_values)
        elif keyboard.is_pressed("s"):
            parameter_values[parameter_index] = parameter_values[parameter_index] - 0.05
            if parameter_values[parameter_index] < 0:
                parameter_values[parameter_index] = 0
            track.update(hsv_values, parameter_values)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        values = [request.form.get("hsv_value_1"), request.form.get("hsv_value_2"), request.form.get("hsv_value_3"), request.form.get("hsv_value_4"), request.form.get("hsv_value_5"), request.form.get("hsv_value_6"), request.form.get("circularity_value"), request.form.get("convexity_value"), request.form.get("intertia_value")]
        for i in range(len(values)):
            if values[i] != None and i<6:
                hsv_values[i] = int(values[i])
            elif values[i] != None and i>=6:
                parameter_values[i-6] = float(values[i])
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

@app.route('/current_param')
def current_param(): 
    return str(parameter_values)

if __name__ == '__main__':
   app.run('0.0.0.0', debug = True, port = 5802)



