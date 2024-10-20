import importlib
import os
import time
import typing

class TimeKeeper:
    latest = time.time()

    def runFunc(self, interval:float, func:typing.Callable, *args):
        ret = func(*args)
        funcEnd = time.time()
        time.sleep(max(interval - (funcEnd - self.latest),0))
        self.latest = time.time()
        return ret

class ScriptImporter:
    patternsFolder = "christmas_lights/patterns"
    scripts = []
    currentScript = ""
    _currentScriptIndex = 0
    updateFunc = None

    @property
    def currentScriptIndex(self):
        return self.currentScriptIndex
    
    @currentScriptIndex.setter
    def currentScriptIndex(self, value:int):
        if type(value) is not int:
            raise ValueError("currentScriptIndex must be set to int")
        if value < 0 or value > len(self.scripts):
            self._currentScriptIndex = 0
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

    def _setCurrentScript(self, script:int):
        self.currentScript = self.scripts[script]
        scriptpath = os.path.join(self.patternsFolder, self.currentScript)
        scriptmodulepath = scriptpath.replace('/','.').replace('.py','')
        try:
            scriptmodule = importlib.import_module(scriptmodulepath)
            self.updateFunc = scriptmodule.update
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

