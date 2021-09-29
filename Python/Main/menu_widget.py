import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot, QSize)
from PySide6.QtGui import QGuiApplication, QVector3D
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QLabel, QBoxLayout, QMessageBox
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)

import numpy as np
import random
from matlab_thread import MatlabMainThread
from matlab_signal import MatlabSignals
from optitrack_signal import OptitrackSignals

class MenuWidget(QWidget):

    def __init__(self, layout,scatter, scatter_series, parent=None):
        QWidget.__init__(self, parent)

        # store the format of the layout
        self._layout = layout
        self._scatter = scatter
        self._scatter_series = scatter_series

        self.is_recording_flag = False # Used to indicate whether any of the button is recording or not. So far not yet used might be useful later?

        self.NZIZbutton_state = False # False is not recording
        self.Circumbutton_state = False
        self.EartoEarutton_state = False

        self.NZIZbutton_text = "Start NZIZ"
        self.Circumbutton_text = "Start Circum"
        self.EartoEarbutton_text = "Start Ear to Ear"

        # I dont think this is being used yet for now.. Also
        self._matlab_thread = None # None for now, we will wait until the Matlab engine finish intializing the threads in the main.py loop then connect them
        self.matlab_signal = MatlabSignals()

        # I dont think this is being used yet for now.. Also
        self._optitrack_thread = None # None for now, we will wait until the Matlab engine finish intializing the threads in the main.py loop then connect them
        self.optitrack_signals = OptitrackSignals()

        # Create Button widget
        self.NZIZbutton = QPushButton(self.NZIZbutton_text)
        self.NZIZbutton.clicked.connect(self.do_nziz) # start a thread when the button is clicked

        self.Circumbutton = QPushButton(self.Circumbutton_text)
        self.Circumbutton.clicked.connect(self.do_circum) # start a thread when the button is clicked

        self.EartoearButton = QPushButton(self.EartoEarbutton_text)
        self.EartoearButton.clicked.connect(self.do_ear_to_ear) # start a thread when the button is clicked

        self.predict_button = QPushButton("Predict")
        self.predict_button.clicked.connect(self.predict_eeg_positions)
        
        self._layout.addWidget(self.NZIZbutton)
        self._layout.addWidget(self.Circumbutton)
        self._layout.addWidget(self.EartoearButton)
        self._layout.addWidget(self.predict_button)
        self._layout.addStretch()

    # I am not sure if this is the best way or so but
    # These functions are called from the main.py and the thread and 
    # 
    def connect_matlab_signals(self, matlab_thread): 
        self._matlab_thread = matlab_thread
        self.matlab_signals.signal_int.connect(self._matlab_thread.spawn_thread)

    def connect_matlab_signals (self, optitrack_thread):
        self._optitrack_thread = optitrack_thread
        self.optitrack_signals.signal_bool.connect(self.set_recording) 

    @Slot()
    def do_nziz(self):
        print("NZIZ started")
        self.change_button_state(self.NZIZbutton, self.NZIZbutton_text)
        # self.matlab_signal.signal_int.emit(1)
        # print("Spawn thread succesful")
        self.optitrack_signals.signal_bool.emit(True)
        print("Okay bool signal emitted from menu widget")

    @Slot()
    def do_circum(self):
        self.change_button_state(self.Circumbutton, self.Circumbutton_text)
        print("Circum started")

    @Slot()
    def do_ear_to_ear(self):
        self.change_button_state(self.EartoearButton, self.EartoEarbutton_text)
        print("Ear 2 Ear started")
    
    @Slot()
    def predict_eeg_positions(self):
        print("Tryna predict eeg positions")

    def change_button_state(self, button, button_label):
        if(button.isFlat()): 
            button.setStyleSheet('QPushButton {background-color: light gray ; color: black;}')
            button.setText(button_label)
            button.setFlat(False)
            
        elif (not self.NZIZbutton.isFlat() and not self.Circumbutton.isFlat() and not self.EartoearButton.isFlat()): # only press the button when it is the only button not flat?
            # Not setting border width here causes a bug where the background colour isnt changed at all ?
            # I can't seem to replicate this on an standalone code that only has a button widget (without the rest of the dock and stuff)
            ### Anyway there is probably a better way to set this stylesheet but this should do also the button size CHANGES when its this set to flat 
            button.setStyleSheet('QPushButton {background-color: rgb(225, 0, 0); color: black; border-style: outset; border-width: 1px; border-color: black;}')
            button.setText('Stop!')
            button.setFlat(True)

        else:
            QMessageBox.warning(self, "Warning", "Finish other recordings first!")
