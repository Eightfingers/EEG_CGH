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
import numpy as np
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
import os

# Adapted from https://www.pythonguis.com/tutorials/plotting-pyqtgraph/ the tutorial on updating data
# pyQtgraph docs https://pyqtgraph.readthedocs.io/en/latest/index.html 

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Qt DataVisualization 2D scatter')
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.plotItem.setTitle("2D view")
        self.setCentralWidget(self.graphWidget)
        
        self.graphWidget.setBackground('w')

        self.live_predicted_eeg_positions = False
        self.live_predicted_nziz_positions = False

        # Variables to hold positions
        self.NZIZscatter_series_x = np.zeros(1)
        self.NZIZscatter_series_y = np.zeros(1)
        self.CIRCUMscatter_series_x = None
        self.CIRCUMscatter_series_y = None
        self.EarToEarscatter_series_x = None
        self.EarToEarscatter_series_y = None
        self.Predicted21_series_x = None
        self.Predicted21_series_y = None
        self.electrode_markers_series_x = None
        self.electrode_markers_series_y = None
        self.specs_series_x = None
        self.specs_series_y = None
        self.stylus_position_series_x = None
        self.stylus_position_series_y = None

        # Colours used for the graphs
        self.red_qcolor = (255, 0, 0) # NZIZ
        self.green_qcolor = (0, 255, 0) # Circum
        self.blue_qcolor = (0, 0, 255) # Ear2Ear
        self.orange_qcolor = (255, 165, 0) # Predicted position
        self.black_qcolor = (0, 0 ,0) # Specs position
        self.yellow_qcolor = (255, 255, 0) # Stylus position
        self.grey_qcolor = (128,128,128) # Reflective Markers

        # Can adjust line colours but not scatter plot colours much

        # Init the few data_line
        self.NZIZ_scatter_trace = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None,symbolBrush=(self.red_qcolor))
        self.Circum_scatter_traec = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.green_qcolor))
        self.EartoEar_scatter_trace = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.blue_qcolor))

        self.NZIZ_scatter = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None,symbolBrush=(self.red_qcolor))
        # self.Circum_scatter = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.green_qcolor))
        # self.EartoEar_scatter = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.blue_qcolor))

        self.Predicter21_scatter = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.orange_qcolor))
        self.electrode_marker_scatter = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.green_qcolor))

        self.reflective_markers_series = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.orange_qcolor))
        self.reflective_marker_in_eeg_position = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.green_qcolor))

        self.specs_scatter = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.black_qcolor))
        self.stylus_scatter = self.graphWidget.plot(self.NZIZscatter_series_x, self.NZIZscatter_series_y, pen=None, symbolBrush=(self.yellow_qcolor))

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

        # Start the matlab thread
        self.matlab_main_thread = MatlabMainThread(self)
        self.matlab_main_thread.start()

        # Start the Optitrack Thread
        self.optitrack_main_thread = OptitrackMainThread(self)
        self.optitrack_main_thread.start()  

        # self.timer = QTimer()
        # self.timer.setInterval(10)
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

    # def update_plot_data(self):

    #     self.x = self.x[1:]  # Remove the first y element.
    #     self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

    #     self.y = self.y[1:]  # Remove the first
    #     self.y.append( randint(0,100))  # Add a new random value.

    #     self.data_line.setData(self.x, self.y)  # Update the data.

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
            self.NZIZ_data = self.stylus_data

            # self.stylus_data[:,0] *= -1 # recitfy the x axis
            self.NZIZ_specs_data = self.specs
            self.NZIZ_specs_rotate = self.specs_rotation
            self.update_and_add_scatterNZIZ(self.stylus_data)

        elif (message == self.CIRCUM_BUTTON): # Circum
            print("Main: Saving Circum data")
            np.savetxt("data_CIRCUMstylus.csv", self.stylus_data, delimiter=',')
            np.savetxt("data_CIRCUMspecs.csv", self.specs, delimiter=',')
            np.savetxt("rotation_data_CIRCUMspecs.csv", self.specs_rotation, delimiter=',')
            self.CIRCUM_data = self.stylus_data
            self.CIRCUM_specs_data = self.specs
            self.CIRCUM_specs_rotate = self.specs_rotation
            # self.stylus_data[:,0] *= -1 # recitfy the x axis
            self.update_and_add_scatterCIRCUM(self.stylus_data)

        elif (message == self.EARTOEAR_BUTTON): # Ear to Ear
            print("Main: Saving Ear to Ear data")
            np.savetxt("data_EarToEarstylus.csv", self.stylus_data, delimiter=',')
            np.savetxt("data_EarToEarspecs.csv", self.specs, delimiter=',')
            np.savetxt("rotation_data_EarToEarspecs.csv", self.specs_rotation, delimiter=',')
            self.EartoEar_data = self.stylus_data
            self.EartoEar_specs_data = self.specs
            self.EartoEar_specs_rotate = self.specs_rotation
            # self.stylus_data[:,0] *= -1 # recitfy the x axis
            self.update_and_add_scatterEarToEar(self.stylus_data)

    @Slot(np.ndarray)
    def update_save_predicted_eeg_positions(self, message):
        self.predicted_positions = message
        np.savetxt("21_predicted_positions_specs_frame.csv", message, delimiter=',')
        if self.Predicted21_series is not None:
            self.chart.removeSeries(self.Predicted21_series) # remove the old series
        
        # self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.marker_size) # reset the seties
        # self.add_list_to_scatterdata2D(self.Predicted21_series, self.predicted_positions)
        # self.chart.addSeries(self.Predicted21_series)

        self.predicted_eeg_positions_global_frame = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_position)
        np.savetxt("21_predicted_positions_global_frame.csv", message, delimiter=',')
        self.Predicted21_series_x = self.predicted_eeg_positions_global_frame[0]
        self.Predicted21_series_y = self.predicted_eeg_positions_global_frame[2]
        self.Predicter21_scatter.setData(self.Predicted21_series_x, self.Predicted21_series_y)

    # Clear all data shown in the graph
    @Slot()
    def clear_data(self):
        # set it to false
        self.live_predicted_eeg_positions = False
        self.live_predicted_nziz_positions = False

        self.chart.removeSeries(self.NZIZscatter_series)
        self.chart.removeSeries(self.CIRCUMscatter_series)
        self.chart.removeSeries(self.EarToEarscatter_series)
        self.chart.removeSeries(self.Predicted21_series)
        self.chart.removeSeries(self.reflective_markers_series)

        self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.marker_size)
        self.NZIZscatter_series_trace = self.create_new_scatter_series(self.red_qcolor, self.marker_size)
        self.CIRCUMscatter_series = self.create_new_scatter_series(self.green_qcolor, self.marker_size)
        self.EarToEarscatter_series = self.create_new_scatter_series(self.black_qcolor, self.marker_size)
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.marker_size)
        self.reflective_markers_series = self.create_new_scatter_series(self.yellow_qcolor, self.marker_size)

    @Slot(np.ndarray)
    def update_fpz_position(self, message):
        self.fpz_positon = message
        np.savetxt("nziz_5_positions.csv", message, delimiter=',')

    @Slot(np.ndarray)
    def update_current_stylus_position(self, message):
        x = np.array([message[0]])
        y = np.array([message[1]])
        self.stylus_scatter.setData(x,y)

    @Slot(list)
    def update_current_specs_position_rotation(self, message):
        self.specs_position = message[0]
        self.specs_rotation = message[1]

        x = np.array([self.specs_position[0]])
        y = np.array([self.specs_position[1]])

        self.specs_scatter.setData(x, y)

        if (self.live_predicted_eeg_positions == True):
            # Convert predicted eeg_position from spec frame to global frame 
            self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_position)

            x = np.array([self.self.global_predicted_eeg_positions[0]])
            y = np.array([self.self.global_predicted_eeg_positions[1]])

            self.Predicter21_scatter.setData(x, y)


        if (self.live_predicted_nziz_positions == True):
            # Convert predicted nziz from spec frame to global frame 
            self.global_predicted_nziz_positions = self.transform_spec_to_global_frame(self.fpz_positon, self.specs_rotation, self.specs_position)

            x = np.array([self.self.global_predicted_nziz_positions[0]])
            y = np.array([self.self.global_predicted_nziz_positions[1]])

            self.Predicter21_scatter.setData(x, y)

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
    def update_reflective_markers_positions(self, message):
        # Check if the optitrack markers are near any electrode positions
        if self.near_predicted_points(message):
            x = np.array([message[0]])
            y = np.array([message[1]])
            self.reflective_marker_in_eeg_position.setData(x,y)

        else:
            x = np.array([message[0]])
            y = np.array([message[1]])
            self.reflective_markers_series.setData(x,y)
            

    @Slot(np.ndarray)
    def update_and_add_scatterNZIZ(self, message):  
        x = np.array([message[0]])
        y = np.array([message[1]])

        self.NZIZ_scatter_trace.setData(x,y)

    @Slot(np.ndarray)
    def update_and_add_scatterCIRCUM(self, message):
        x = np.array([message[0]])
        y = np.array([message[1]])

        self.Circum_scatter_traec.setData(x,y)

    @Slot(np.ndarray)
    def update_and_add_scatterEarToEar(self, message):
        x = np.array([message[0]])
        y = np.array([message[1]])

        self.EartoEar_scatter_trace.setData(x,y)

    def add_list_to_scatterdata2D(self,scatter_series, data):
        print(data)
        if data.ndim == 1: # its a single dimensional array
            print(data.ndim)
            print(data[0])
        # scatter_series.append(data[0], data[2])

    def create_new_scatter_series(self, colour, size):
        self.chart_series_new_series = QScatterSeries()
        self.chart_series_new_series.setColor(colour)
        self.chart_series_new_series.setMarkerSize(size)

        return self.chart_series_new_series

    def near_predicted_points(self, sample_data):
        data_set = self.predicted_positions
        for sample in sample_data:
            for data in data_set:
                magnitude_difference = np.absolute(np.linalg.norm(sample) - np.linalg.norm(data))
                if magnitude_difference < self.threshold_placement_range:
                    index = np.where(data_set == data) 
                    self.predicted_eeg_positions_with_electrodes = np.delete(self.predicted_positions, index) # Found the attached electrode
                    self.predicted_positions = np.delete(self.predicted_positions, index) # Delete from the lsit of 21 positions 
                    index_sample = np.where(sample_data == sample)
                    self.unassigned_electrode_markers = np.delete(sample_data, index_sample) # Not yet attached electrodes
                    return True
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
