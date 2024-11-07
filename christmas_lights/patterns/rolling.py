import numpy as np
from christmas_lights.utils import AbstractPattern

class Pattern(AbstractPattern):
    def start(self):
        for i in range(self.nrpixels):
            self.pixels[i] = ((self.nrpixels - i) * 255 / self.nrpixels, i * 50 / self.nrpixels, i * 255 / self.nrpixels)

    def update(self):
        self.pixels = np.roll(self.pixels, 1, axis=0)

