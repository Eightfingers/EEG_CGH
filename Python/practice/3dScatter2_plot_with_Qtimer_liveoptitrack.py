import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread,
                            QWaitCondition, QTimer)
from PySide6.QtGui import QGuiApplication, QVector3D, QColor
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem, QScatter3DSeries,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)
import numpy as np

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Qt DataVisualization 3D scatter')
        self.green_qcolor = QColor(0, 255, 0)

        self.series2 = self.create_new_scatter_series(self.green_qcolor)

        self.scatter = Q3DScatter()
        self.scatter_series = QScatter3DSeries()
        self.scatter_series.setBaseColor(QColor(255, 0, 0))

        self.y_axis = QValue3DAxis()
        self.y_axis.setTitle('Y')
        self.y_axis.setTitleVisible(True)    

        self.z_axis = QValue3DAxis()
        self.z_axis.setTitle('Z')
        self.z_axis.setTitleVisible(True)

        # Set the axis properties
        segment_count = 8
        sub_segment_count = 2
        axis_minimum = -0.8
        axis_maximum = 0.8

        self.axis = self.create_axis("Hello world", segment_count, sub_segment_count, axis_minimum, axis_maximum)
        self.scatter.setAxisX(self.axis)
        self.scatter.setAxisY(self.y_axis)
        self.scatter.setAxisZ(self.z_axis)

        # create 10000 random spatial positions 
        self.coordinates = np.array([[10,10,10], [0,0,0]])
        self.add_list_to_scatterdata(self.scatter_series, self.coordinates)
        self.scatter.addSeries(self.scatter_series)
        self.container = QWidget.createWindowContainer(self.scatter)
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.container.setMinimumSize(size, size)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        
        self.setCentralWidget(self.container)

        if (self.scatter_series.dataProxy().itemCount() != 0 ):
            print("The number of items is.. ", self.scatter_series.dataProxy().itemCount())
            # kekw = self.scatter_series.dataProxy().array() # this will crash the app
            # print(kekw)

        if (self.scatter_series.dataProxy().itemCount() != 0 ):
            pass

        # self.scatter_series.dataProxy().resetArray(QScatter3DSeries())
        
        # set starting position of camera
        camera = self.scatter.scene().activeCamera()
        camera.setYRotation(25)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(100)

    def update_plot_data(self):
        self.scatter.removeSeries(self.series2) # remove the old position
        self.series2.dataProxy().removeItems(0,3) # remove 3 items, starting from the first position
        self.coordinates = np.random.randint(0, 100, size=(3, 3)) 
        self.add_list_to_scatterdata(self.series2, self.coordinates)
        self.scatter.addSeries(self.series2)
        self.scatter.show()

    def add_list_to_scatterdata(self, scatter_series, data):
        for d in data:
            scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[1], d[2])))

    def create_new_scatter_series(self, colour):
        scatter_series_new_series = QScatter3DSeries()
        scatter_series_new_series.setBaseColor(colour)

        return scatter_series_new_series

    def create_axis(self, title, segment_count, sub_segment_count, axis_min, axis_max):
        new_axis = QValue3DAxis()
        new_axis.setTitle(title)
        new_axis.setTitleVisible(True)
        new_axis.setSegmentCount(segment_count)
        new_axis.setRange(axis_min, axis_max)
        new_axis.setSubSegmentCount(sub_segment_count)

        return new_axis


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
