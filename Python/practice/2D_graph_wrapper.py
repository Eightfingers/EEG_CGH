import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread,
                            QWaitCondition, QTimer)
from PySide6.QtGui import QGuiApplication, QVector3D, QColor
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)
import numpy as np
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
import os

# Adapted from https://www.pythonguis.com/tutorials/plotting-pyqtgraph/ the tutorial on updating data
# pyQtgraph docs https://pyqtgraph.readthedocs.io/en/latest/index.html 

class MainWindow(QMainWindow):

    def __init__(self):
        
        self.NZIZscatter_series_x = np.array([1])
        self.NZIZscatter_series_y = np.array([2])
        self.CIRCUMscatter_series_x = None
        self.CIRCUMscatter_series_y = None
        self.EarToEarscatter_series_x = None
        self.EarToEarscatter_series_y = None
        self.Predicted21_series_x = None
        self.Predicted21_series_y = None
        self.electrode_markers_series_x = None
        self.electrode_markers_series_y = None
        self.specs_series_x = None
        self.specs_series_y = None
        self.stylus_position_series_x = None
        self.stylus_position_series_y = None

        super().__init__()


        self.reflective_markers_series = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.orange_qcolor))
        self.reflective_marker_in_eeg_position = self.create_new_scatter_series(self.green_qcolor, self.marker_size) # reflective marker in eeg position


        self.setWindowTitle('Qt DataVisualization 2D scatter')
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.plotItem.setTitle("2D view")
        self.setCentralWidget(self.graphWidget)
        

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        self.data_line = self.graphWidget.plot(self.x, self.y, pen=None, symbolBrush=('r'))

        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
