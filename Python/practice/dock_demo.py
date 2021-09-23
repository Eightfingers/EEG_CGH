import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot)
from PySide6.QtGui import QGuiApplication, QVector3D
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QTextEdit
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)
import numpy as np

class DockDemo(QMainWindow):
    def __init__(self, parent=None):
        super(DockDemo, self).__init__(parent)
        self.setCentralWidget(QTextEdit())

        self.docked = QDockWidget("Dockable", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.docked)
        self.dockedWidget = QWidget(self)
        self.docked.setWidget(self.dockedWidget)
        self.setWindowTitle("Dock demo")
        self.dockedWidget.setLayout(QVBoxLayout())
        for i in range(5):
            self.dockedWidget.layout().addWidget(QPushButton("{}".format(i)))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = DockDemo()
    ex.show()
    sys.exit(app.exec_())