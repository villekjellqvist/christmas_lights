import threading
import time
from christmas_lights.utils import ScriptImporter, TimeKeeper
import numpy as np

UPDATETIME = 0.02

class LightsRunner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pixels = []
        self.lock = threading.Lock()
        self._stop_event = threading.Event()
        self.timeKeeper = TimeKeeper()

        self.scriptImporter = ScriptImporter()
        self.scriptImporter.findscripts()
        self.scriptImporter.currentScriptIndex = 0

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            pixels = self.timeKeeper.runFunc(
                    UPDATETIME, self.scriptImporter.updateFunc
                )
            with self.lock:
                self.pixels = pixels

    def stop(self):
        self._stop_event.set()
        self.pixels = np.zeros_like(self.pixels).tolist()
        print("Thread is stopped")

    def getPixels(self):
        with self.lock:
            ret = self.pixels
        return ret
