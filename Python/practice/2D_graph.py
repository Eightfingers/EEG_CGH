"""PySide6 port of the linechart example from Qt v5.x"""

import sys
from PySide6.QtCore import QPointF, QSize, QStringConverter, Qt
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

        self.series = self.create_new_scatter_series(self.red_qcolor, 1)
        self.series = QScatterSeries()
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

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self._chart_view)


    def add_list_to_scatterdata(self,scatter_series, data):
        for d in data:
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