import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QPointF, QSize, QStringConverter, Qt, Slot, QTimer
from PySide6.QtGui import QGuiApplication, QVector3D, QColor, QPainter
from PySide6.QtWidgets import QBoxLayout, QDockWidget, QHBoxLayout, QMainWindow, QApplication, QSizePolicy, QVBoxLayout, QWidget
from PySide6.QtCharts import QAbstractAxis, QCategoryAxis, QChart, QChartView, QLegend, QScatterSeries, QValueAxis, QBarCategoryAxis
import numpy as np
from menu_widget import MenuWidget
from status_widget import StatusWidget
# from optitrack_thread import OptitrackMainThread
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import random 

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlim([-6, 6])
        self.axes.set_ylim([-6, 6])
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('CGH EEG Optitrack Assisted EEG localization')

        # Colours used for the graphs
        self.red_qcolor = QColor(255, 0, 0) # NZIZ
        self.green_qcolor = QColor(0, 255, 0) # Circum
        self.blue_qcolor = QColor(0, 0, 255) # Ear2Ear
        self.yellow_qcolor = QColor(255, 255, 0) # Stylus position
        self.black_qcolor = QColor(0, 0 ,0) # Specs position
        self.orange_qcolor = QColor(255, 165, 0) # Predicted position
        self.grey_qcolor = QColor(128,128,128) # Reflective Markers

        self.coordinates = np.random.randint(-5, 5, size=(1, 2)) 
        self.coordinates2 = np.random.randint(-5, 5, size=(1, 2)) 
        self.coordinates3 = np.random.randint(-5, 5, size=(1, 2)) 
        self.xdata = self.coordinates[:,0]
        self.ydata = self.coordinates[:,1]
        self.xdata2 = self.coordinates2[:,0]
        self.ydata2 = self.coordinates2[:,1]
        self.xdata3 = self.coordinates3[:,0]
        self.ydata3 = self.coordinates3[:,1]


        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.matlabcanvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.matlabcanvas.axes.scatter(self.xdata, self.ydata)
        self.setCentralWidget(self.matlabcanvas)

        self.NZIZ_trace_ref = self.matlabcanvas.axes.scatter(self.xdata, self.ydata, color='red')
        # if self.Circum_trace_ref != None:
        self.Circum_trace_ref = self.matlabcanvas.axes.scatter(self.xdata2, self.ydata2, color='blue')
        # if self.EartoEar_trace_ref != None:
        self.EartoEar_trace_ref = self.matlabcanvas.axes.scatter(self.xdata2, self.ydata2, color='green')


        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(33) # ~30hz
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.coordinates = np.random.randint(-5, 5, size=(1, 2)) 
        self.coordinates2 = np.random.randint(-5, 5, size=(1, 2)) 
        self.coordinates3 = np.random.randint(-5, 5, size=(1, 2)) 
        self.xdata = self.coordinates[:,0]
        self.ydata = self.coordinates[:,1]
        self.xdata2 = self.coordinates2[:,0]
        self.ydata2 = self.coordinates2[:,1]
        self.xdata3 = self.coordinates3[:,0]
        self.ydata3 = self.coordinates3[:,1]

        self.matlabcanvas.axes.cla()
        self.matlabcanvas.axes.set_xlim([-6, 6])
        self.matlabcanvas.axes.set_ylim([-6, 6])
        # if self.NZIZ_trace_ref != None:

        self.NZIZ_trace_ref.remove()
        self.NZIZ_trace_ref = self.matlabcanvas.axes.scatter(self.xdata, self.ydata, color='red')
        self.Circum_trace_ref.remove()
        self.Circum_trace_ref = self.matlabcanvas.axes.scatter(self.xdata2, self.ydata2, color='blue')
        # if self.EartoEar_trace_ref != None:a
        self.EartoEar_trace_ref.remove()
        self.EartoEar_trace_ref = self.matlabcanvas.axes.scatter(self.xdata2, self.ydata2, color='green')
        self.matlabcanvas.draw()

        # # Note: we no longer need to clear the axis.
        # if self.matlabcanvas is None:
        #     # First time we have no plot reference, so do a normal plot.
        #     # .plot returns a list of line <reference>s, as we're
        #     # only getting one we can take the first element.
        #     # plot_refs = self.matlabcanvas.axes.scatter(self.x, self.ydata, 'r')
        # else:
        #     # We have a reference, we can use it to update the data for that line.
        #     self._plot_ref.set_ydata(self.ydata)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.resize(440, 300)
    sys.exit(app.exec())