# Import matlab engine
# import matlab.engine

# Import standard python lib
import numpy as np
import sys
import ctypes
import math
import numpy
from argparse import ArgumentParser, RawTextHelpFormatter

# Import pyside6lib
from PySide6.QtDataVisualization import (Q3DBars, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QValue3DAxis)
from PySide6.QtCore import QCoreApplication, Signal, SIGNAL, SLOT, Qt, QSize, QPointF
from PySide6.QtGui import (QVector3D, QOpenGLFunctions,
    QMatrix4x4, QOpenGLContext, QSurfaceFormat, QGuiApplication)
from PySide6.QtWidgets import (QApplication, QWidget, QMessageBox, QHBoxLayout,
    QSlider, QSizePolicy, QMainWindow)

# Import pyside6 qt opengl stuff
from PySide6.QtOpenGL import (QOpenGLVertexArrayObject, QOpenGLBuffer,
    QOpenGLShaderProgram, QOpenGLShader)
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from shiboken6 import VoidPtr

# Import matlab engine stuff
# eng = matlab.engine.start_matlab()
# print("Calling matlab function...")
# eng.triarea(nargout=0)
# print("Finished!")

def data_to_bar_data_row(data):
    return list(QBarDataItem(d) for d in data)


def data_to_bar_data_array(data):
    return list(data_to_bar_data_row(row) for row in data)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Qt test')

        # Set axis stuff
        self._column_axis = QCategory3DAxis()
        self._column_axis.setTitle('Columns')
        self._column_axis.setTitleVisible(True)
        self._column_axis.setLabels(['Column1', 'Column2'])
        self._column_axis.setLabelAutoRotation(30)

        self._row_axis = QCategory3DAxis()
        self._row_axis.setTitle('Rows')
        self._row_axis.setTitleVisible(True)
        self._row_axis.setLabels(['Row1', 'Row2'])
        self._row_axis.setLabelAutoRotation(30)

        self._value_axis = QValue3DAxis()
        self._value_axis.setTitle('Values')
        self._value_axis.setTitleVisible(True)
        self._value_axis.setRange(0, 5)

        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

