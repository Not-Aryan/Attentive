import cv2
import flask
from flask import *
from flask_moment import Moment
from datetime import datetime
import threading
from threading import Thread
from time import sleep
import json
import os
from train import trainn
from prepareData import prep
from testImages import test
from flask_pymongo import PyMongo

app = Flask("Attentive")
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/attentive-db"
app.config['SECRET_KEY'] = 'lookataryanman'
moment = Moment(app)

mongo = PyMongo(app)

vc=cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

imgOk = False
trainOk = False

@app.route('/', methods=['GET', 'POST']) 
def student():
    return render_template('start.html')

@app.route('/train', methods=['GET', 'POST']) 
def train():
    return render_template('train.html')
         


@app.route('/teacher', methods=['GET', 'POST']) 
def teacher():
    if request.method == "GET":
        print("HERE")
        return render_template('reports.html')
    elif request.method == "POST":
        rf = request.form
        for x in rf.keys():
            data_dic = json.loads(x)

        print(data_dic['class'])
        doc = {'class': data_dic['class'], 'assign': data_dic['assign']}
        found = mongo.db.studentInfo.find(doc)
        for x in found:
            stufff = x
            del stufff['_id']
        resp = jsonify(stufff)
        resp.headers['Access-Control-Allow-Origin']='*'
        return resp

def generateData(name, ty):
    global trainOk
    if not os.path.exists('static/datasets/' + name):
        os.mkdir('static/datasets/' + name)
        os.mkdir('static/datasets/' + name + '/front')
        os.mkdir('static/datasets/' + name + '/turned')
    taken1 = 0
    while trainOk == True:
        rval, frame = vc.read()
        frame = frame[60:660, 240:1040]
        cv2.imwrite('static/datasets/' + name + '/' + ty + '/image'+str(taken1)+'.jpg',frame)
        taken1 = taken1 +1


def ThreadTrain(name, t):
    global tt
    tt = Thread(target=generateData(name, t))
    tt.start()
    return "Processing"

def gen():
   """Video streaming generator function.""" 
   print('Streamer inititalised')
   while True:
        rval, frame = vc.read()
      #   cv2.Flip(frame, flipMode=-1)
        imgs = (853, 480)
        frame = cv2.resize(frame, imgs)
        byteArray = cv2.imencode('t.jpg', cv2.flip(frame,1))[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + byteArray + b'\r\n')



@app.route('/video_feed')
def video_feed():
   # cv.Flip(frame, flipMode=-1) 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/starttrain', methods=['POST'])
def starttrain():
    global trainOk
    trainOk = True
    rf = request.form
    for x in rf.keys():
        data_dic = json.loads(x)
    name = data_dic['name'].replace(" ", "-")
    t = data_dic['type']
    ThreadTrain(name, t)
    resp = Response("Application Started")
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp



@app.route('/stoptrain', methods=['POST'])
def stoptrain():
    rf = request.form
    for x in rf.keys():
        dd = json.loads(x)
    global trainOk
    trainOk = False
    name = dd['name'].replace(" ", "-")
    if (dd['o'] == 'stop'):
        things = prep(name)
        trainn(things[0], things[1], name)
        print("DONEBLUE")
    resp = Response("Application Stopped")
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp

# @app.route('/MLstart', methods=['POST'])
# def mlstart():
#     rf = request.form
#     for x in rf.keys():
#         data_dic = json.loads(x)
#     name = data_dic['name'].replace(" ", "-")
#     things = prep(name)
#     print(things)
#     resp = Response("Application Stopped")
#     resp.headers['Access-Control-Allow-Origin']='*'
#     return resp

#--------------------------------------------------------------------------------

def takePic(name):
    global imgOk
    taken = 0
    if not os.path.exists('static/images/students/' + name):
            os.mkdir('static/images/students/' + name)
    while imgOk == True:
        rval, frame = vc.read()
        # savePath = 'images/'
        taken = taken +1
        frame = frame[60:660, 240:1040]
        date = datetime.now()
        date = date.strftime("%b %d %Y %I:%M:%S")
        date = str(date)
        date = date.replace(" ", "-")
        date = date.replace(":", "-")
        cv2.imwrite('static/images/students/' + name + '/' +date+'.jpg',frame)
        sleep(1)
        # session['image'] = 'static/images/image.jpg'

def Start(name):
    t = Thread(target=takePic(name))
    t.start()
    return "Processing"


@app.route('/startimg', methods=['POST']) 
def startimg():
    global imgOk
    imgOk = True
    rf = request.form
    for x in rf.keys():
        dd = json.loads(x)
    name = dd['name'].replace(" ", "-")
    print(dd['class'])
    print(dd['assign'])
    Start(name)
    resp = Response("Application Stopped")
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp

@app.route('/stopimg', methods=['POST']) 
def stopimg():
    global imgOk
    imgOk = False
    rf = request.form
    for x in rf.keys():
        dd = json.loads(x)
    name = dd['name'].replace(" ", "-")
    info = test(name)
    doc = {}
    doc['times-turned'] = info[0]
    doc['times-turned-num'] = len(info[0])
    doc['attenspan'] = info[2]
    doc['name'] = name
    doc['class'] = dd['class']
    doc['assign'] = dd['assign']
    mongo.db.studentInfo.insert_one(doc)
    print(info)
    resp = Response("Application Stopped")
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp

if __name__ == '__main__':
   app.run(debug=True, port=8000)

