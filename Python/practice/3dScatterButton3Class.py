import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot, QSize)
from PySide6.QtGui import QGuiApplication, QVector3D
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QLabel, QBoxLayout 
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)
import numpy as np
import random
from menu_widget import MenuWidget
from status_widget import StatusWidget

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('Qt DataVisualization 3D random scatter')

        self.scatter = Q3DScatter()
        self.scatter_series = QScatter3DSeries()

        # Main central widget
        self.container = QWidget.createWindowContainer(self.scatter)
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.container.setMinimumSize(size, size)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        self.setCentralWidget(self.container)

        # Create left dockable window widget
        self.left_dock = QDockWidget("Menu", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)


        # Create a dummy widget as the main dock widget
        self.left_dock_main_widget = QWidget()

        # Main layout of the left dockable widget
        self.left_dock_layout = QVBoxLayout()

        # Layout of the widgets inside the dockable widgets
        self.menu_layout = QVBoxLayout()
        self.status_layout = QVBoxLayout()

        self.left_dock_menu_widget = MenuWidget(self)
        self.left_dock_layout.addLayout(self.menu_layout)

        self.left_dock_status_widget = StatusWidget(self)
        self.left_dock_layout.addLayout(self.status_layout)

        self.left_dock_main_widget.setLayout(self.left_dock_layout)

        self.left_dock.setWidget(self.left_dock_main_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())