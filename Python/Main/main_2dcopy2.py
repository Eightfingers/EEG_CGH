"""PySide6 port of the Chart Themes example from Qt v5.x"""

import sys
from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPalette
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizePolicy,
    QWidget)
from PySide6.QtCharts import (QAreaSeries, QBarSet, QChart, QChartView,
                              QLineSeries, QPieSeries, QScatterSeries,
                              QSplineSeries, QStackedBarSeries, QValueAxis)

import numpy as np

# from ui_themewidgetcopy2 import Ui_ThemeWidgetForm as ui

from random import random, uniform

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('CGH EEG Optitrack Assisted EEG localization')

        self.main_chart = QChart()  
        self.main_chart.setTitle("Scatter Top 2D View")

        # Colours used for the graphs
        self.red_qcolor = QColor(255, 0, 0)
        self.marker_size = 10

        # Each of this series is used to represent data on the graph
        self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.marker_size)
        self.NZIZscatter_series.setName("NZIZ")
        self.coordinates = 5 * np.random.random_sample((3, 2))
        print(self.coordinates)

        # self.add_list_to_series_data2D(self.NZIZscatter_series, self.coordinates)
        self.NZIZscatter_series.append(5, 5)

        print(self.NZIZscatter_series.points())

        self.main_chart.addSeries(self.NZIZscatter_series)
        self.main_chart.setTitle("2D Scatter plot")

        # # Axis
        # self.main_chart.createDefaultAxes()
        self.axisX = QValueAxis()
        self.axisX.setTickCount(10)
        self.axisX.setMin(-10)
        self.axisX.setMax(10)
        self.axisX.setTitleText("X")

        self.axisY = QValueAxis()
        self.axisY.setTickCount(10)
        self.axisY.setMin(-10)
        self.axisY.setMax(10)
        self.axisY.setTitleText("Y")
        self.main_chart.addAxis(self.axisX, Qt.AlignBottom)
        self.main_chart.addAxis(self.axisY, Qt.AlignLeft)

        self._chart_view = QChartView(self.main_chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self._chart_view)

        # self.timer = QTimer()
        # self.timer.setInterval(10)
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

    # def update_plot_data(self):
        # self.NZIZscatter_series.clear()

    def create_new_scatter_series(self, colour, size):
        chart_series_new_series = QScatterSeries()
        chart_series_new_series.setColor(colour)
        chart_series_new_series.setMarkerSize(size)

        return chart_series_new_series

    def add_list_to_series_data2D(self,scatter_series, data):
    # if type(data) == np.ndarray:
        if data.ndim == 1: # its a single dimensional array
            x = np.array([data[0]])
            y = np.array([data[1]]) 
            scatter_series.append(data[0], data[1])
        else:
            for d in data:
                print("d[0] is, ", d[0], " d[1] is ", d[1])
                scatter_series.append(d[0], d[1])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    window.resize(440, 300)
    sys.exit(app.exec())