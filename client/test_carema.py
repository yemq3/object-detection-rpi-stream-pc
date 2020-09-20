import numpy as np
import cv2
import time

FRAME_RATE = 30

cap = cv2.VideoCapture(0)
assert cap.isOpened()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, FRAME_RATE)

his = []
prev = time.time()
while True:
    rval, image = cap.read()
    if not rval:
        break

    # _, img_encoded = cv2.imencode('.jpg', image)


    # result_img = plot_boxes_cv2(image, boxes)
    # cv2.imshow('res', image)

    now = time.time()
    his.append(now - prev)
    prev = now

    print("fps:", 1 / (sum(his[-5:])/len(his[-5:])))
    
    # key = cv2.waitKey(1)
    # if key == 27: # exit on ESC
    #     break


cap.release()
cv2.destroyAllWindows()