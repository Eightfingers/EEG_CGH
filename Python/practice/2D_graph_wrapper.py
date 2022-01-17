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
        super().__init__()

        self.setWindowTitle('Qt DataVisualization 2D scatter')
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.plotItem.setTitle("2D view")
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0), style=Qt.DashLine)
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen, symbol='+', symbolBrush=('b'))

        self.timer = QTimer()
        self.timer.setInterval(50)
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
