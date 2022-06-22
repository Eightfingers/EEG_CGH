import numpy as np

class EEGPosition():
    def __init__(self, position, name):

        self.position = position # numpy array of xyz
        self.name = name
        self.visible = False
