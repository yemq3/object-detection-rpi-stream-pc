import socketio
import cv2
import json
import numpy as np
import time

BUFFER_SIZE = 100
FRAME_RATE = 8
CircularBuffer = [None for _ in range(BUFFER_SIZE)]

url = "http://127.0.0.1"

cap = cv2.VideoCapture(0)
assert cap.isOpened()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, FRAME_RATE)

sio = socketio.Client()
sio.connect(url)
print("sid:", sio.sid)

def plot_boxes_cv2(img, boxes):
    img = np.copy(img)

    width = img.shape[1]
    height = img.shape[0]
    for i in range(len(boxes)):
        box = boxes[i]
        x1 = int(box[0] * width)
        y1 = int(box[1] * height)
        x2 = int(box[2] * width)
        y2 = int(box[3] * height)


        rgb = (255, 0, 0)

        if len(box) == 7:
            cls_conf = box[5]
            cls_name = box[6]
            print('%s: %f' % (cls_name, cls_conf))
            img = cv2.putText(img, cls_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.2, rgb, 1)
        img = cv2.rectangle(img, (x1, y1), (x2, y2), rgb, 1)

    return img


@sio.event
def response(data):
    image, send_time = CircularBuffer[data["frameid"] % BUFFER_SIZE]
    boxes = json.loads(data["boxes"])

    delay = time.time()-send_time
    print("delay:", delay)

    result_img = plot_boxes_cv2(image, boxes)
    cv2.imshow('res', result_img)
    cv2.waitKey(0)


frameid = 0
prev = 0
while True:
    time_elapsed = time.time() - prev
    rval, image = cap.read()
    if not rval:
        break
    if time_elapsed > 1./FRAME_RATE:
        prev = time.time()

        _, img_encoded = cv2.imencode('.jpg', image)

        data = {
            "image": img_encoded.tostring(),
            "frameid": frameid,
            "send_time": time.time()
        }

        sio.emit("image", data)

        CircularBuffer[frameid % BUFFER_SIZE] = (image, data["send_time"])
        frameid += 1

cap.release()
cv2.destroyAllWindows()