import socketio
import cv2
import json
import numpy as np
import time
import heapq

BUFFER_SIZE = 100
FRAME_RATE = 10
CircularBuffer = [None for _ in range(BUFFER_SIZE)]
PriorityQueue = []

url = "http://127.0.0.1"

cap = cv2.VideoCapture(0)
assert cap.isOpened()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, FRAME_RATE)

sio = socketio.Client()
sio.connect(url)
print("sid:", sio.sid)
s = time.time()

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
            # print('%s: %f' % (cls_name, cls_conf))
            img = cv2.putText(img, cls_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.2, rgb, 1)
        img = cv2.rectangle(img, (x1, y1), (x2, y2), rgb, 1)

    return img

his = []
@sio.event
def response(data):
    image, send_time = CircularBuffer[data["frameid"] % BUFFER_SIZE]
    boxes = json.loads(data["boxes"])

    delay = time.time()-send_time
    print(frameid, data["frameid"])
    print("delay:", delay)
    his.append(delay)

    result_img = plot_boxes_cv2(image, boxes)

    print("process fps:", data["frameid"]/(time.time()-s))

    heapq.heappush(PriorityQueue, (data["frameid"], result_img))

    # cv2.imshow('res', result_img)
    # print(sum(his)/len(his))

frameid = 0
prev = time.time()
while True:
    time_elapsed = time.time() - prev
    rval, image = cap.read()
    if not rval:
        break
    if time_elapsed > 1./FRAME_RATE:
        prev = time.time()
        print("send fps:", 1/time_elapsed)

        _, img_encoded = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 50])

        data = {
            "image": img_encoded.tostring(),
            "frameid": frameid,
            "send_time": time.time()
        }

        sio.emit("image", data)

        CircularBuffer[frameid % BUFFER_SIZE] = (image, data["send_time"])
        frameid += 1

        if len(PriorityQueue):
            _, result_img = heapq.heappop(PriorityQueue)
            cv2.imshow('res', result_img)
            cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
