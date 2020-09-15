import requests
from app import *
from flask import request, render_template
import numpy as np
import cv2
from app.yolov4 import *
from PIL import Image
import json
from flask_socketio import send, emit

@app.route('/')
def index():
    return "Hello"

@socketio.on("test")
def hello():
    return render_template("hello.html")

@app.route('/api/test', methods=['POST'])
def test():
    nparr = np.fromstring(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # img = Image.open(file.stream)
    # img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

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

