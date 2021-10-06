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

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # store the format of the layout
        self.layout = parent.menu_layout
        self.parent = parent
        
        # https://stackoverflow.com/questions/1296501/find-path-to-currently-running-file
        self.save_directory = os.getcwd() + "\RecordedData"

        self.is_recording_flag = False # Used to indicate whether any of the button is recording or not. So far not yet used might be useful later?

        self.NZIZbutton_text = "Start NZIZ"
        self.Circumbutton_text = "Start Circum"
        self.EartoEarbutton_text = "Start Ear to Ear"

        # I dont think this is being used yet for now.. 
        self._matlab_thread = None # None for now, we will wait until the Matlab engine finish intializing the threads in the main.py loop then connect them
        self.matlab_signals = AppSignals()
        self.fpz_signals = AppSignals()

        self._optitrack_thread = None 
        
        self.NZIZoptitrack_signals = AppSignals()
        self.NZIZoptitrack_signals.signal_numpy.connect(parent.update_and_add_scatterNZIZ)

        self.CIRCUMoptitrack_signals = AppSignals()
        self.CIRCUMoptitrack_signals.signal_numpy.connect(parent.update_and_add_scatterCIRCUM)

        self.EarToEaroptitrack_signals = AppSignals()
        self.EarToEaroptitrack_signals.signal_numpy.connect(parent.update_and_add_scatterEarToEar)

        self.optitrack_signals = AppSignals() 
        self.optitrack_signals.signal_list.connect(parent.left_dock_status_widget.change_label)

        # Create Button widgets
        self.NZIZbutton = QPushButton(self.NZIZbutton_text)
        self.NZIZbutton.clicked.connect(self.do_nziz) # start a thread when the button is clicked

        self.Circumbutton = QPushButton(self.Circumbutton_text)
        self.Circumbutton.clicked.connect(self.do_circum) # start a thread when the button is clicked

        self.EartoearButton = QPushButton(self.EartoEarbutton_text)
        self.EartoearButton.clicked.connect(self.do_ear_to_ear) # start a thread when the button is clicked

        self.predictpz_button = QPushButton("Predict Fpz")
        self.predictpz_button.clicked.connect(self.predict_fpz_position) # can only start when there are 3 scatter data

        self.predict_button = QPushButton("Predict 21")
        self.predict_button.clicked.connect(self.predict_eeg_positions) # can only start when there are 3 scatter data

        self.clear_button = QPushButton("Clear") # Clear EEG positions
        self.clear_button.clicked.connect(parent.clear_data) 

        self.layout.addWidget(self.NZIZbutton)
        self.layout.addWidget(self.Circumbutton)
        self.layout.addWidget(self.EartoearButton)
        self.layout.addWidget(self.predictpz_button)
        self.layout.addWidget(self.predict_button)
        self.layout.addWidget(self.clear_button)
        self.layout.addStretch()

    # I am not sure if this is the best way or so but
    # These functions are called from the main.py and the thread and 
    # 

    def connect_matlab_signals(self, matlab_thread): 
        self._matlab_thread = matlab_thread
        self.matlab_signals.signal_list.connect(self.parent.update_and_add_scatterNZIZ)
        self.fpz_signals.signal_list.connect(self._matlab_thread.spawn_thread)

    def connect_optitrack_signals (self, optitrack_thread):
        self._optitrack_thread = optitrack_thread
        self.optitrack_signals.signal_bool.connect(self._optitrack_thread.set_recording) 
        self.optitrack_signals.signal_bool.connect(self._optitrack_thread.clear_data)

    @Slot()
    def do_nziz(self):
        self.change_button_state(self.NZIZbutton, self.NZIZbutton_text)

    @Slot()
    def do_circum(self):
        self.change_button_state(self.Circumbutton, self.Circumbutton_text)

    @Slot()
    def do_ear_to_ear(self):
        self.change_button_state(self.EartoearButton, self.EartoEarbutton_text)
    
    def predict_eeg_positions(self):
        print("Tryna predict eeg positions")
        if (self.parent.NZIZscatter_series.dataProxy().itemCount() == 0 and  self.parent.CIRCUMscatter_series.dataProxy().itemCount() == 0 and self.parent.EarToEarscatter_series.dataProxy().itemCount() == 0 ):
            QMessageBox.warning(self, "Warning", "Please complete all 3 takes first!!")
        else:
            print("Predict stuff now")

    @Slot()
    def predict_fpz_position(self):
        print("Predicting FPZ position")
        message = [self.parent.NZIZ_data, self.parent.NZIZ_specs_data]
        self.fpz_signals.signal_list.emit(message)

        # if (parent.NZIZscatter_series.dataProxy().itemCount() == 0):
        #     QMessageBox.warning(self, "Warning", "Please complete NZIZ trace first!!")
        # else:
        #     # Call the matlab engine 
        #     print("Predict stuff now")

    def change_button_state(self, button, button_label):
        if(button.isFlat()): # If the initial state of the button is flat and it is clicked, unflat them
            button.setStyleSheet('QPushButton {background-color: light gray ; color: black;}')
            button.setText(button_label)
            button.setFlat(False)

            # Get the data from the optitrack thread
            self.stylus_data = self._optitrack_thread.stylus_data 
            self.specs = self._optitrack_thread.specs_data 
            self.specs_rotation = self._optitrack_thread.specs_rotation_data

            # Strip of all the zeroes
            self.stylus_data = self.stylus_data[~np.all(self.stylus_data == 0, axis=1)]
            self.specs = self.specs[~np.all(self.specs == 0, axis=1)]
            self.specs_rotation = self.specs_rotation[~np.all(self.specs_rotation == 0, axis=1)]

            # Save the data accordingly
            if (button_label == "Start NZIZ"):
                self.NZIZstylus_data = self.stylus_data
                self.NZIZspecs_data = self.specs

                # self.parent.NZIZ_data = self.NZIZstylus_data
                # self.parent.NZIZ_specs_data = self.NZIZspecs_data # SHIT NOT WORKING ?
                # print("IS DATA SAVE ACCORDINGLY/")
                # print(self.parent.NZIZ_specs_data)
                # print(self.parent.NZIZ_data)
                self.NZIZ_specs_rotation = self.specs_rotation
                print(self.NZIZstylus_data)
                # update parent variables
                np.savetxt("data_NZIZstylus.csv",self.NZIZstylus_data, delimiter=',')
                np.savetxt("data_NZIZspecs.csv",self.NZIZspecs_data, delimiter=',')
                np.savetxt("rotation_data_NZIZspecs.csv",self.NZIZ_specs_rotation, delimiter=',')

                self.NZIZoptitrack_signals.signal_numpy.emit(self.NZIZstylus_data)

            elif (button_label == "Start Circum"):
                self.CIRCUMstylus_data = self.stylus_data
                self.CIRCUMspecs_data = self.specs
                np.savetxt(self.save_directory + "\data_CIRCUMstylus.csv",self.CIRCUMstylus_data, delimiter=',')
                np.savetxt(self.save_directory + "\data_CIRCUMspecs.csv",self.CIRCUMspecs_data, delimiter=',')
                # emit to update to the main widget
                self.CIRCUMoptitrack_signals.signal_numpy.emit(self.CIRCUMstylus_data)

            elif (button_label == "Start Ear to Ear"):
                self.EarToEarstylus_data = self.stylus_data
                self.EarToEarpecs_data = self.specs
                np.savetxt(self.save_directory + "\data_EarToEarstylus.csv", self.EarToEarstylus_data, delimiter=',')
                np.savetxt(self.save_directory + "\data_EarToEarspecs.csv", self.EarToEarpecs_data, delimiter=',')
                self.EarToEaroptitrack_signals.signal_numpy.emit(self.EarToEarstylus_data)

            self.optitrack_signals.signal_bool.emit(False) # Stop recording
            self.optitrack_signals.signal_list.emit(["Stylus","Stopped"])
            self.optitrack_signals.signal_list.emit(["Specs","Stopped"])


        elif (not self.NZIZbutton.isFlat() and not self.Circumbutton.isFlat() and not self.EartoearButton.isFlat()): # only press the button when it is the only button not flat?
            # Not setting border width here causes a bug where the background colour isnt changed at all ?
            # I can't seem to replicate this on an standalone code that only has a button widget (without the rest of the dock and stuff)
            ### Anyway there is probably a better way to set this stylesheet but this should do also the button size CHANGES when its this set to flat 
            button.setStyleSheet('QPushButton {background-color: rgb(225, 0, 0); color: black; border-style: outset; border-width: 1px; border-color: black;}')
            button.setText('Stop!')
            button.setFlat(True)
            self.optitrack_signals.signal_bool.emit(True)

        else:
            QMessageBox.warning(self, "Warning", "Finish other recordings first!")
