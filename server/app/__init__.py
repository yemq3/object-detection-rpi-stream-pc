from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="../templates")
app.config['SECRET_KEY'] = "b'sk?\x83J\x9bh~hid\x0e\x80\x95\xdc*\x04\"\x9c\xe5\x8ey\xdc\xa9'"
socketio = SocketIO(app)


from app import views

from app.yolov4 import *

# from yolov4.demo import detect_cv2
# from yolov4.tool.utils import *
# from yolov4.tool.torch_utils import *
# from yolov4.tool.darknet2pytorch import Darknet
# use_cuda = False


# m = Darknet("../yolov4/cfg/yolov4-tiny.cfg")

# m.print_network()
# m.load_weights("../yolov4/yolov4-tiny.weights")

# if use_cuda:
#     m.cuda()

# num_classes = m.num_classes
# if num_classes == 20:
#     namesfile = '../yolov4/data/voc.names'
# elif num_classes == 80:
#     namesfile = '../yolov4/data/coco.names'
# else:
#     namesfile = '../yolov4/data/x.names'
# class_names = load_class_names(namesfile)


