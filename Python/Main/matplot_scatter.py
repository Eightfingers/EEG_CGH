from multiprocessing import dummy
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QPointF, QSize, QStringConverter, Qt, Slot, QTimer
from PySide6.QtGui import QGuiApplication, QVector3D, QColor, QPainter
from PySide6.QtWidgets import QBoxLayout, QDockWidget, QHBoxLayout, QMainWindow, QApplication, QSizePolicy, QVBoxLayout, QWidget
from PySide6.QtCharts import QAbstractAxis, QCategoryAxis, QChart, QChartView, QLegend, QScatterSeries, QValueAxis, QBarCategoryAxis
import numpy as np
from matlab_thread import MatlabMainThread
from menu_widget import MenuWidget
from status_widget import StatusWidget
# from optitrack_thread import OptitrackMainThread
from optitrack_thread import OptitrackMainThread
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

        self.x = np.array([5,7,8,7,2,17,2,9,4,11,12,9,6])
        self.y = np.array([99,86,87,88,111,86,103,87,94,78,77,85,86])
        self.coordinates = np.random.randint(-5, 5, size=(100, 2)) 
        self.xdata = self.coordinates[0]
        self.ydata = self.coordinates[1]

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.matlabcanvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.matlabcanvas.axes.scatter(self.xdata, self.ydata)

        dummy_array = np.array([[1000,1000],[1000,1000]])
        x_dummy = dummy_array[:,0]
        y_dummy = dummy_array[:,0]
        
        self.stylus_position = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.NZIZ_trace_ref = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green') 
        self.Circum_trace_ref = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.EartoEar_trace_ref = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')

        self.EartoEar_data_trace = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.EartoEar_specs_data = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.EartoEar_specs_rotate = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        
        self.NZIZ_data_trace = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.NZIZ_specs_data = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.NZIZ_specs_rotate = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')

        self.CIRCUM_data_trace = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.CIRCUM_specs_data = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.CIRCUM_specs_rotate = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')

        self.stylus_position = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.specs_position = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')

        self.Predicted21_series = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')
        self.NZIZscatter_series = self.matlabcanvas.axes.scatter(x_dummy, y_dummy, color='green')

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
        self.setCentralWidget(self.matlabcanvas)

        # Start the main thread
        self.matlab_main_thread = MatlabMainThread(self)
        self.matlab_main_thread.start()

        # Start the Optitrack Thread
        self.optitrack_main_thread = OptitrackMainThread(self)
        self.optitrack_main_thread.start()  
        
        # Now connect and initialize the Signals in the MenuWidget with the threads
        self.left_dock_menu_widget.connect_matlab_signals(self.matlab_main_thread)
        self.left_dock_menu_widget.connect_optitrack_signals(self.optitrack_main_thread)

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(33) # ~30hz
        self.timer.timeout.connect(self.update_plot)
        # self.timer.start()

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
        self.matlabcanvas.axes.scatter(self.xdata, self.ydata, color='red')
        self.matlabcanvas.axes.scatter(self.xdata2, self.ydata2, color='blue')
        self.matlabcanvas.axes.scatter(self.xdata2, self.ydata2, color='green')
        self.matlabcanvas.draw()

    # Function that is called from the menu widget to save trace data into csv files
    @Slot(int)
    def save_trace_data (self, message):
        # Get the data from the optitrack thread
        self.stylus_data = self.optitrack_main_thread.stylus_data
        self.specs = self.optitrack_main_thread.specs_data
        self.specs_rotation = self.optitrack_main_thread.specs_rotation_data

        # Strip of all the zeroes
        self.stylus_data = self.stylus_data[~np.all(self.stylus_data == 0, axis=1)]
        self.specs = self.specs[~np.all(self.specs == 0, axis=1)]
        self.specs_rotation = self.specs_rotation[~np.all(self.specs_rotation == 0, axis=1)]

        if (message == self.NZIZ_BUTTON): # NZIZ
            print("Main: Saving NZIZ data")
            np.savetxt("data_NZIZstylus.csv", self.stylus_data, delimiter=',')
            np.savetxt("data_NZIZspecs.csv", self.specs, delimiter=',')
            np.savetxt("rotation_data_NZIZspecs.csv", self.specs_rotation, delimiter=',')
            self.stylus_data[:,0] *= -1 # recitfy the x axis
            self.NZIZ_data_trace = self.stylus_data
            self.NZIZ_specs_data = self.specs
            self.NZIZ_specs_rotate = self.specs_rotation

            self.x_data = self.NZIZ_data_trace[0]
            self.y_data = self.NZIZ_data_trace[1]
            # self.update_and_add_scatterNZIZ(self.stylus_data)
            self.NZIZ_trace_ref = self.matlabcanvas.axes.scatter(self.xdata2, self.ydata2, color='green')
            self.matlabcanvas.draw()

        elif (message == self.CIRCUM_BUTTON): # Circum
            print("Main: Saving Circum data")
            np.savetxt("data_CIRCUMstylus.csv", self.stylus_data, delimiter=',')
            np.savetxt("data_CIRCUMspecs.csv", self.specs, delimiter=',')
            np.savetxt("rotation_data_CIRCUMspecs.csv", self.specs_rotation, delimiter=',')
            self.stylus_data[:,0] *= -1 # recitfy the x axis

            self.CIRCUM_data_trace = self.stylus_data
            self.CIRCUM_specs_data = self.specs
            self.CIRCUM_specs_rotate = self.specs_rotation

            self.x_data = self.CIRCUM_data_trace[0]
            self.y_data = self.CIRCUM_data_trace[1]
            # self.update_and_add_scatterCIRCUM(self.stylus_data)
            self.Circum_trace_ref = self.matlabcanvas.axes.scatter(self.x_data, self.y_data, color='green')
            self.matlabcanvas.draw()

        elif (message == self.EARTOEAR_BUTTON): # Ear to Ear
            print("Main: Saving Ear to Ear data")
            np.savetxt("data_EarToEarstylus.csv", self.stylus_data, delimiter=',')
            np.savetxt("data_EarToEarspecs.csv", self.specs, delimiter=',')
            np.savetxt("rotation_data_EarToEarspecs.csv", self.specs_rotation, delimiter=',')
            self.stylus_data[:,0] *= -1 # recitfy the x axis

            self.EartoEar_data_trace = self.stylus_data
            self.EartoEar_specs_data = self.specs
            self.EartoEar_specs_rotate = self.specs_rotation
            self.x_data = self.EartoEar_data_trace[0]
            self.y_data = self.EartoEar_data_trace[1]
            # self.update_and_add_scatterNZIZ(self.stylus_data)
            # self.update_and_add_scatterEarToEar(self.stylus_data)
            self.EartoEar_trace_ref = self.matlabcanvas.axes.scatter(self.x_data, self.y_data, color='green')
            self.matlabcanvas.draw()

    @Slot(np.ndarray)
    def update_save_predicted_eeg_positions(self, message):
        self.predicted_positions = message
        np.savetxt("21_predicted_positions_specs_frame.csv", message, delimiter=',')
        # if self.Predicted21_series is not None:
        #     self.chart.removeSeries(self.Predicted21_series) # remove the old series
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.marker_size) # reset the seties
        self.add_list_to_scatterdata2D(self.Predicted21_series, self.predicted_positions)
        self.chart.addSeries(self.Predicted21_series)

        self.predicted_eeg_positions_global_frame = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_position)
        np.savetxt("21_predicted_positions_global_frame.csv", message, delimiter=',')

    # Clear all data shown in the graph
    @Slot()
    def clear_data(self):
        # set it to false
        print("Clearing data")

    @Slot(np.ndarray)
    def update_fpz_position(self, message):
        self.fpz_positon = message
        np.savetxt("nziz_5_positions.csv", message, delimiter=',')

    @Slot(np.ndarray)
    def show_current_stylus_position(self, message):
        # print("The current stylus position is", message[0])
        stylus_position = message[0]
        x_data = stylus_position[0]
        y_data = stylus_position[1]

        # self.update_and_add_scatterNZIZ(self.stylus_data)
        self.stylus_position.remove()
        self.stylus_position = self.matlabcanvas.axes.scatter(x_data, y_data, color='green')
        self.matlabcanvas.show()

    @Slot(list)
    def update_current_specs_position_rotation(self, message):
        self.specs_position = message[0]
        self.specs_rotation = message[1]

        print("The current specs position is", self.specs_position)
        # print("The current stylus position is", message[0])
        stylus_position = message[0]
        x_data = stylus_position[0]
        y_data = stylus_position[1]

        # self.update_and_add_scatterNZIZ(self.stylus_data)
        self.stylus_position.remove()
        self.stylus_position = self.matlabcanvas.axes.scatter(x_data, y_data, color='green')
        self.matlabcanvas.show()

        if (self.live_predicted_eeg_positions == True):
            # Convert predicted eeg_position from spec frame to global frame 
            self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_position)
            x_data = self.global_predicted_eeg_positions[0]
            y_data = self.global_predicted_eeg_positions[1]

            self.Predicted21_series.remove()
            self.Predicted21_series = self.matlabcanvas.axes.scatter(x_data, y_data, color='green')
            self.matlabcanvas.show()

        if (self.live_predicted_nziz_positions == True):
            # Convert predicted nziz from spec frame to global frame 
            self.global_predicted_nziz_positions = self.transform_spec_to_global_frame(self.fpz_positon, self.specs_rotation, self.specs_position)

            self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_position)
            x_data = self.global_predicted_eeg_positions[0]
            y_data = self.global_predicted_eeg_positions[1]

            self.NZIZscatter_series_trace.remove()
            self.NZIZscatter_series_trace = self.matlabcanvas.axes.scatter(x_data, y_data, color='green')
            self.matlabcanvas.show()

    def transform_spec_to_global_frame(self, series, specs_rotation, specs_position):
        r = R.from_quat(specs_rotation) # rotate the orientation
        #print("The SPECS rotation is ..", specs_rotation)
        # print("The Specs position is ..", specs_position)
        new_predicted_positions = r.apply(series)
        new_predicted_positions = new_predicted_positions + specs_position # now add the displaced amount
        # print("Main: The specs position is",specs_position)
        return new_predicted_positions

    @Slot(bool)
    def set_live_predicted_eeg_positions(self, message):
        self.live_predicted_eeg_positions = message

    @Slot(bool)
    def set_live_fpz_positions(self, message):
        self.live_predicted_nziz_positions = message

    # This is not the predicted position, rather it will show positions of
    # electrode with optitrack markers. The message here contains the positions of reflective markers
    @Slot(np.ndarray)
    def show_electrode_positions(self, message):
        if self.reflective_markers_series is not None:
            self.chart.removeSeries(self.reflective_markers_series) # remove the old position
        self.reflective_markers_series = self.create_new_scatter_series(self.grey_qcolor, self.marker_size)
        self.reflective_marker_in_eeg_position = self.create_new_scatter_series(self.green_qcolor, self.marker_size) # reflective marker in eeg position

        # Check if the optitrack markers are near any electrode positions
        if self.near_predicted_points(message):
            self.add_list_to_scatterdata2D(self.reflective_marker_in_eeg_position, self.predicted_eeg_positions_with_electrodes)
            self.chart.addSeries(self.reflective_marker_in_eeg_position)
        else:
            self.add_list_to_scatterdata2D(self.reflective_markers_series, self.unassigned_electrode_markers)
            self.chart.addSeries(self.reflective_markers_series)

        self.chart.addSeries(self.reflective_markers_series)
        self.chart.show()

    @Slot(np.ndarray)
    def update_and_add_scatterNZIZ(self, message):
        self.add_list_to_scatterdata2D(self.NZIZscatter_series_trace, message)
        self.chart.addSeries(self.NZIZscatter_series_trace)
        self.chart.show()

    @Slot(np.ndarray)
    def update_and_add_scatterCIRCUM(self, message):
        self.add_list_to_scatterdata2D(self.CIRCUMscatter_series, message)
        self.chart.addSeries(self.CIRCUMscatter_series)
        self.chart.show()

    @Slot(np.ndarray)
    def update_and_add_scatterEarToEar(self, message):
        self.add_list_to_scatterdata2D(self.EarToEarscatter_series, message)
        self.chart.addSeries(self.EarToEarscatter_series)
        self.chart.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.resize(440, 300)
    sys.exit(app.exec())