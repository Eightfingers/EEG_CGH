import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox
import matlab.engine
from app_signals import AppSignals

# Create the main Thread
class MatlabMainThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        # Instantiate signals and connect signals to the Slots at the StatusWidget (parent)
        self.signals = AppSignals()
        self.status_widget = parent.left_dock_status_widget
        self.menu_widget = parent.left_dock_menu_widget

        self.signals.signal_list.connect(self.status_widget.change_label) # change label function is found in status_widget.py
        self.signals.signal_numpy.connect(parent.show_nziz_positions)

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
        except Exception as e:
            self.signals.signal_list.emit(["Matlab","Error"]) # emit a list signal
            print(e)

    @Slot(int)
    def spawn_thread(self, message):
        self.worker_thread = MatlabWorkerThread(self)
        self.worker_thread.start()
        # print("Spawn matlab thread called!!!")
        # print(message)
        
# Create a worker thread that is responsible for executing of scripts inside the matlab engine
class MatlabWorkerThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.matlab_engine = parent.eng
        # print("Tryna do some stuff")
        kekw = self.matlab_engine.test(3,2)
        # parent.signals.signal_numpy.emit(kekw) # emit da results
        print(kekw)

    def run(self):
        try:
            pass
        except:
            pass
