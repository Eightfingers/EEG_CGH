import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot, QSize)
from PySide6.QtGui import QGuiApplication, QVector3D
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QLabel, QBoxLayout 
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)
import numpy as np
from matlab_thread import MatlabMainThread
from menu_widget import MenuWidget
from status_widget import StatusWidget

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('CGH EEG Optitrack Assisted EEG localization')

        self.nziz_data = None
        self.circum_data = None
        self.eartoear_data = None

        self.nziz_data_specs = None
        self.circum_data_specs = None
        self.eartoear_data_specs = None

        self.scatter = Q3DScatter()
        self.scatter_series = QScatter3DSeries()

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
        self.left_dock_menu_widget = MenuWidget(self.menu_layout, self.scatter, self.scatter_series, self)
        self.left_dock_main_layout.addLayout(self.menu_layout)

        self.left_dock_status_widget = StatusWidget(self.status_layout, self)
        self.left_dock_main_layout.addLayout(self.status_layout)

        self.left_dock_main_widget.setLayout(self.left_dock_main_layout)
        self.left_dock.setWidget(self.left_dock_main_widget)

        # Start the main thread
        self.matlab_main_thread = MatlabMainThread(self.left_dock_status_widget, self.left_dock_menu_widget)
        self.matlab_main_thread.start()

        # Now connect the Signals in the MenuWidget to the matlab_thread main
        self.left_dock_menu_widget.connect_matlab_signals(self.matlab_main_thread)

    # Create the Slots that will receive signals from the worker Thread
    @Slot(np.ndarray)
    def update_and_add_scatter(self, message):
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