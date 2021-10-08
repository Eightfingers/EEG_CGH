import sys
from matlab.engine import matlabengine
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox
import matlab.engine
from app_signals import AppSignals


# https://www.geeksforgeeks.org/python-call-parent-class-method/

# Create the main Thread
class MatlabMainThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        # Instantiate signals and connect signals to the Slots at the StatusWidget (parent)
        self.signals_to_main = AppSignals()
        self.signals_to_status = AppSignals()
        
        self.signals_to_main.signal_numpy.connect(parent.show_nziz_positions)
        self.signals_to_status.signal_list.connect(parent.left_dock_status_widget.change_label) # change label function is found in status_widget.py

    def run(self):
        # Start the Matlab Engine
        try:
            # I know this can be a tuple/dictionary but this is the first thing that came to my mind
            self.signals_to_status.signal_list.emit(["Matlab","Testing"]) # emit a list signal
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
            self.signals_to_status.signal_list.emit(["Matlab","Okay"]) # emit a list signal
        except Exception as e:
            self.signals_to_status.signal_list.emit(["Matlab","Error"]) # emit a list signal
            print(e)

    @Slot(list)
    def spawn_thread(self, message):
        stylus_data = message[0]
        specs_data = message[1]

        self.worker_thread = MatlabWorkerThread(stylus_data, specs_data, self)
        self.worker_thread.start()
        # print("Spawn matlab thread called!!!")
        # print(message)
        
# Create a worker thread that is responsible for executing of scripts inside the matlab engine
class MatlabWorkerThread(QThread):
    def __init__(self, specs_data, stylus_data, parent=None):
        QThread.__init__(self, parent)
        self.matlab_engine = parent.eng
        self._stylus_data = stylus_data 
        self._specs_data = specs_data
        # print("specs_Data iss")
        # print(self._specs_data)
        # print("Tryna do some stuff")

        nziz_positions = self.matlab_engine.get_nziz()
        # nziz_positions = self.matlab_engine.get_nziz_30_9_2021()
        nziz_positions = np.array([nziz_positions[0], nziz_positions[1], nziz_positions[2]])
        nziz_positions = np.transpose(nziz_positions)
        print(nziz_positions)
        parent.signals.signal_numpy.emit(nziz_positions) # emit da results


    def run(self):
        try:
            pass
        except:
            pass
