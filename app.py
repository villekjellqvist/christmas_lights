from flask import Flask, jsonify
from flask_cors import CORS
import atexit
from christmas_lights.christmas_lights import LightsRunner

lightsThread = LightsRunner()
lightsThread.start()

def shutdown():
    lightsThread.stop()
    lightsThread.join()

atexit.register(shutdown)

app = Flask(__name__)
CORS(app)

@app.route("/pixels")
def sendPalette():
    return jsonify(lightsThread.getPixels())

