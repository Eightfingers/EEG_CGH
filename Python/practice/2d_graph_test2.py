import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import QChart, QChartView, QScatterSeries, QValueAxis


class TestChart(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.series = QScatterSeries()
        self.series.append(0, 0)
        self.series.append(2, 4)
        self.series.append(3, 8)

        self.chart = QChart()
        self.chart.createDefaultAxes()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.setAxisX(self.axisX)
        self.chart.setAxisY(self.axisY)

        self.chart.setTitle("Simple Scatter chart test")

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self._chart_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestChart()
    window.show()
    window.resize(440, 300)
    sys.exit(app.exec())