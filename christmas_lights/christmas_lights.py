import threading
from time import sleep
import numpy as np
import importlib
import os



class LightsRunner(threading.Thread):
    def __init__(self, palette):
        super().__init__()
        self.palette = palette
        self.lock = threading.Lock()
        self._stop_event = threading.Event()

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            with self.lock:
                self.palette = np.roll(self.palette, 1).tolist()
            sleep(0.02)

    def stop(self):
        self._stop_event.set()
        self.palette = np.zeros_like(self.palette).tolist()
        print("Thread is stopped")
        

    def getPalette(self):
        if self.stopped():
            return
        with self.lock:
            ret = self.palette
        return ret