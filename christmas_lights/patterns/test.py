import numpy as np

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

def update():
    global palette
    palette = np.roll(palette, 1).tolist()
    return palette