import numpy as np
from flask import Flask, Response, render_template, request
#from networktables import NetworkTables
from VideoStream import VideoStream
from tracking import tracking
from drawer import drawer
from calculations import *
from functions import *
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

            imageR = cv2.flip(imageR, 0)
            imageL = cv2.flip(imageL, 0)

            posR, rR, imageRT = track.ball(imageR)
            posL, rL, imageLT = track.ball(imageL)

            depth = find_distance(imageRT, imageLT, posR, posL)
            angle = -find_angle(90, height, width/2, posR, posL)

            #table.putNumber('distance_to_ball', depth)
            #table.putNumber('angle_to_ball', angle)
            
            display_image = imageRT

            if posR != (0,0) and rR!= 0: 
                is_ball = track.find_circle(track.crop(imageR, posR, rR), rR, 50,30)
                if is_ball == True: display_image = draw.dot(display_image, posR, 5)
                else: depth = angle = 0

            lowerColor = np.full((50, 50, 3), (hsv_values[0], hsv_values[1], hsv_values[2]), dtype=np.float32)
            lowerColor = cv2.cvtColor(lowerColor, cv2.COLOR_HSV2BGR)
            upperColor = np.full((50, 50, 3), (hsv_values[3], hsv_values[4], hsv_values[5]), dtype=np.float32)
            upperColor = cv2.cvtColor(upperColor, cv2.COLOR_HSV2BGR)
            disp_img = np.full((376, 672, 3), (0, 0, 0))
            for i in range(len(display_image)):
                for j in range(len(display_image[i])):
                    disp_img[i][j][:] = display_image[i][j]
            disp_img[0:lowerColor.shape[0], 0:lowerColor.shape[1]] = lowerColor
            disp_img[0:upperColor.shape[0], 50:50+upperColor.shape[1]] = upperColor

            #disp_img = cv2.resize(disp_img, (int(1344/4), int(376/2)))

            yield (b'--frame\r\n' 
                b'Content-type: text/plain\r\n\r\n' + cv2.imencode('.jpg', disp_img)[1].tostring() + b'\r\n')

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



