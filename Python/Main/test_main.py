import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot, QSize)
from PySide6.QtGui import QGuiApplication, QVector3D, QColor
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QLabel, QBoxLayout
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem, QAbstract3DGraph,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)
import numpy as np
from matlab_thread import MatlabMainThread
from menu_widget import MenuWidget
from status_widget import StatusWidget
from optitrack_thread import OptitrackMainThread

from scipy.spatial.transform import Rotation as R

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('CGH EEG Optitrack Assisted EEG localization')

        # Used to be shown
        self.scatter = Q3DScatter()
        self.NZIZscatter_series = QScatter3DSeries()
        self.CIRCUMscatter_series = QScatter3DSeries()
        self.EarToEarscatter_series = QScatter3DSeries()

        # Unfortunately, i think to access the array data that has been added QScatter3DSeries()
        # is buggy, it just crashes the app. Below is just a quick remedy by having a seperate 
        # variables to store all the array data.

        self.NZIZ_data = None
        self.NZIZ_specs_data = None
        self.CIRCUM_data = None
        self.CIRCUM_specs_data = None
        self.EarToEar_data = None
        self.EarToEar_specs_data = None

        self.NZIZscatter_series.setBaseColor(QColor(255, 0, 0)) # Red for NZIZ trace 
        self.CIRCUMscatter_series.setBaseColor(QColor(0, 255, 0)) # Green for Circumference trace
        self.EarToEarscatter_series.setBaseColor(QColor(0, 0, 255)) # Blue for Ear to Ear trace

        # Set the axis 
        self.x_axis = QValue3DAxis()
        self.x_axis.setTitle('X')
        self.x_axis.setTitleVisible(True)

        self.y_axis = QValue3DAxis()
        self.y_axis.setTitle('Y')
        self.y_axis.setTitleVisible(True)    

        self.z_axis = QValue3DAxis()
        self.z_axis.setTitle('Z')
        self.z_axis.setTitleVisible(True)

        self.scatter.setAxisX(self.x_axis)
        self.scatter.setAxisY(self.y_axis)
        self.scatter.setAxisZ(self.z_axis)

        # Set no Shadow
        self.scatter.setShadowQuality(QAbstract3DGraph.ShadowQualityNone)

        # Main central widget
        self.graph = QWidget.createWindowContainer(self.scatter)
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.graph.setMinimumSize(size, size)
        self.graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.graph.setFocusPolicy(Qt.StrongFocus)
        self.setCentralWidget(self.graph)

        # Create left dockable window widget
        self.left_dock = QDockWidget("Menu", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)

        # Create a dummy widget as the main dock widget
        self.left_dock_main_widget = QWidget()

        # Main layout of the left main dockable widget
        self.left_dock_main_layout = QVBoxLayout()

        # Layout of the widgets inside the dockable widgets
        self.menu_layout = QVBoxLayout()
        self.status_layout = QVBoxLayout()

        # Some comments (might be wrong! not a QT/ Python expert)
        # This is logically isn't too right? Because even though I created a new MenuWidget, I am not using the layout in the widget 
        # object at all. I am just passing self.menu_layout parameter to it and then reusing that self.menu_layout paremeter. 
        # I did it this way because I want to have a more seperate codes for the contents in the dock widget and have a more 
        # neat code layout. I realize QT doesn't allow nesting widgets inside widgets. And layouts and widgets are 2 seperate entities.
        self.left_dock_status_widget = StatusWidget(self)
        self.left_dock_main_layout.addLayout(self.status_layout)
        
        self.left_dock_menu_widget = MenuWidget(self)
        self.left_dock_main_layout.addLayout(self.menu_layout)

        self.left_dock_main_widget.setLayout(self.left_dock_main_layout)
        self.left_dock.setWidget(self.left_dock_main_widget)

        # Start the main thread
        self.matlab_main_thread = MatlabMainThread(self)
        self.matlab_main_thread.start()

        # Start the Optitrack Thread
        # self.optitrack_main_thread = OptitrackMainThread(self)
        # self.optitrack_main_thread.start()  
        
        # Now connect and initialize the Signals in the MenuWidget with the threads
        self.left_dock_menu_widget.connect_matlab_signals(self.matlab_main_thread)
        # self.left_dock_menu_widget.connect_optitrack_signals(self.optitrack_main_thread)

    @Slot()
    def clear_data(self):
        self.scatter.removeSeries(self.NZIZscatter_series)
        self.scatter.removeSeries(self.CIRCUMscatter_series)
        self.scatter.removeSeries(self.EarToEarscatter_series)

        # Reset the series. I Couldn't really figure out the method in the python function. Hope this will do for now
        self.NZIZscatter_series = QScatter3DSeries()
        self.CIRCUMscatter_series = QScatter3DSeries()
        self.EarToEarscatter_series = QScatter3DSeries()

        self.NZIZscatter_series.setBaseColor(QColor(255, 0, 0)) # Red for NZIZ trace 
        self.CIRCUMscatter_series.setBaseColor(QColor(0, 255, 0)) # Green for Circumference trace
        self.EarToEarscatter_series.setBaseColor(QColor(0, 0, 255)) # Blue for Ear to Ear trace

    # Create the Slots that will receive signals from the worker Thread
    @Slot(np.ndarray)
    def update_and_add_scatterNZIZ(self, message):
        self.add_list_to_scatterdata(self.NZIZscatter_series, message)
        self.scatter.addSeries(self.NZIZscatter_series)
        self.scatter.show()

    # Create the Slots that will receive signals from the worker Thread
    @Slot(np.ndarray)
    def show_nziz_positions(self, message):
        print(message)
        self.add_list_to_scatterdata_z_y_swapped(self.NZIZscatter_series, message)
        self.scatter.addSeries(self.NZIZscatter_series)
        self.scatter.show()

    @Slot(np.ndarray)
    def update_and_add_scatterCIRCUM(self, message):
        self.add_list_to_scatterdata(self.CIRCUMscatter_series, message)
        self.scatter.addSeries(self.CIRCUMscatter_series)
        self.scatter.show()

    @Slot(np.ndarray)
    def update_and_add_scatterEarToEar(self, message):
        self.add_list_to_scatterdata(self.EarToEarscatter_series, message)
        self.scatter.addSeries(self.EarToEarscatter_series)
        self.scatter.show()

    def add_list_to_scatterdata(self, scatter_series, data):
        if data.ndim == 1:
            scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(data[0], data[1], data[2])))
        else:
            for d in data:
                scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[1], d[2])))

    def add_list_to_scatterdata_z_y_swapped(self, scatter_series, data):
        if data.ndim == 1:
            scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(data[0], data[2], data[1])))
        else:
            for d in data:
                scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[2], d[1])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())