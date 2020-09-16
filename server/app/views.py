import requests
from app import *
from flask import request
import numpy as np
import cv2
from app.yolov4 import *
from PIL import Image
import json
from flask_socketio import emit
import time

@app.route('/')
def index():
    return "Hello"

@socketio.on("image")
def hello(message):
    nparr = np.fromstring(message["image"], np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    sized = cv2.resize(img, (darknet.width, darknet.height))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)
    
    boxes = do_detect(darknet, sized, 0.4, 0.6, False)
    boxes = np.array(boxes[0]).tolist()

    for i in range(len(boxes)):
        boxes[i][6] = class_names[int(boxes[i][6])]
    
    response = {
        'frameid': message["frameid"],
        'boxes' : json.dumps(boxes)
    }

    emit('response', response)

@app.route('/api/test', methods=['POST'])
def test():
    nparr = np.fromstring(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    sized = cv2.resize(img, (darknet.width, darknet.height))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)
    boxes = do_detect(darknet, sized, 0.4, 0.6, False)
    boxes = np.array(boxes[0]).tolist()

    for i in range(len(boxes)):
        boxes[i][6] = class_names[int(boxes[i][6])]
    
    response = {
        'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0]),
        'boxes' : json.dumps(boxes)
    }

    return response

