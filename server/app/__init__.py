from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="../templates")
app.config['SECRET_KEY'] = "b'sk?\x83J\x9bh~hid\x0e\x80\x95\xdc*\x04\"\x9c\xe5\x8ey\xdc\xa9'"
socketio = SocketIO(app)


from app import views

from app.yolov4 import *




