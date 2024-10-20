import importlib
import os

class ScriptImporter:
    patternsFolder = "christmas_lights/patterns"
    scripts = []
    currentScript = ""
    listIndex = 0
    updateFunc = None

    def findscripts(self):
        folder = os.path.relpath(self.patternsFolder)
        scripts_in_folder = []
        for file in os.listdir(folder):
            if file.endswith(".py"):
                scripts_in_folder.append(file)
        self.scripts = scripts_in_folder

    def setCurrentScript(self, script:str):
        self.currentScript = script
        scriptpath = os.path.join(self.patternsFolder, self.currentScript)
        scriptmodulepath = scriptpath.replace('/','.').replace('.py','')
        try:
            scriptmodule = importlib.import_module(scriptmodulepath)
            self.updateFunc = scriptmodule.update
            del scriptmodule
        except ImportError:
            ImportError(f"Error importing file {script}")

    def cycleScript(self):
        self.listIndex += 1
        if self.listIndex >= len(self.scripts):
            self.listIndex = 0
        script = self.scripts[self.listIndex]
        self.setCurrentScript(script)
