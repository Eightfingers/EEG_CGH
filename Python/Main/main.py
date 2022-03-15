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
# from optitrack_thread import OptitrackMainThread
from optitrack_thread import OptitrackMainThread
from scipy.spatial.transform import Rotation as R

# https://doc.qt.io/qtforpython/PySide6/QtDataVisualization/QAbstract3DGraph.html#PySide6.QtDataVisualization.PySide6.QtDataVisualization.QAbstract3DGraph.currentFps
# Numpy data is processed in Nx3 format

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('CGH EEG Optitrack Assisted EEG localization')

        # The graph
        self.scatter = Q3DScatter()
        # self.scatter.setAspectRatio(1)
        # self.scatter.setHorizontalAspectRatio(1)

        # Colours used for the graphs
        self.red_qcolor = QColor(255, 0, 0) # NZIZ
        self.green_qcolor = QColor(0, 255, 0) # Circum
        self.blue_qcolor = QColor(0, 0, 255) # Ear2Ear
        self.yellow_qcolor = QColor(255, 255, 0) # Stylus position
        self.black_qcolor = QColor(0, 0 ,0) # Specs positionQqqqqqqqqqq
        self.orange_qcolor = QColor(255, 165, 0) # Predicted position
        self.grey_qcolor = QColor(128,128,128) # Reflective Markers


        # Used to control scatter size on the graph
        self.itemsize = 0.1
        self.bigger_itemsize = 0.15
        self.threshold_placement_range = 0.008 # 0.008m , 8mm 

        # Each of this series is used to represent data on the graph
        self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.NZIZscatter_series_trace = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.CIRCUMscatter_series = self.create_new_scatter_series(self.green_qcolor, self.itemsize)
        self.EarToEarscatter_series = self.create_new_scatter_series(self.black_qcolor, self.itemsize)
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize)
        self.specs_series = self.create_new_scatter_series(self.black_qcolor, self.bigger_itemsize)
        self.stylus_position_series = self.create_new_scatter_series(self.yellow_qcolor, self.bigger_itemsize)
        self.reflective_markers_position_series = self.create_new_scatter_series(self.grey_qcolor, self.itemsize)

        # Variables to store positional and predicted data, some are unused
        self.predicted_positions = None
        self.fpz_positon = None
        self.NZIZ_data = None
        self.NZIZ_specs_data = None
        self.NZIZ_specs_rotate = None
        self.CIRCUM_data = None
        self.CIRCUM_specs_data = None
        self.CIRCUM_specs_rotate = None
        self.EarToEar_data = None
        self.EarToEar_specs_data = None
        self.EarToEar_specs_rotate = None
        self.specs_live_position = None
        self.specs_rotation = None

        self.NZIZ_BUTTON = 1
        self.CIRCUM_BUTTON = 2
        self.EARTOEAR_BUTTON = 3
        
        self.live_predicted_eeg_positions = False
        self.live_predicted_nziz_positions = False

        # Set the axis properties
        segment_count = 8
        sub_segment_count = 2
        axis_minimum = -0.6
        axis_maximum = 0.6
        self.x_axis = QValue3DAxis()
        self.x_axis.setTitle('X')
        self.x_axis.setTitleVisible(True)
        self.x_axis.setSegmentCount(segment_count)
        self.x_axis.setRange(axis_minimum, axis_maximum)
        self.x_axis.setSubSegmentCount(sub_segment_count)
        # self.x_axis.setAutoAdjustRange(True)

        self.y_axis = QValue3DAxis()
        self.y_axis.setTitle('Y')
        self.y_axis.setTitleVisible(True)  
        self.y_axis.setSegmentCount(8)  
        self.y_axis.setSegmentCount(segment_count)
        self.y_axis.setRange(axis_minimum, axis_maximum)
        self.y_axis.setSubSegmentCount(sub_segment_count)
        # self.y_axis.setAutoAdjustRange(True)

        self.z_axis = QValue3DAxis()
        self.z_axis.setTitle('Z')
        self.z_axis.setTitleVisible(True)
        self.z_axis.setSegmentCount(8)  
        self.z_axis.setSegmentCount(segment_count)
        self.z_axis.setRange(axis_minimum, axis_maximum)
        self.z_axis.setSubSegmentCount(sub_segment_count)
        # self.z_axis.setAutoAdjustRange(True)

        self.scatter.setAxisX(self.x_axis)
        self.scatter.setAxisY(self.y_axis)
        self.scatter.setAxisZ(self.z_axis)
        # self.scatter.setMargin(0.01)

        # Set no Shadow
        self.scatter.setShadowQuality(QAbstract3DGraph.ShadowQualityNone)

        # Main central widget
        self.graph = QWidget.createWindowContainer(self.scatter)
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.graph.setMinimumSize(size, size) # GUI size
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
        self.optitrack_main_thread = OptitrackMainThread(self)
        self.optitrack_main_thread.start()  
        
        # Now connect and initialize the Signals in the MenuWidget with the threads
        self.left_dock_menu_widget.connect_matlab_signals(self.matlab_main_thread)
        self.left_dock_menu_widget.connect_optitrack_signals(self.optitrack_main_thread)

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

        self.scatter.removeSeries(self.Predicted21_series) # remove the old series
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize) # reset the seties
        self.add_list_to_scatterdata(self.Predicted21_series, self.predicted_positions)
        self.scatter.addSeries(self.Predicted21_series)

        self.predicted_eeg_positions_global_frame = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_live_rotation , self.specs_live_position)
        np.savetxt("21_predicted_positions_global_frame.csv", message, delimiter=',')
    
    @Slot(bool)
    def set_reflective_markers(self, message):
        self.live_reflective_markers = message

    # Clear all data shown in the graph
    @Slot()
    def clear_data(self):
        # set it to false
        self.live_predicted_eeg_positions = False
        self.live_predicted_nziz_positions = False

        self.scatter.removeSeries(self.NZIZscatter_series)
        self.scatter.removeSeries(self.CIRCUMscatter_series)
        self.scatter.removeSeries(self.EarToEarscatter_series)
        self.scatter.removeSeries(self.Predicted21_series)
        self.scatter.removeSeries(self.reflective_markers_position_series)

        self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.NZIZscatter_series_trace = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.CIRCUMscatter_series = self.create_new_scatter_series(self.green_qcolor, self.itemsize)
        self.EarToEarscatter_series = self.create_new_scatter_series(self.black_qcolor, self.itemsize)
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize)
        self.reflective_markers_position_series = self.create_new_scatter_series(self.yellow_qcolor, self.itemsize)

    @Slot(np.ndarray)
    def update_fpz_position(self, message):
        self.fpz_positon = message
        np.savetxt("nziz_5_positions.csv", message, delimiter=',')

    @Slot(np.ndarray)
    def update_current_stylus_position(self, message):
        self.scatter.removeSeries(self.stylus_position_series) # remove the old position
        self.stylus_position_series = self.create_new_scatter_series(self.yellow_qcolor, self.bigger_itemsize)
        self.add_list_to_scatterdata(self.stylus_position_series, message)
        self.scatter.addSeries(self.stylus_position_series)
        self.scatter.show()

    @Slot(list)
    def update_current_specs_position_rotation(self, message):
        self.specs_live_position = message[0]
        self.specs_rotation = message[1]
        self.scatter.removeSeries(self.specs_series) # remove the old position
        self.specs_series = self.create_new_scatter_series(self.black_qcolor, self.bigger_itemsize) # reset the seties
            
        self.add_list_to_scatterdata(self.specs_series, self.specs_live_position)
        self.scatter.addSeries(self.specs_series)
        self.scatter.show()

        if (self.live_predicted_eeg_positions == True):
            # Convert predicted eeg_position from spec frame to global frame 
            self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_live_position)
            self.scatter.removeSeries(self.Predicted21_series) # remove the old series
            self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize) # reset the seties
            self.add_list_to_scatterdata(self.Predicted21_series, self.global_predicted_eeg_positions)
            self.scatter.addSeries(self.Predicted21_series)
            self.scatter.show()

        if (self.live_predicted_nziz_positions == True):
            # Convert predicted nziz from spec frame to global frame 
            self.global_predicted_nziz_positions = self.transform_spec_to_global_frame(self.fpz_positon, self.specs_rotation, self.specs_live_position)
            if self.NZIZscatter_series_trace in self.scatter.seriesList():
                self.scatter.removeSeries(self.NZIZscatter_series_trace) # remove the trace if its still there
            self.scatter.removeSeries(self.NZIZscatter_series)
            self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
            self.add_list_to_scatterdata(self.NZIZscatter_series, self.global_predicted_nziz_positions)
            self.scatter.addSeries(self.NZIZscatter_series)

            self.scatter.show()

    def transform_spec_to_global_frame(self, series, specs_rotation, specs_position):
        print(specs_rotation)
        specs_rotation[[3,0]] = specs_rotation[[0, 3]]
        r = R.from_quat(specs_rotation) # rotate the orientation
        #print("The SPECS rotation is ..", specs_rotation)
        # print("The Specs position is ..", specs_live_position)
        new_predicted_positions = r.apply(series)
        new_predicted_positions = new_predicted_positions + specs_position # now add the displaced amount
        # print("Main: The specs position is",specs_live_position)
        return new_predicted_positions

    @Slot(bool)
    def set_live_predicted_eeg_positions(self, message):
        self.live_predicted_eeg_positions = message

    @Slot(bool)
    def set_live_fpz_positions(self, message):
        self.live_predicted_nziz_positions = message

    # This is not the predicted position, rather it will show positions of
    # electrode with optitrack markers
    @Slot(np.ndarray)
    def update_reflective_markers_positions(self, message):
        self.scatter.removeSeries(self.reflective_markers_position_series) # remove the old position
        self.reflective_markers_position_series = self.create_new_scatter_series(self.grey_qcolor, self.itemsize)
        self.add_list_to_scatterdata(self.reflective_markers_position_series, message)
        self.scatter.addSeries(self.reflective_markers_position_series)
        self.scatter.show()

        # if near become green.

        # else it is grey

    @Slot(np.ndarray)
    def update_and_add_scatterNZIZ(self, message):
        self.add_list_to_scatterdata(self.NZIZscatter_series_trace, message)
        self.scatter.addSeries(self.NZIZscatter_series_trace)
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
        if data.ndim == 1: # if its one dimensional
            scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(data[0], data[1], data[2])))
        else:
            for d in data:
                scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[1], d[2])))

    def create_new_scatter_series(self, colour, size):
        self.scatter_series_new_series = QScatter3DSeries()
        self.scatter_series_new_series.setBaseColor(colour)
        self.scatter_series_new_series.setItemSize(size)

        return self.scatter_series_new_series

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

    @Slot(float)
    def adjust_axis_min_max(self, message):
        position = message / 10
        # Make bigger range
        self.scatter.axisX().setRange(self.axis_minimum - position, self.axis_maximum + position)
        self.scatter.axisY().setRange(self.axis_minimum - position, self.axis_maximum + position)
        self.scatter.axisZ().setRange(self.axis_minimum - position, self.axis_maximum + position)


if __name__ == '__main__':  
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())