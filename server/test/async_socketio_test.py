import socketio
import asyncio
import cv2
import json
import numpy as np
import queue

q = queue()

url = ""

sio = socketio.AsyncClient()
await sio.connect(url)
print("sid:", sio.sid)

@sio.event
async def message(data):
    pass

async def GetImageAndEncode():
    cap = cv2.VideoCapture(0)
    assert cap.isOpened()

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 24)

    while True:
        rval, image = cap.read()
        if rval:
            _, img_encoded = cv2.imencode('.jpg', image)
            q.put(img_encoded.tostring())
            await SendImage()
        else:
            break

async def SendImage():
    