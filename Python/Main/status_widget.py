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

# Signals must inherit QObject
class ScatterSignal(QObject):
    # Create a Signal class to contain signal data types
    signal_np = Signal(np.ndarray)

class UpdateDataThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self.signals = ScatterSignal()
        self.signals.signal_np.connect(parent.update_and_add_scatter)
        print("Update data worker called")

    # This stop function is not used in this example
    def stop(self):
        print("Stopped called")

    def run(self):
        random_coordinates = np.random.randint(0, 100, size=(10, 3)) 
        # Emit signals whenever you want (print to command line)
        self.signals.signal_np.emit(random_coordinates) 
        print("signalemited")

class MenuWidget(QWidget):

    def __init__(self, layout, scatter, scatter_series):
        # super(MenuWidget, self).__init__()

        self._layout = layout
        self._scatter = scatter
        self._scatter_series = scatter_series

        # Create Button widget
        self.button = QPushButton("Randomize the graph!")
        self.button.clicked.connect(self.start_thread) # start a thread when the button is clicked

        # Create placeholder buttons 
        self.button2 = QPushButton("Button 2")
        self.button2.clicked.connect(self.change_label) # start a thread when the button is clicked
        self.button3 = QPushButton("Button 3")
        # Create placeholder labels
        self.label = QLabel("Lol")
        self.label2 = QLabel("Lulz")

        self._layout.addStretch()
        self._layout.addWidget(self.button)
        self._layout.addWidget(self.button2)
        self._layout.addWidget(self.button3)
        self._layout.addWidget(self.label)
        self._layout.addWidget(self.label2)
        self._layout.addStretch()

        # set the layout of the menu
        self.setLayout(self._layout)

    def start_thread(self):
        instanced_thread = UpdateDataThread(self)
        instanced_thread.start()

    # Create the Slots that will receive signals from the worker Thread
    @Slot(np.ndarray)
    def update_and_add_scatter(self, message):
        print("signal recieved")
        self.add_list_to_scatterdata(self._scatter_series, message)
        self._scatter.addSeries(self._scatter_series)
        self._scatter.show()
    
    @Slot()
    def change_label(self,message):
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.label.setText(random.choice(self.hello))

    def add_list_to_scatterdata(self, scatter_series, data):
        for d in data:
            scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[1], d[2])))