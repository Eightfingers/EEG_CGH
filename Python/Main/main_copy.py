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
import os
from scipy.spatial.transform import Rotation as R

# https://doc.qt.io/qtforpython/PySide6/QtDataVisualization/QAbstract3DGraph.html#PySide6.QtDataVisualization.PySide6.QtDataVisualization.QAbstract3DGraph.currentFps
# Numpy data is processed in Nx3 format

# convetions 
# Matlab Z is upwards 
# Python QtScatter Y is upwards
# ScipyRotate 

# Quaternion convention
# Matlab w, x,y,z
# Optitrack x,y,z,w
# Scipy x,y,z,w


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('CGH EEG Optitrack Assisted EEG localization')

        # The graph
        self.scatter = Q3DScatter()

        # self.scatter.setAspectRatio(1)
        # self.scatter.setHorizontalAspectRatio(1)

        # Colours used for the graphs
        self.red_qcolor = QColor(255, 0, 0)
        self.green_qcolor = QColor(0, 255, 0)
        self.blue_qcolor = QColor(0, 0, 255)
        self.yellow_qcolor = QColor(255, 255, 0)
        self.orange_qcolor = QColor(255, 165, 0)
        self.black_qcolor = QColor(0, 0 ,0)
        self.grey_qcolor = QColor(128,128,128)

        # Used to control scatter size on the graph
        self.itemsize = 0.1
        self.bigger_itemsize = 0.15

        # Each of this series is used to represent data on the graph
        self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.NZIZscatter_series_trace = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.CIRCUMscatter_series = self.create_new_scatter_series(self.green_qcolor, self.itemsize)
        self.EarToEarscatter_series = self.create_new_scatter_series(self.black_qcolor, self.itemsize)
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize)
        self.specs_series = self.create_new_scatter_series(self.black_qcolor, self.bigger_itemsize)
        self.stylus_position_series = self.create_new_scatter_series(self.yellow_qcolor, self.bigger_itemsize)
        self.all_markers_series = self.create_new_scatter_series(self.grey_qcolor, self.itemsize)

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
        self.specs_position = None
        self.specs_rotation = None

        self.NZIZ_BUTTON = 1
        self.CIRCUM_BUTTON = 2
        self.EARTOEAR_BUTTON = 3
        self.live_predicted_eeg_positions = False
        self.live_predicted_nziz_positions = False

        # Set the axis properties
        segment_count = 8
        sub_segment_count = 2
        axis_minimum = -0.8
        axis_maximum = 0.8
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
            self.NZIZ_specs_data = self.specs
            self.NZIZ_specs_rotate = self.specs_rotation
            
            NZIZ_in_specs_frame = self.transform_from_global_to_specs_frame(self.NZIZ_data, self.NZIZ_specs_data, self.NZIZ_specs_rotate )
            # print("NZIZ IN SPECS FRAME IS ", NZIZ_in_specs_frame)
            self.fpz_positon = NZIZ_in_specs_frame
            np.savetxt("data_NZIZstylus_specs_frame.csv", NZIZ_in_specs_frame, delimiter=',')

            NZIZ_back_to_global_frame = self.transform_spec_to_global_frame(NZIZ_in_specs_frame, self.specs_rotation, self.specs_position)

            self.NZIZscatter_series2 = self.create_new_scatter_series(self.green_qcolor, self.itemsize)
            self.add_list_to_scatterdata(self.NZIZscatter_series2, NZIZ_back_to_global_frame)
            self.scatter.addSeries(self.NZIZscatter_series2)
            self.scatter.show()

            self.update_and_add_scatterNZIZ(NZIZ_in_specs_frame)
            self.update_and_add_scatterNZIZ(self.NZIZ_data) 

        elif (message == self.CIRCUM_BUTTON): # Circum
            print("Main: Saving Circum data")
            np.savetxt("data_CIRCUMstylus.csv", self.stylus_data, delimiter=',')
            np.savetxt("data_CIRCUMspecs.csv", self.specs, delimiter=',')
            np.savetxt("rotation_data_CIRCUMspecs.csv", self.specs_rotation, delimiter=',')
            self.CIRCUM_data = self.stylus_data
            self.CIRCUM_specs_data = self.specs
            self.CIRCUM_specs_rotate = self.specs_rotation
            self.update_and_add_scatterCIRCUM(self.stylus_data)

        elif (message == self.EARTOEAR_BUTTON): # Ear to Ear
            print("Main: Saving Ear to Ear data")
            np.savetxt("data_EarToEarstylus.csv", self.stylus_data, delimiter=',')
            np.savetxt("data_EarToEarspecs.csv", self.specs, delimiter=',')
            np.savetxt("rotation_data_EarToEarspecs.csv", self.specs_rotation, delimiter=',')
            self.EartoEar_data = self.stylus_data
            self.EartoEar_specs_data = self.specs
            self.EartoEar_specs_rotate = self.specs_rotation
            self.update_and_add_scatterEarToEar(self.stylus_data)

    def transform_from_global_to_specs_frame (self, stylus_trace, specs_position, specs_rotation):
        specs_position[:,0] *= -1
        specs_rotation[:,0] *= -1
        # specs_rotation = specs_rotation[:,[0,1,3,2]]
        # print("Before column swap")
        # print(specs_position[1,:])
        # specs_position = specs_position[:,[0,2,1]]
        # print("After column swap")
        # print(specs_position[1,:])

        r = R.from_quat(specs_rotation)
        r_inverse = r.inv() # get the inverse
        new_predicted_positions = r_inverse.apply(stylus_trace) # apply the inverse to the stylus trace to rotate it back to specs frame origin rotation 
        new_predicted_positions = new_predicted_positions - specs_position # minus the specs displacement amount to bring it to specs origin

        return new_predicted_positions


    @Slot(np.ndarray)
    def save_predicted_eeg_positions(self, message):
        self.predicted_positions = message

        self.scatter.removeSeries(self.Predicted21_series) # remove the old series
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize) # reset the seties
        self.add_list_to_scatterdata(self.Predicted21_series, self.predicted_positions)
        self.scatter.addSeries(self.Predicted21_series)

        np.savetxt("21_predicted_positions_specs_frame.csv", message, delimiter=',')

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
        self.scatter.removeSeries(self.all_markers_series)

        # self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        # self.NZIZscatter_series_trace = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        # self.CIRCUMscatter_series = self.create_new_scatter_series(self.green_qcolor, self.itemsize)
        # self.EarToEarscatter_series = self.create_new_scatter_series(self.black_qcolor, self.itemsize)
        # self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize)
        # self.all_markers_series = self.create_new_scatter_series(self.yellow_qcolor, self.itemsize)
    
    @Slot(np.ndarray)
    def update_fpz_position(self, message):
        # self.fpz_positon = message
        # self.scatter.removeSeries(self.NZIZscatter_series_trace) # remove the old position
        # self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        # self.add_list_to_scatterdata(self.NZIZscatter_series, self.fpz_positon)
        # self.scatter.addSeries(self.NZIZscatter_series)
        pass

    @Slot(np.ndarray)
    def show_current_stylus_position(self, message):
        self.scatter.removeSeries(self.stylus_position_series) # remove the old position
        self.stylus_position_series = self.create_new_scatter_series(self.yellow_qcolor, self.bigger_itemsize)
        self.add_list_to_scatterdata(self.stylus_position_series, message)
        self.scatter.addSeries(self.stylus_position_series)
        self.scatter.show()

    @Slot(list)
    def update_current_specs_position_rotation(self, message):
        self.specs_position = message[0]
        self.specs_rotation = message[1]
        self.scatter.removeSeries(self.specs_series) # remove the old position
        self.specs_series = self.create_new_scatter_series(self.black_qcolor, self.bigger_itemsize) # reset the seties
            
        self.add_list_to_scatterdata(self.specs_series, self.specs_position)
        self.scatter.addSeries(self.specs_series)
        self.scatter.show()
        # print("The SPECS rotation is ..", self.specs_rotation)
        # print("The Specs position is ..", self.specs_position)

        # if (self.live_predicted_eeg_positions == True):
        #     # Convert predicted eeg_position from spec frame to global frame 
        #     self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_position)
        #     self.scatter.removeSeries(self.Predicted21_series) # remove the old series
        #     self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize) # reset the seties
        #     self.add_list_to_scatterdata(self.Predicted21_series, self.global_predicted_eeg_positions)
        #     self.scatter.addSeries(self.Predicted21_series)
        #     self.scatter.show()

        if (self.live_predicted_nziz_positions == True):
            # Convert predicted nziz from spec frame to global frame 
            self.global_predicted_nziz_positions = self.transform_spec_to_global_frame(self.fpz_positon, self.specs_rotation, self.specs_position)
            # if self.NZIZscatter_series_trace in self.scatter.seriesList():
            #     self.scatter.removeSeries(self.NZIZscatter_series_trace) # remove the trace if its still there
            self.scatter.removeSeries(self.NZIZscatter_series)
            self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
            self.add_list_to_scatterdata(self.NZIZscatter_series, self.global_predicted_nziz_positions)
            self.scatter.addSeries(self.NZIZscatter_series)

            self.scatter.show()
            pass

    def transform_spec_to_global_frame(self, series, specs_rotation, specs_position):
        specs_position[0] *= -1
        specs_rotation[0] *= -1
        # print(specs_rotation, "ROTATIOn")
        # print(specs_position, "Position")
        # specs_rotation = specs_rotation[:,[0,1,3,2]]
        # print("Before column swap")
        # print(specs_position[1,:])
        # specs_position = specs_position[:,[0,2,1]]
        # print("After column swap")
        # print(specs_position[1,:])

        r = R.from_quat(specs_rotation) # rotate the orientation
        # print(series, "NIGAA THE SERIES IS THIS ")
        new_predicted_positions = r.apply(series)
        new_predicted_positions = new_predicted_positions + specs_position # now add the displaced amount
        # print("Main: The specs position is",specs_position)
        return new_predicted_positions

    @Slot(bool)
    def set_live_predicted_eeg_positions(self, message):
        self.live_predicted_eeg_positions = message
        self.scatter.removeSeries(self.CIRCUMscatter_series)
        self.scatter.removeSeries(self.EarToEarscatter_series)


    @Slot(bool)
    def set_live_fpz_positions(self, message):
        self.live_predicted_nziz_positions = message


    # This is not the predicted position, rather it will show positions of
    # electrode with optitrack markers
    @Slot(np.ndarray)
    def show_electrode_positions(self, message):
        self.scatter.removeSeries(self.all_markers_series) # remove the old position
        self.all_markers_series = self.create_new_scatter_series(self.grey_qcolor, self.itemsize)
        self.add_list_to_scatterdata(self.all_markers_series, message)
        self.scatter.addSeries(self.all_markers_series)
        self.scatter.show()

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


if __name__ == '__main__':  
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())