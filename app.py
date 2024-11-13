from flask import Flask, jsonify, request
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
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://lightspi.local")

@app.route("/getSettings")
def getSettings():
    return jsonify(lightsThread.settings)

@app.route("/setSettings", methods=["POST"])
def setSettings():
    data = request.get_json()
    lightsThread.settings = data
    return "Settings updated"


@app.route("/setPattern", methods=["POST"])
def setScript():
    si = lightsThread.scriptImporter
    data = request.get_json()
    si.currentScriptIndex = data["scriptnr"]
    return "setScript Successfull"

@app.route("/getPatterns")
def sendPalette():
    si = lightsThread.scriptImporter
    running = [True if i==si.currentScriptIndex else False for i in range(len(si.scripts))]
    ret = jsonify({"scripts":si.scripts, "running":running})
    return ret

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data['data'])

@socketio.on("getPixels")
def sendPixels():
    emit("pixels",lightsThread.getPixels(), json=True)

if __name__ == '__main__':
    socketio.run(app)

