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
import matlab.engine
from matlab_thread import MatlabMainThread

class StatusWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # store the format of the layout
        self._layout = parent.status_layout
        self.matlab_label = "Matlab: "
        self.optitrack_label = "Optitrack: "
        self.wand_label = "Stylus: "
        self.specs_label = "Specs: "

        # Create placeholder labels
        self.matlab_qlabel = QLabel(self.matlab_label)
        self.optitrack_qlabel = QLabel(self.optitrack_label)
        self.wand_qlabel = QLabel(self.wand_label)
        self.specs_qlabel = QLabel(self.specs_label)

        self._layout.addWidget(self.matlab_qlabel)
        self._layout.addWidget(self.optitrack_qlabel)
        self._layout.addWidget(self.wand_qlabel)
        self._layout.addWidget(self.specs_qlabel)
        self._layout.addStretch()   

    @Slot(list)
    def change_label(self,message):
        self.label = message[0]
        self.status = message[1]
        
        if self.label == "Matlab":
            self.matlab_qlabel.setText(self.matlab_label + self.status)
        elif self.label == "Optitrack" :
            self.optitrack_qlabel.setText(self.optitrack_label + self.status) 
        elif self.label == "Stylus" :
            self.wand_qlabel.setText(self.wand_label + self.status) 
        elif self.label == "Specs" :
            self.specs_qlabel.setText(self.specs_label + self.status) 

