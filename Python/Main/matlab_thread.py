import sys
from matlab.engine import matlabengine
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox
import matlab.engine
from debug_trace import trace_matlab
from app_signals import AppSignals

# In optitrack, the quaternion follows q=x*i+y*j+z*k+w; However, In matlab, the quaternion follows q=w+x*i+y*j+z*k
# Create the main Thread

class MatlabMainThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        # Instantiate signals and connect signals to the Slots at the StatusWidget (parent)
        self.signals_to_main = AppSignals() # used for all 21 positions
        self.signals_to_main2 = AppSignals() # used for fpz positions
        self.signals_to_status = AppSignals()
        self.signals_to_menu = AppSignals()

        self.signals_to_main.signal_numpy.connect(parent.update_save_predicted_eeg_positions)
        self.signals_to_main.signal_bool.connect(parent.set_live_predicted_eeg_positions)
        self.signals_to_main2.signal_numpy.connect(parent.update_fpz_position)
        self.signals_to_main2.signal_bool.connect(parent.set_live_fpz_positions)

        self.signals_to_status.signal_list.connect(parent.left_dock_status_widget.change_label) # change label function is found in status_widget.py
        self.signals_to_menu.signal_str.connect(parent.left_dock_menu_widget.change_predict_state) # change button text on the menu widget

    def run(self):
        # Start the Matlab Engine
        try:
            # I know this can be a tuple/dictionary but this is the first thing that came to my mind
            self.signals_to_status.signal_list.emit(["Matlab","Testing"]) # emit a list signal
            trace_matlab("Starting Matlab engine!")
            self.eng = matlab.engine.start_matlab()
            trace_matlab("Matlab engine running!")
            trace_matlab("Is 37 a prime?")
            tf = self.eng.isprime(37)
            trace_matlab("Matlab says its ...")
            trace_matlab(tf)
            trace_matlab("Trying to call matlab script")
            triangle_size = self.eng.test(1,2)
            trace_matlab(triangle_size)
            trace_matlab("Success")
            self.signals_to_status.signal_list.emit(["Matlab","Okay"]) # emit a list signal
        except Exception as e:
            self.signals_to_status.signal_list.emit(["Matlab","Error"]) # emit a list signal
            trace_matlab(e)

    @Slot(list)
    def spawn_thread(self, message):
        command = message[0]

        self.worker_thread = MatlabWorkerThread(command, self)
        self.worker_thread.start()
        
# Create a worker thread that is responsible for executing of scripts inside the matlab engine
class MatlabWorkerThread(QThread):
    def __init__(self, command, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
        self.matlab_engine = parent.eng
        self._command = command

    def run(self):
        try:
            if self._command == "NZIZ positions":
                nziz_positions = self.matlab_engine.get_nziz()
                # nziz_positions = self.matlab_engine.get_nziz_30_9_2021()
                # nziz_positions = self.matlab_engine.no_transform_get_nziz() # no spec transfofrm
                nziz_positions = np.array(nziz_positions)
                trace_matlab("The NZIZ positions are:\n {}".format(nziz_positions))
                
                np.savetxt("nziz_positions.csv", nziz_positions, delimiter=',')
                self.parent.signals_to_main2.signal_numpy.emit(nziz_positions) # Update positions in main.py
                self.parent.signals_to_main2.signal_bool.emit(True) # Start global transformation

            elif self._command == "21 positions":
                all_positions = self.matlab_engine.EEGpoints_quat() # no spec transform at all
                # all_positions = self.matlab_engine.no_transform_EEGpoints_quat() # no spec transform at all
                all_positions = np.array(all_positions)
                trace_matlab("The 21 positions are:\n {}".format(all_positions))
                self.parent.signals_to_main.signal_numpy.emit(all_positions) 
                self.parent.signals_to_main.signal_bool.emit(True) # After finish predicting, make it live 
            self.parent.signals_to_menu.signal_str.emit(self._command) # indicate it has finished predicting

        except Exception as e:
            trace_matlab("Error in running the script")
            trace_matlab(e)