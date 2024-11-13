import numpy as np
from christmas_lights.utils import AbstractPattern

class Pattern(AbstractPattern):
    colors = ("red", "green", "blue")
    currentColor = 0
    i = 0
    j = 0
    def start(self):
        for i in range(self.nrpixels):
            self.pixels[i] = ((self.nrpixels - i) * 255 / self.nrpixels, i * 50 / self.nrpixels, i * 255 / self.nrpixels)

    def update(self):
        self.fade(0.75)
        self.pixels[self.j] = self.getColor()
        self.i += 1
        self.j += self.i%5 == 0
        if self.j == self.nrpixels:
            self.j = 0
            self.currentColor = (self.currentColor + 1)%3
        

    def getColor(self):
        color = self.colors[self.currentColor]
        if color == "red":
            return (255,0,0)
        if color == "green":
            return (0,255,0)
        if color == "blue":
            return (0,0,255)

