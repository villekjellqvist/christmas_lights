import threading
from time import sleep
from christmas_lights.utils import ScriptImporter
import numpy as np

class LightsRunner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.palette = []
        self.lock = threading.Lock()
        self._stop_event = threading.Event()

        self.scriptImporter = ScriptImporter()
        self.scriptImporter.findscripts()
        self.scriptImporter.setCurrentScript(self.scriptImporter.scripts[0])

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            with self.lock:
                self.palette = self.scriptImporter.updateFunc()
            sleep(0.02)

    def stop(self):
        self._stop_event.set()
        self.palette = np.zeros_like(self.palette).tolist()
        print("Thread is stopped")
        

    def getPixels(self):
        if self.stopped():
            return
        with self.lock:
            ret = self.palette
        return ret