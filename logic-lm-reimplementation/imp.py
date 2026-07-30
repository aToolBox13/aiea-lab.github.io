# fake imp module so old pyke code stops crying on python 3.12+
# pyke only ever calls imp.reload(), so thats all we need here
import importlib

def reload(module):
    return importlib.reload(module)
