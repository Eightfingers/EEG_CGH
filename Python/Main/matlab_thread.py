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
        self.signals_to_main = AppSignals() # used for all 21 positions
        self.signals_to_main2 = AppSignals() # used for fpz positions
        self.signals_to_status = AppSignals()
        self.signals_to_menu = AppSignals()

        self.signals_to_main.signal_numpy.connect(parent.show_eeg_positions)
        self.signals_to_main2.signal_numpy.connect(parent.show_fpz_position)
        self.signals_to_main2.signal_bool.connect(parent.set_live_fpz_positions)
        self.signals_to_status.signal_list.connect(parent.left_dock_status_widget.change_label) # change label function is found in status_widget.py
        self.signals_to_menu.signal_str.connect(parent.left_dock_menu_widget.change_predict_state) # change button text on the menu widget

    def run(self):
        # Start the Matlab Engine
        try:
            # I know this can be a tuple/dictionary but this is the first thing that came to my mind
            self.signals_to_status.signal_list.emit(["Matlab","Testing"]) # emit a list signal
            print("MATLAB: Starting Matlab engine!")
            self.eng = matlab.engine.start_matlab()
            print("MATLAB: Matlab engine running!")
            print("MATLAB: Is 37 a prime?")
            tf = self.eng.isprime(37)
            print("MATLAB: Matlab says its ...")
            print(tf)
            print("MATLAB: Trying to call matlab script")
            triangle_size = self.eng.test(1,2)
            print(triangle_size)
            print("MATLAB: Success")
            self.signals_to_status.signal_list.emit(["Matlab","Okay"]) # emit a list signal
        except Exception as e:
            self.signals_to_status.signal_list.emit(["Matlab","Error"]) # emit a list signal
            print(e)

    @Slot(list)
    def spawn_thread(self, message):
        stylus_data = message[0]
        specs_data = message[1]
        command = message[2]

        self.worker_thread = MatlabWorkerThread(stylus_data, specs_data, command, self)
        self.worker_thread.start()
        # print("Spawn matlab thread called!!!")
        # print(message)
        
# Create a worker thread that is responsible for executing of scripts inside the matlab engine
class MatlabWorkerThread(QThread):
    def __init__(self, stylus_data, specs_data, command, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.matlab_engine = parent.eng
        self._stylus_data = stylus_data 
        self._specs_data = specs_data
        self._command = command
        # print("specs_Data iss")
        # print(self._specs_data)
        # print("Tryna do some stuff")

    def run(self):
        try:
            if self._command == "NZIZ positions":
                nziz_positions = self.matlab_engine.get_nziz()
                # nziz_positions = self.matlab_engine.get_nziz_30_9_2021()
                nziz_positions = np.array(nziz_positions)
                print("Matlab: The NZIZ positions are:", nziz_positions)
                self.parent.signals_to_main2.signal_numpy.emit(nziz_positions)
                self.parent.signals_to_main2.signal_bool.emit(True)

            elif self._command == "21 positions":
                all_positions = self.matlab_engine.EEGpoints_quat()
                all_positions = np.array(all_positions)
                print(all_positions)
                print("Matlab: The All positions are:", all_positions)
                self.parent.signals_to_main.signal_numpy.emit(all_positions) 
            self.parent.signals_to_menu.signal_str.emit(self._command) # indicate it has finished predicting

        except Exception as e:
            print("Matlab: Error in running the script")
            print(e)