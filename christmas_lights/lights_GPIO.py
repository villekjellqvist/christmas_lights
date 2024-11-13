from utils import TimeKeeper
import os
from config import SA_NAME, UPDATETIME, NR_PIXELS, PIDFILE
import time
import board
import neopixel
import numpy as np
import SharedArray as sa
import atexit

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = NR_PIXELS

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
atexit.register(pixels.deinit)
timekeeper = TimeKeeper(UPDATETIME)

for i in range(6):
    try:
        SA = sa.attach(SA_NAME)
        print("GPIO: Attached to shared pixels array")
        break
    except FileNotFoundError:
        if i < 5:
            print(f"GPIO: Shared pixels array not found, retrying in 2 seconds...")
            time.sleep(2)
            continue
        print(f"GPIO: Shared pixels array not found, exiting...")
        exit()

while(True):
    if not os.path.isfile(PIDFILE):
        print("GPIO: Flask server stopped. Exiting...")
        exit()
    timekeeper.wait()
    while np.allclose(SA[0], 0):
        time.sleep(0.01)
    for i,p in enumerate(SA[1:]):
        pixels[i] = np.asarray(p,dtype=int)
    SA[0,:] = 0
    pixels.show()




def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


