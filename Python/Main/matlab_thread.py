import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import matlab.engine

# Signals must inherit QObject
class MatlabSignals(QObject):
    signal_str = Signal(str)
    signal_int = Signal(int)
    signal_np = Signal(np.ndarray) 
    signal_list = Signal(list)
    signal_dict = Signal(dict)

# Create the Worker Thread
class MatlabMainThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        # Instantiate signals and connect signals to the Slots at the StatusWidget (parent)
        self.signals = MatlabSignals()
        self.signals.signal_list.connect(parent.change_label)

        # self.signals.signal_int.connect(parent.update_int_field)
        # self.signals.signal_np.connect(parent.update_np_field)
        # self.signals.signal_list.connect(parent.update_list_field)

    def run(self):
        # Do something on the worker thread
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



        # Emit signals whenever you want
        # self.signals.signal_int.emit(a) 
        # self.signals.signal_np.emit(coordinates) # emit np
        # self.signals.signal_list.emit([a,b,c]) # emit list
