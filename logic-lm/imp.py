# the pyke i downloadded needed imp, but imp doesnt exist anymore, so this gets it back from the past
import importlib

def reload(module):
    return importlib.reload(module)
