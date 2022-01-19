"""PySide6 port of the linechart example from Qt v5.x"""

import sys
from PySide6.QtCore import QPointF, QSize, QStringConverter, Qt, QTimer
from PySide6.QtGui import QGuiApplication, QVector3D, QColor, QPainter
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import QAbstractAxis, QCategoryAxis, QChart, QChartView, QLegend, QScatterSeries, QValueAxis, QBarCategoryAxis
import numpy as np


class TestChart(QMainWindow):
    def __init__(self):
        super().__init__()

        # Colours used for the graphs
        self.red_qcolor = QColor(255, 0, 0)
        self.green_qcolor = QColor(0, 255, 0)
        self.blue_qcolor = QColor(0, 0, 255)
        self.yellow_qcolor = QColor(255, 255, 0)
        self.orange_qcolor = QColor(255, 165, 0)
        self.black_qcolor = QColor(0, 0 ,0)
        self.grey_qcolor = QColor(128,128,128)

        self.series = self.create_new_scatter_series(self.red_qcolor, 10)
        # self.series = QScatterSeries()
        self.series.setName("Lmfao2")
        self.coordinates = np.random.randint(0, 100, size=(100, 3)) 
        self.add_list_to_scatterdata(self.series, self.coordinates)


        self.chart = QChart()
        self.axisX = QValueAxis()
        self.axisX.setRange(-10,10)
        self.axisX.setTitleText("X")

        self.chart.addSeries(self.series)
        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.setTitle("Simple line chart example")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)
        self.chart.show()

        self.series2 = self.create_new_scatter_series(self.green_qcolor, 10)
        # self.series = QScatterSeries()
        self.series2.setName("Lmfao")
        self.coordinates = np.random.randint(0, 100, size=(100, 3)) 
        self.add_list_to_scatterdata(self.series2, self.coordinates)
        self.chart.addSeries(self.series2)
        self.chart.show()

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self._chart_view)

        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.chart.removeSeries(self.series2)
        self.series2 = self.create_new_scatter_series(self.green_qcolor, 10)
        self.coordinates = np.random.randint(0, 100, size=(3, 3)) 
        self.add_list_to_scatterdata(self.series2, self.coordinates)
        self.chart.addSeries(self.series2)
        self.chart.show()

    def add_list_to_scatterdata(self,scatter_series, data):
        print(type(data))
        print(data)
        for d in data:
            print(type(d))
            print(type(d[0]))
            scatter_series.append(d[0], d[1])

    def create_new_scatter_series(self, colour, size):
        self.scatter_series_new_series = QScatterSeries()
        self.scatter_series_new_series.setColor(colour)
        self.scatter_series_new_series.setMarkerSize(size)

        return self.scatter_series_new_series


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestChart()
    window.show()
    window.resize(440, 300)
    sys.exit(app.exec())