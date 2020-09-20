from flask import Flask
from flask_socketio import SocketIO
from engineio.payload import Payload

app = Flask(__name__, template_folder="../templates")
app.config['SECRET_KEY'] = "b'sk?\x83J\x9bh~hid\x0e\x80\x95\xdc*\x04\"\x9c\xe5\x8ey\xdc\xa9'"
Payload.max_decode_packets = 500 # see https://github.com/miguelgrinberg/python-engineio/issues/142
socketio = SocketIO(app)


from app import views

from app.yolov4 import *




