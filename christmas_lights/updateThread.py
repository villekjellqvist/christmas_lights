import threading
import time
from christmas_lights.utils import ScriptImporter, TimeKeeper, sendToGPIO, rgb, DaemonPid
from christmas_lights.config import SA_NAME, NR_PIXELS, UPDATETIME, PIDFILE
import numpy as np
import SharedArray as sa


def createSA():
    global SA
    try:
        SA = sa.create(SA_NAME, (NR_PIXELS+1,3))
        SA[:,:] = 0
    except FileExistsError:
        sa.delete(SA_NAME)
        SA = sa.create(SA_NAME, (NR_PIXELS+1,3))
        SA[:,:] = 0


class LightsRunner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pixelsRGB = []
        self.pixels = np.zeros((NR_PIXELS,3))
        self.lock = threading.Lock()
        self._stop_event = threading.Event()
        self.timeKeeper = TimeKeeper(UPDATETIME)

        self.scriptImporter = ScriptImporter(self.pixels)
        self.scriptImporter.findscripts()
        self.scriptImporter.currentScriptIndex = 0

        self.pidFile = DaemonPid(PIDFILE)
        createSA()

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            self.timeKeeper.wait()
            self.scriptImporter.updateFunc()
            self.pixels = self.scriptImporter.patternMaker.pixels
            sendToGPIO(self.pixels, SA)
            with self.lock:
                self.pixelsRGB = rgb(self.pixels)

    def stop(self):
        self._stop_event.set()
        sa.delete("lights")
        self.pidFile.closeFile()
        print("Thread is stopped")

    def getPixels(self):
        with self.lock:
            ret = self.pixelsRGB
        return ret
