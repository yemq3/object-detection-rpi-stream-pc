import numpy as np
import cv2
import time
import requests
import json
import sys

cap = cv2.VideoCapture(0)
assert cap.isOpened()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 24)

url = "http://192.168.199.180/api/test"

content_type = 'image/jpeg'
headers = {'content-type': content_type}

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

while True:
    rval, image = cap.read()
    if rval==True:
        start = time.time()
        _, img_encoded = cv2.imencode('.jpg', image)
        finish = time.time()
        print("encode:%f" % (finish-start))
        print(sys.getsizeof(img_encoded.tostring()))
        
        start = time.time()
        r = requests.post(url, data=img_encoded.tostring(), headers=headers)
        finish = time.time()
        print("get:%f" % (finish-start))
        
        start = time.time()
        boxes = json.loads(r.json()["boxes"])
        finish = time.time()
        print("decode:%f" % (finish-start))

        result_img = plot_boxes_cv2(image, boxes)
        cv2.imshow('res', result_img)
        # cv2.imshow("Output", image)
        
        key = cv2.waitKey(10)
        if key == 27: # exit on ESC
            break
    elif rval==False:
        break


cap.release()
cv2.destroyAllWindows()