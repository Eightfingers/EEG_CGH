import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot, QSize)
from PySide6.QtGui import QGuiApplication, QVector3D, QColor
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

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('Qt DataVisualization 3D random scatter')

        self.scatter = Q3DScatter()
        self.scatter_series = QScatter3DSeries()
        # Main central widget
        self.container = QWidget.createWindowContainer(self.scatter)
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.container.setMinimumSize(size, size)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        self.setCentralWidget(self.container)

        # Create left dockable window widget
        self.left_dock = QDockWidget("Menu", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)

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

        # Create a a parent widget to handle button widgets??
        self.docked_parent_widget = QWidget()

        # Set layout properties
        self.docked_layout = QVBoxLayout()

        # self.docked_layout_widget.setAlignment(Qt.AlignTop) # align top
        self.docked_layout.addStretch() # looks like a hack but this is to centralize the widgets 
        self.docked_layout.addWidget(self.button)
        self.docked_layout.addWidget(self.button2)
        self.docked_layout.addWidget(self.button3)
        self.docked_layout.addWidget(self.label)
        self.docked_layout.addWidget(self.label2)
        self.docked_layout.addStretch() # looks like a hack but this is to centralize the widgets

        self.docked_parent_widget.setLayout(self.docked_layout) # set the layout of the parent widget
        self.left_dock.setWidget(self.docked_parent_widget) # now add the widget into the dock

        # self.docked_parent_widget.setLayout(QBoxLayout(QBoxLayout.TopToBottom)) # This layout arranges the widget position from top to bottom

        self.random_coordinates = np.random.randint(0, 100, size=(10, 3)) 
        self.add_list_to_scatterdata(self.scatter_series, self.random_coordinates)
        self.scatter.addSeries(self.scatter_series)
        self.scatter.show()

    def start_thread(self):
        instanced_thread = UpdateDataThread(self)
        instanced_thread.start()

    # Create the Slots that will receive signals from the worker Thread
    @Slot(np.ndarray)
    def update_and_add_scatter(self, message):
        print("signal recieved")

        # self.scatter.removeSeries(self.scatter_series) # remove the old position
        # self.scatter_series = self.reset_scatter_series(QColor(0, 0, 0))

        # self.scatter_series = QScatter3DSeries() # create a new series at every instance
        # self.scatter_series.setBaseColor(QColor(0, 0, 0)) # Black
        # self.scatter_series.setItemSize(0.5)

        self.scatter_series.dataProxy().removeItems(0,self.scatter_series.dataProxy().itemCount())
        self.add_list_to_scatterdata(self.scatter_series, message)
        
        self.scatter.show()
    
    @Slot()
    def change_label(self,message):
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.label.setText(random.choice(self.hello))

    def add_list_to_scatterdata(self, scatter_series, data):
        for d in data:
            scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[1], d[2])))

    def reset_scatter_series(self, colour):
        self.scatter_series_new_series = QScatter3DSeries()
        self.scatter_series_new_series.setBaseColor(colour)
        self.scatter_series_new_series.setItemSize(0.5)

        return self.scatter_series_new_series


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())