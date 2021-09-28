import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot, QSize)
from PySide6.QtGui import QGuiApplication, QVector3D
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QLabel, QBoxLayout 
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)

import numpy as np
import random
from matlab_thread import MatlabMainThread
from matlab_signal import MatlabSignals

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

        self._matlab_thread = None # None for now, we will wait until the Matlab engine finish intializing in the main.py loop
        self.matlab_signal = MatlabSignals()

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

    def connect_matlab_signals(self, matlab_thread):
        self._matlab_thread = matlab_thread
        self.matlab_signal.signal_int.connect(self._matlab_thread.spawn_thread)
        print("kek")

    @Slot()
    def do_nziz(self):
        print("NZIZ started")
        self.change_button_state(self.NZIZbutton, self.NZIZbutton_state)
        self.matlab_signal.signal_int.emit(1)
        print("Spawn thread succesful")

    @Slot()
    def do_circum(self):
        self.change_button_state(self.Circumbutton, self.NZIZbutton_state)
        print("Circum started")

    @Slot()
    def do_ear_to_ear(self):
        self.change_button_state(self.EartoearButton, self.EartoEarutton_state)
        print("Ear 2 Ear started")
    
    @Slot()
    def predict_eeg_positions(self):
        print("Tryna predict eeg positions")

    def change_button_state(self, button, button_state):
        button_state = not button_state # this is somehow legal?
        print(self.NZIZbutton_state)
        print(self.Circumbutton_state)
        print(self.EartoEarutton_state)
        if (self.NZIZbutton_state or self.Circumbutton_state or self.EartoEarutton_state):
            self.is_recording_flag = True # If any of the state is True that means its recording
        else:
            self.is_recording_flag = False # else its not
        
        print("The recording state is ..", self.is_recording_flag)
        if (self.is_recording_flag is False):
            print("Button state going to change!")
            button.setText('Stop!')
            button.setStyleSheet('QPushButton {background-color: light gray; color: red;}')
        else:
            print("You cant do any recording till you stop the current recording!")

