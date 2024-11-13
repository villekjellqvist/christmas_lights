import importlib
import os
import sys
import time
import typing
import numpy as np

class AbstractPattern:
    def __init__(self, pixels_array):
        self.pixels = np.asarray(pixels_array, dtype=int)
        self.nrpixels = self.pixels.shape[0]

    def start(self):
        pass
    
    def update(self):
        raise NotImplementedError

    def fade(self,val:float):
        self.pixels = np.asarray(self.pixels*val, dtype=int)

class zeroPattern(AbstractPattern):
    def update(self):
        self.pixels = np.zeros_like(self.pixels)
        
def rgb(array):
    ret = []
    for p in array:
        r = int(p[0])
        g = int(p[1])
        b = int(p[2])
        ret.append(f"rgb({r},{g},{b})")
    return ret

def sendToGPIO(pixels, SA, GPIO_enabled_checker):
    if not GPIO_enabled_checker():
        SA[1:] = 0
        SA[0] = 1
        return
    while np.allclose(SA[0], 1):
        if not GPIO_enabled_checker():
            SA[1:] = 0
            SA[0] = 1
        return
        time.sleep(1)
    SA[1:] = pixels
    SA[0] = 1
    
class DaemonPid:
    def __init__(self, pidfile):
        self.pidfile = pidfile
        self.pid = str(os.getpid())
        if os.path.isfile(self.pidfile):
            print("PID file exists. Deleting...")
            os.remove(self.pidfile)
        with open(self.pidfile, mode='w') as file:
            file.write(self.pid)
            print("Successfully written PID file")
    
    def closeFile(self):
        os.remove(self.pidfile)


class TimeKeeper:
    def __init__(self, interval:int):
        self.interval = interval
        self.latest = int((time.time_ns() // 1e9) * 1000)

    def _time_ms(self):
        return int(time.time_ns() // 1e6)

    def wait(self):
        sleeptime = (self.interval + self.latest - self._time_ms())/1000
        time.sleep(max(sleeptime,0))
        self.latest = self._time_ms()

class ScriptImporter:
    patternMaker:AbstractPattern
    patternsFolder = "christmas_lights/patterns"
    scripts = []
    currentScript = ""
    _currentScriptIndex = 0
    updateFunc = None

    def __init__(self, pixels_array):
        self.pixels_array = pixels_array

    @property
    def currentScriptIndex(self):
        return self._currentScriptIndex
    
    @currentScriptIndex.setter
    def currentScriptIndex(self, value:int):
        if type(value) is not int:
            raise ValueError("currentScriptIndex must be set to int")
        if value > len(self.scripts):
            self._currentScriptIndex = 0
        elif value < 0:
            self._currentScriptIndex = -1
            self.patternMaker = zeroPattern(self.pixels_array)
            self.updateFunc = self.patternMaker.update
            return
        else:
            self._currentScriptIndex = value
        self._setCurrentScript(self._currentScriptIndex)
        

    def findscripts(self):
        folder = os.path.relpath(self.patternsFolder)
        scripts_in_folder = []
        for file in os.listdir(folder):
            if file.endswith(".py"):
                scripts_in_folder.append(file)
        self.scripts = scripts_in_folder

    def _setCurrentScript(self, scriptnr:int):
        self.currentScript = self.scripts[scriptnr]
        scriptpath = os.path.join(self.patternsFolder, self.currentScript)
        scriptmodulepath = scriptpath.replace('/','.').replace('.py','')
        try:
            scriptmodule = importlib.import_module(scriptmodulepath)
            self.patternMaker = scriptmodule.Pattern(self.pixels_array)
            self.patternMaker.start()
            self.updateFunc = self.patternMaker.update
            del scriptmodule
        except ImportError:
            ImportError(f"Error importing file {script}")

    def cycleScript(self, steps=1):
        if steps > len(self.scripts):
            raise RuntimeError("No working scriptfiles found.")
        try:
            self.currentScriptIndex += steps
        except ImportError:
            self.cycleScript(steps+1)

