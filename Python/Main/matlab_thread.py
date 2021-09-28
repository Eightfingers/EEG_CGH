import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import matlab.engine
from matlab_signal import MatlabSignals

# Create the main Thread
class MatlabMainThread(QThread):
    def __init__(self,status_widget, menu_widget, parent=None):
        QThread.__init__(self, parent)

        # Instantiate signals and connect signals to the Slots at the StatusWidget (parent)
        self.signals = MatlabSignals()
        self._status_widget = status_widget
        self._menu_widget = menu_widget

        self.signals.signal_list.connect(self._status_widget.change_label) # change label function is found in status_widget.py
 
    def run(self):
        # Start the Matlab Engine
        try:
            # I know this can be a tuple/dictionary but this is the first thing that came to my mind
            self.signals.signal_list.emit(["Matlab","Testing"]) # emit a list signal
            print("Starting Matlab engine!")
            self.eng = matlab.engine.start_matlab()
            print("Matlab engine running!")
            print("Is 37 a prime?")
            tf = self.eng.isprime(37)
            print("Matlab says its ...")
            print(tf)
            print("Trying to call matlab script")
            triangle_size = self.eng.test(1,2)
            print(triangle_size)
            print("Success")
            self.signals.signal_list.emit(["Matlab","Okay"]) # emit a list signal
        except:
            print("Error in starting or calling matlab engine")

    @Slot()
    def spawn_thread(self, message):
        print("Spawn matlab thread called!!!")
        print(message)
        
# Create a worker thread that is responsible for executing of scripts inside the matlab engine
class MatlabWorkerThread(QThread):
    def __init__(self,matlab_engine, parent=None):
        QThread.__init__(self, parent)
        self._matlab_engine = matlab_engine

    def run(self):
        # Start the Matlab Engine
        try:
            print("I am spawned!@")
        except:
            print("wtf")
