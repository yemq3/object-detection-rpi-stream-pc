import cv2
import numpy as np
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

cap = cv2.VideoCapture(0)
assert cap.isOpened()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

def encrypt(data, password):
    cipher = AES.new(password, AES.MODE_EAX)
    data = cipher.encrypt(data)
    return (data)
key = get_random_bytes(16)
while True:
    rval, image = cap.read()
    if not rval:
        break
    
    start = time.time()
    _, img_encoded = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 95])
    finish = time.time()
    print(finish-start)

    start = time.time()
    encrypt_data = encrypt(img_encoded.tostring(), key)
    finish = time.time()
    # print(finish-start)
    # print(len(encrypt_data))