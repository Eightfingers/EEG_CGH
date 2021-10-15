import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot)
from PySide6.QtGui import QGuiApplication, QVector3D
from PySide6.QtWidgets import (QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget,
                                QSizePolicy, QSlider, QLabel)
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)
import numpy as np

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

        # Main central widget
        self.scatter = Q3DScatter()
        self.scatter_series = QScatter3DSeries()
        self.container = QWidget.createWindowContainer(self.scatter)
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.container.setMinimumSize(size, size)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        self.setCentralWidget(self.container)

        # Create left dockable window widget
        self.docked = QDockWidget("Menu", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.docked)

        # Create a a parent widget to handle button widgets??
        self.docked_parent_widget = QWidget(self)
        self.docked.setWidget(self.docked_parent_widget)
        self.docked_parent_widget.setLayout(QVBoxLayout()) # set the layout of parent widget

        # Create Button widget
        self.button = QPushButton("Randomize the graph!")
        self.button.clicked.connect(self.start_thread) # start a thread when the button is clicked

        # Create a placeholder button to show QVBoxLayout
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")

        # Add the button widget to the docked window
        self.widget = QWidget()
        self.docked_parent_widget.layout().addWidget(self.button)
        self.docked_parent_widget.layout().addWidget(self.button2)
        self.docked_parent_widget.layout().addWidget(self.button3)

        self.axisMinSliderX = QSlider(Qt.Horizontal, self.widget)
        self.axisMinSliderX.setMinimum(0)
        self.axisMinSliderX.setTickInterval(1)
        self.axisMinSliderX.setEnabled(True)
        self.axisMaxSliderX = QSlider(Qt.Horizontal, self.widget)
        self.axisMaxSliderX.setMinimum(1)
        self.axisMaxSliderX.setTickInterval(1)
        self.axisMaxSliderX.setEnabled(True)

        self.axisMinSliderZ = QSlider(Qt.Horizontal, self.widget)
        self.axisMinSliderZ.setMinimum(0)
        self.axisMinSliderZ.setTickInterval(1)
        self.axisMinSliderZ.setEnabled(True)
        self.axisMaxSliderZ = QSlider(Qt.Horizontal, self.widget)
        self.axisMaxSliderZ.setMinimum(1)
        self.axisMaxSliderZ.setTickInterval(1)
        self.axisMaxSliderZ.setEnabled(True)

        # self.docked_parent_widget.layout().addWidget(QLabel("Column range"))
        # self.docked_parent_widget.layout().addWidget(QLabel("Min range"))
        # self.docked_parent_widget.layout().addWidget(self.axisMinSliderX)
        # self.docked_parent_widget.layout().addWidget(QLabel("Max range"))
        # self.docked_parent_widget.layout().addWidget(self.axisMaxSliderX)
        # self.docked_parent_widget.layout().addWidget(QLabel("Row range"))
        # self.docked_parent_widget.layout().addWidget(QLabel("Min range"))
        # self.docked_parent_widget.layout().addWidget(self.axisMinSliderZ)
        # self.docked_parent_widget.layout().addWidget(QLabel("Max range"))
        # self.docked_parent_widget.layout().addWidget(self.axisMaxSliderZ)

        self.axisMinSliderX.valueChanged.connect(self.adjustXMin)
        self.axisMaxSliderX.valueChanged.connect(self.adjustXMax)
        self.axisMinSliderZ.valueChanged.connect(self.adjustZMin)
        self.axisMaxSliderZ.valueChanged.connect(self.adjustZMax)

        minimum = -150
        maximum = 150
        self.scatter.axisX().setRange(minimum, maximum)
        self.scatter.axisX().setSubSegmentCount(2)
        self.scatter.axisX().setSegmentCount(8)
        self.scatter.axisX().setTitle('X')
        self.scatter.axisY().setRange(minimum, maximum)
        self.scatter.axisY().setSegmentCount(8)
        self.scatter.axisY().setSubSegmentCount(2)
        self.scatter.axisY().setTitle('Y')
        self.scatter.axisZ().setRange(minimum, maximum)
        self.scatter.axisZ().setSegmentCount(8)
        self.scatter.axisZ().setSubSegmentCount(2)
        self.scatter.axisZ().setTitle('Z')

        self.m_stepX = 0.05
        self.m_stepZ = 0.05
        self.m_rangeMinX = -8
        self.m_rangeMinZ = -8

        self.m_axisMinSliderX = QSlider()
        self.m_axisMaxSliderX = QSlider()
        self.m_axisMinSliderZ = QSlider()
        self.m_axisMaxSliderZ = QSlider()

    def adjustXMin(self, minimum):
        minX = self.m_stepX * float(minimum) + self.m_rangeMinX

        maximum = self.m_axisMaxSliderX.value()
        if minimum >= maximum:
            maximum = minimum + 1
            self.m_axisMaxSliderX.setValue(maximum)
        maxX = self.m_stepX * maximum + self.m_rangeMinX

        self.setAxisXRange(minX, maxX)

    def adjustXMax(self, maximum):
        maxX = self.m_stepX * float(maximum) + self.m_rangeMinX

        minimum = self.m_axisMinSliderX.value()
        if maximum <= minimum:
            minimum = maximum - 1
            self.m_axisMinSliderX.setValue(minimum)
        minX = self.m_stepX * minimum + self.m_rangeMinX

        self.setAxisXRange(minX, maxX)

    def adjustZMin(self, minimum):
        minZ = self.m_stepZ * float(minimum) + self.m_rangeMinZ

        maximum = self.m_axisMaxSliderZ.value()
        if minimum >= maximum:
            maximum = minimum + 1
            self.m_axisMaxSliderZ.setValue(maximum)
        maxZ = self.m_stepZ * maximum + self.m_rangeMinZ

        self.setAxisZRange(minZ, maxZ)

    def adjustZMax(self, maximum):
        maxX = self.m_stepZ * float(maximum) + self.m_rangeMinZ

        minimum = self.m_axisMinSliderZ.value()
        if maximum <= minimum:
            minimum = maximum - 1
            self.m_axisMinSliderZ.setValue(minimum)
        minX = self.m_stepZ * minimum + self.m_rangeMinZ

        self.setAxisZRange(minX, maxX)

    def setAxisXRange(self, minimum, maximum):
        self.scatter.axisX().setRange(minimum, maximum)

    def setAxisZRange(self, minimum, maximum):
        self.scatter.axisZ().setRange(minimum, maximum)

    def start_thread(self):
        instanced_thread = UpdateDataThread(self)
        instanced_thread.start()

    # Create the Slots that will receive signals from the worker Thread
    @Slot(np.ndarray)
    def update_and_add_scatter(self, message):
        print("signal recieved")
        self.add_list_to_scatterdata(self.scatter_series, message)
        self.scatter.addSeries(self.scatter_series)
        self.scatter.show()

    def add_list_to_scatterdata(self, scatter_series, data):
        for d in data:
            scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[1], d[2])))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
