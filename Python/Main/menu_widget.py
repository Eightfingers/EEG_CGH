import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot, QSize)
from PySide6.QtGui import QGuiApplication, QVector3D
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QLabel, QBoxLayout, QMessageBox
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)

import numpy as np
import sys, os
from matlab_thread import MatlabMainThread
from pathlib import Path
from app_signals import AppSignals

class MenuWidget(QWidget):

    # Button number convention

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # store the format of the layout
        self.layout = parent.menu_layout

        self.NZIZ_BUTTON = 1
        self.CIRCUM_BUTTON = 2
        self.EARTOEAR_BUTTON = 3
        self.lock = False

        self.parent = parent # Couldn't find a way to reference the parent, from the class functions.
        
        # https://stackoverflow.com/questions/1296501/find-path-to-currently-running-file
        self.save_directory = os.getcwd() + "\RecordedData"

        self.is_recording_flag = False # Used to indicate whether any of the button is recording or not. So far not yet used might be useful later?

        self.NZIZbutton_text = "Start NZIZ"
        self.Circumbutton_text = "Start Circum"
        self.EartoEarbutton_text = "Start Ear to Ear"
        self.attach_electrodes_button_text = "Attach electrodes"

        # I dont think this is being used yet for now.. 
        self._matlab_thread = None # None for now, we will wait until the Matlab engine finish intializing the threads in the main.py loop then connect them
        self._optitrack_thread = None 
        
        self.signals_to_matlab = AppSignals()

        self.signals_to_optitrack = AppSignals()

        self.signals_to_main = AppSignals()
        self.signals_to_main.signal_int.connect(parent.save_data) 
        self.signals_to_main.signal_bool.connect(parent.set_live_predicted_eeg_positions)
        
        self.NZIZdata_to_main_signals = AppSignals()
        self.NZIZdata_to_main_signals.signal_numpy.connect(parent.update_and_add_scatterNZIZ)

        self.CIRCUMdata_to_main_signals = AppSignals()
        self.CIRCUMdata_to_main_signals.signal_numpy.connect(parent.update_and_add_scatterCIRCUM)

        self.EarToEardata_to_main_signals = AppSignals()
        self.EarToEardata_to_main_signals.signal_numpy.connect(parent.update_and_add_scatterEarToEar)

        self.signals_to_status = AppSignals() 
        self.signals_to_status.signal_list.connect(parent.left_dock_status_widget.change_label)

        # Create Button widgets
        self.NZIZbutton = QPushButton(self.NZIZbutton_text)
        self.NZIZbutton.clicked.connect(self.do_nziz) # start a thread when the button is clicked

        self.Circumbutton = QPushButton(self.Circumbutton_text)
        self.Circumbutton.clicked.connect(self.do_circum) # start a thread when the button is clicked

        self.EartoearButton = QPushButton(self.EartoEarbutton_text)
        self.EartoearButton.clicked.connect(self.do_ear_to_ear) # start a thread when the button is clicked

        self.attach_electrodes_button = QPushButton(self.attach_electrodes_button_text)
        self.attach_electrodes_button.clicked.connect(self.do_eeg_placements) # can only start when there are 3 scatter data

        self.predictpz_button = QPushButton("Predict Fpz")
        self.predictpz_button.clicked.connect(self.predict_fpz_position) # can only start when there are 3 scatter data

        self.predict_all_button = QPushButton("Predict 21")
        self.predict_all_button.clicked.connect(self.predict_eeg_positions) # can only start when there are 3 scatter data

        self.clear_button = QPushButton("Clear") # Clear EEG positions
        self.clear_button.clicked.connect(parent.clear_data) 

        self.layout.addWidget(self.NZIZbutton)
        self.layout.addWidget(self.Circumbutton)
        self.layout.addWidget(self.EartoearButton)
        self.layout.addWidget(self.predictpz_button)
        self.layout.addWidget(self.predict_all_button)
        self.layout.addWidget(self.attach_electrodes_button)
        self.layout.addWidget(self.clear_button)
        self.layout.addStretch()

    # I am not sure if this is the best way or so but
    # These functions are called from the main.py and these signals are only initialized after 
    # matlab engine is fullying running and stuff

    def connect_matlab_signals(self, matlab_thread): 
        self._matlab_thread = matlab_thread
        self.signals_to_matlab.signal_list.connect(self._matlab_thread.spawn_thread)

    def connect_optitrack_signals (self, optitrack_thread):
        self._optitrack_thread = optitrack_thread
        self.signals_to_status.signal_bool.connect(self._optitrack_thread.set_recording) 
        self.signals_to_status.signal_bool.connect(self._optitrack_thread.clear_data)
        self.signals_to_optitrack.signal_bool.connect(self._optitrack_thread.set_show_all_markers)

    @Slot()
    def do_nziz(self):
        self.change_trace_button_state(self.NZIZbutton, self.NZIZbutton_text)

    @Slot()
    def do_circum(self):
        self.change_trace_button_state(self.Circumbutton, self.Circumbutton_text)

    @Slot()
    def do_ear_to_ear(self):
        self.change_trace_button_state(self.EartoearButton, self.EartoEarbutton_text)

    @Slot()
    def do_eeg_placements(self):
        if self.lock:
            if (self.parent.NZIZscatter_series.dataProxy().itemCount() == 0 and  self.parent.CIRCUMscatter_series.dataProxy().itemCount() == 0 and self.parent.EarToEarscatter_series.dataProxy().itemCount() == 0 ):
                QMessageBox.warning(self, "Warning", "Please complete all 3 takes first!!")
            else:
                if(self.attach_electrodes_button.isFlat()): # If the initial state of the button is flat and it is clicked, unflat them
                    self.attach_electrodes_button.setStyleSheet('QPushButton {background-color: light gray ; color: black;}')
                    self.attach_electrodes_button.setText(self.attach_electrodes_button_text)
                    self.attach_electrodes_button.setFlat(False)
                    self.signals_to_optitrack.signal_bool.emit(False)
                    self.signals_to_main.signal_bool.emit(False)

                else:
                    self.attach_electrodes_button.setStyleSheet('QPushButton {background-color: rgb(225, 0, 0); color: black; border-style: outset; border-width: 1px; border-color: black;}')
                    self.attach_electrodes_button.setText('Stop!')
                    self.attach_electrodes_button.setFlat(True)
                    self.signals_to_optitrack.signal_bool.emit(True)
                    self.signals_to_main.signal_bool.emit(True)
        else:
                if(self.attach_electrodes_button.isFlat()): # If the initial state of the button is flat and it is clicked, unflat them
                    self.attach_electrodes_button.setStyleSheet('QPushButton {background-color: light gray ; color: black;}')
                    self.attach_electrodes_button.setText(self.attach_electrodes_button_text)
                    self.attach_electrodes_button.setFlat(False)
                    self.signals_to_optitrack.signal_bool.emit(False)
                    self.signals_to_main.signal_bool.emit(False)

                else:
                    self.attach_electrodes_button.setStyleSheet('QPushButton {background-color: rgb(225, 0, 0); color: black; border-style: outset; border-width: 1px; border-color: black;}')
                    self.attach_electrodes_button.setText('Stop!')
                    self.attach_electrodes_button.setFlat(True)
                    self.signals_to_optitrack.signal_bool.emit(True)
                    self.signals_to_main.signal_bool.emit(True)

    @Slot(str) # used by the matlab thread to indicate that it has finished predicting
    def change_predict_state(self, message):
        if message == "21 positions":
            self.predict_all_button.setStyleSheet('QPushButton {background-color: light gray ; color: black;}')
            self.predict_all_button.setText("Predict 21")
        elif message == "NZIZ positions":
            self.predictpz_button.setStyleSheet('QPushButton {background-color: light gray ; color: black;}')
            self.predictpz_button.setText("Predict Fpz")
    
    def predict_eeg_positions(self):
        print("Menu: Predict eeg positions")
        if self.lock:
            if (self.parent.NZIZscatter_series.dataProxy().itemCount() == 0 and  self.parent.CIRCUMscatter_series.dataProxy().itemCount() == 0 and self.parent.EarToEarscatter_series.dataProxy().itemCount() == 0 ):
                QMessageBox.warning(self, "Warning", "Please complete all 3 takes first!!")
            else:
                message =[1,2,"21 positions"] # 1,2 is a dummy message
                self.signals_to_matlab.signal_list.emit(message)
                self.predict_all_button.setStyleSheet('QPushButton {background-color: red ; color: black;}')
                self.predict_all_button.setText("Predicting ..")
        else:
            message =[1,2,"21 positions"] # 1,2 is a dummy message
            self.signals_to_matlab.signal_list.emit(message)
            self.predict_all_button.setStyleSheet('QPushButton {background-color: red ; color: black;}')
            self.predict_all_button.setText("Predicting ..")


    def predict_fpz_position(self):
        if self.lock:
            if (self.parent.NZIZscatter_series.dataProxy().itemCount() == 0 ):
                QMessageBox.warning(self, "Warning", "Please complete NZIZ trace!!")
            else:
                print("Menu: Predicting FPZ position")
                self.signals_to_main2.signal_bool.emit(True)
                # message = [self.parent.NZIZ_data, self.parent.NZIZ_specs_data]
                message =[1,2,"NZIZ positions"] # 1,2 is a dummy message
                self.signals_to_matlab.signal_list.emit(message)
                self.signals_to_status.signal_list.emit(["Stylus","Stopped"])
                self.predictpz_button.setStyleSheet('QPushButton {background-color: red ; color: black;}')
                self.predictpz_button.setText("Predicting ..")
        else:
                print("Menu: Predicting FPZ position")
                # message = [self.parent.NZIZ_data, self.parent.NZIZ_specs_data]
                message =[1,2,"NZIZ positions"] # 1,2 is a dummy message
                self.signals_to_matlab.signal_list.emit(message)
                self.signals_to_status.signal_list.emit(["Stylus","Stopped"])
                self.predictpz_button.setStyleSheet('QPushButton {background-color: red ; color: black;}')
                self.predictpz_button.setText("Predicting ..")

    @Slot()
    def change_trace_button_state(self, button, button_label):
        if(button.isFlat()): # If the initial state of the button is flat and it is clicked, unflat them
            button.setStyleSheet('QPushButton {background-color: light gray ; color: black;}')
            button.setText(button_label)
            button.setFlat(False)

            # Save the data accordingly
            if (button_label == "Start NZIZ"):
                self.signals_to_main.signal_int.emit(self.NZIZ_BUTTON)

            elif (button_label == "Start Circum"):
                self.signals_to_main.signal_int.emit(self.CIRCUM_BUTTON)

            elif (button_label == "Start Ear to Ear"):
                self.signals_to_main.signal_int.emit(self.EARTOEAR_BUTTON)

            self.signals_to_status.signal_bool.emit(False) # Stop recording
            self.signals_to_status.signal_list.emit(["Stylus","Stopped"])
            self.signals_to_status.signal_list.emit(["Specs","Stopped"])

        elif (not self.NZIZbutton.isFlat() and not self.Circumbutton.isFlat() and not self.EartoearButton.isFlat()): # only press the button when it is the only button not flat?
            # Not setting border width here causes a bug where the background colour isnt changed at all ?
            # I can't seem to replicate this on an standalone code that only has a button widget (without the rest of the dock and stuff)
            ### Anyway there is probably a better way to set this stylesheet but this should do also the button size CHANGES when its this set to flat 
            button.setStyleSheet('QPushButton {background-color: rgb(225, 0, 0); color: black; border-style: outset; border-width: 1px; border-color: black;}')
            button.setText('Stop!')
            button.setFlat(True)
            self.signals_to_status.signal_bool.emit(True)

        else:
            QMessageBox.warning(self, "Warning", "Finish other recordings first!")
