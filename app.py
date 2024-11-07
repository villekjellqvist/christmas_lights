from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import atexit
from christmas_lights.updateThread import LightsRunner

lightsThread = LightsRunner()
lightsThread.start()

def shutdown():
    lightsThread.stop()
    lightsThread.join()

atexit.register(shutdown)

app = Flask(__name__)
#CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://lightspi.local")

# @app.route("/pixels")
# def sendPalette():
#     return jsonify(lightsThread.getPixels())

@socketio.on('message')
def handle_message(data):
    print(data)
    print('received message: ' + data['data'])

@socketio.on("getPixels")
def sendPixels():
    #print(lightsThread.getPixels())
    emit("pixels",lightsThread.getPixels(), json=True)

if __name__ == '__main__':
    socketio.run(app)