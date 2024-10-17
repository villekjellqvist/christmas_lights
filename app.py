from flask import Flask, jsonify
from flask_cors import CORS
import atexit
from christmas_lights.christmas_lights import LightsRunner

def rgb(r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)
    return f"rgb({r},{g},{b})"

def make_palette(nrpixels: int):
    palette = []
    for i in range(nrpixels):
        palette.append(
            rgb((nrpixels - i) * 255 / nrpixels, i * 50 / nrpixels, i * 255 / nrpixels)
        )
    return palette
        

palette = make_palette(50)

lightsThread = LightsRunner(palette)
lightsThread.start()

def shutdown():
    lightsThread.stop()
    lightsThread.join()

atexit.register(shutdown)

app = Flask(__name__)
CORS(app)

@app.route("/pixels")
def sendPalette():
    return jsonify(lightsThread.getPalette())

