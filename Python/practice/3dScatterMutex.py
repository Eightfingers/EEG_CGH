import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot)
from PySide6.QtGui import QGuiApplication, QVector3D
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget
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

    # This stun function is not called
    def stop(self):
        print("Stopped called")

    def run(self):
        random_coordinates = np.random.randint(0, 100, size=(10, 3)) 
        # Emit signals whenever you want (print to command line)
        self.signals.signal_np.emit(random_coordinates) 
        print("signalemited")

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)

        self.setWindowTitle('Qt DataVisualization 3D random scatter')
        
        self.scatter = Q3DScatter()
        self.scatter_series = QScatter3DSeries()
        
        self.button = QPushButton("Randomized the graph!")
        self.button.clicked.connect(self.start_thread) # start a thread when the button is clicked

        self.container = QWidget.createWindowContainer(self.scatter)
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.container.setMinimumSize(size, size)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        self.setCentralWidget(self.container)

        # self.dock = QDockWidget(self.container)
        # self.dockWidgetArea = 10
        # self.dock.setWidget(self.button)

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
