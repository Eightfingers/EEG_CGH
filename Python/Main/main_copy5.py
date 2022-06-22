import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread, QObject, 
                            QWaitCondition, Slot, QSize, QTimer)
from PySide6.QtGui import QGuiApplication, QVector3D, QColor
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QLabel, QBoxLayout
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem, QAbstract3DGraph,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem, QCustom3DLabel)
import numpy as np
from matlab_thread import MatlabMainThread
from menu_widget import MenuWidget
from status_widget import StatusWidget
from optitrack_thread import OptitrackMainThread
from scipy.spatial.transform import Rotation as R
from debug_trace import trace_main
from eeg_positions import EEGPosition
from app_configs import AppConfigs
from app_signals import AppSignals
import pandas as pd

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
# Qt

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.debug = False

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
        self.starting_axis_point_size = 0.15

        self.threshold_placement_range = 0.020# 0.017 

        # Each of this series is used to represent data on the graph
        self.NZIZpoints_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.zeropoint_series = self.create_new_scatter_series(self.red_qcolor, self.starting_axis_point_size)
        self.NZIZscatter_series_trace = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.CIRCUMscatter_series_trace = self.create_new_scatter_series(self.green_qcolor, self.itemsize)
        self.EarToEarscatter_series_trace = self.create_new_scatter_series(self.black_qcolor, self.itemsize)
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize)
        self.specs_series = self.create_new_scatter_series(self.black_qcolor, self.itemsize)
        self.stylus_position_series = self.create_new_scatter_series(self.yellow_qcolor, self.itemsize)

        self.reflmarkers_not_near_predict_series = self.create_new_scatter_series(self.grey_qcolor, self.itemsize)
        self.reflective_markers_position_series = self.create_new_scatter_series(self.grey_qcolor, self.itemsize)
        self.reflmarkers_near_predicted_series = self.create_new_scatter_series(self.green_qcolor, self.itemsize)

        # Variables to hold data
        # Predicted positions
        self.predicted_positions = None # all predicted positions
        self.predicted_positions_to_draw = None # predicted positions that is not near reflective markers
        self.eeg_list = [] # Holds EEG positions

        self.reflective_markers_positions = np.array([[0,0,0], [0,0,0]]) # all reflective marker positions
        self.reflective_markers_positions_to_draw = None # for those that are not near the predicted positions
        self.reflmarkers_in_predicted_positions = None # A list to store reflective markers in predicted positions
        self.global_predicted_eeg_positions = None

        self.fpz_positon = None

        # Trace data
        self.NZIZ_data = None
        self.NZIZ_specs_data = None
        self.NZIZ_specs_rotate = None
        self.CIRCUM_data = None
        self.CIRCUM_specs_data = None
        self.CIRCUM_specs_rotate = None
        self.EarToEar_data = None
        self.EarToEar_specs_data = None
        self.EarToEar_specs_rotate = None

        # Used to hold latest specs / stylus latest position or rotation
        self.specs_live_position = None
        self.specs_live_rotation = None
        self.live_stylus_position = None

        self.signals_to_status = AppSignals()

        # Matlab array order
        # predicted = [Fpz; Fp2; F8; T4; T6; O2; Oz; O1; T5; T3; F7; Fp1; Fz; Cz; Pz; C4; C3; F4; F3; P3; P4 ];
        self.predicted_names_order = ["Fpz", "Fp2", "F8", "T4", "T6", "O2", "Oz", "O1", "T5", "T3", "F7", "Fp1", "Fz", "Cz", "Pz", "C4", "C3", "F4", "F3", "P3", "P4"]

        self.NZIZ_BUTTON = 1
        self.CIRCUM_BUTTON = 2
        self.EARTOEAR_BUTTON = 3

        # Modes
        self.app_mode = AppConfigs.mode_idle
        self.live_predicted_eeg_positions = False
        self.live_predicted_nziz_positions = False
        self.live_reflective_markers = False

        # Set the axis properties
        self.segment_count = 8
        self.sub_segment_count = 2
        self.axis_minimum = -0.8
        self.axis_maximum = 0.8
        self.x_axis = self.create_axis('X', self.segment_count, self.sub_segment_count, self.axis_minimum, self.axis_maximum)
        self.scatter.setAxisX(self.x_axis)
        self.y_axis = self.create_axis('Y', self.segment_count, self.sub_segment_count, self.axis_minimum, self.axis_maximum)
        self.scatter.setAxisY(self.y_axis)
        self.z_axis = self.create_axis('Z', self.segment_count, self.sub_segment_count, self.axis_minimum, self.axis_maximum)
        self.scatter.setAxisZ(self.z_axis)

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

        self.left_dock_status_widget = StatusWidget(self)
        self.left_dock_main_layout.addLayout(self.status_layout)
        
        self.left_dock_menu_widget = MenuWidget(self)
        self.left_dock_main_layout.addLayout(self.menu_layout)

        self.left_dock_main_widget.setLayout(self.left_dock_main_layout)
        self.left_dock.setWidget(self.left_dock_main_widget)

        # Once menu and status layout is initialized update the app mode to idle
        self.signals_to_status.signal_list.connect(self.left_dock_status_widget.change_label) # change label function is found in status_widget.py
        self.signals_to_status.signal_list.emit(["Mode", AppConfigs.mode_idle])

        # Start the main thread
        self.matlab_main_thread = MatlabMainThread(self)
        self.matlab_main_thread.start()

        # Start the Optitrack Thread
        self.optitrack_main_thread = OptitrackMainThread(self)
        self.optitrack_main_thread.start()  
        
        # Now connect and initialize the Signals in the MenuWidget with the threads
        self.left_dock_menu_widget.connect_matlab_signals(self.matlab_main_thread)
        self.left_dock_menu_widget.connect_optitrack_signals(self.optitrack_main_thread)

        # self.scatter.addSeries(self.zeropoint_series)
        # self.add_list_to_scatterdata(self.zeropoint_series, np.array([[0,0,0]]))
        self.scatter.addSeries(self.stylus_position_series)
        self.scatter.addSeries(self.specs_series)
        self.scatter.addSeries(self.reflective_markers_position_series)
        self.scatter.addSeries(self.reflmarkers_not_near_predict_series)
        self.scatter.addSeries(self.reflmarkers_near_predicted_series)
        self.scatter.addSeries(self.CIRCUMscatter_series_trace)
        self.scatter.addSeries(self.NZIZscatter_series_trace)
        self.scatter.addSeries(self.EarToEarscatter_series_trace)

        # Start the timer to periodically update plot data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(50)

    # Update the scatter plot with the new data
    def update_plot_data(self):

        # Helper funcs
        def animate_21_predicted_points_in_global_frame():
            if self.Predicted21_series not in self.scatter.seriesList():
                self.draw_21_predicted_positions()
            else:
                self.Predicted21_series.dataProxy().removeItems(0,self.Predicted21_series.dataProxy().itemCount())
                self.draw_21_predicted_positions()

        def animate_fpz_in_global_frame():
            if self.NZIZpoints_series not in self.scatter.seriesList():
                self.scatter.addSeries(self.NZIZpoints_series)
                self.draw_fpz_positions()
            else:
                self.NZIZpoints_series.dataProxy().removeItems(0,self.NZIZpoints_series.dataProxy().itemCount())
                self.draw_fpz_positions()

        # This is activated to place electrode markers on the head
        def animate_reflective_markers_attaching():
            if self.near_predicted_points(self.reflective_markers_positions):  # Remove predicted_positions which are near reflective markers
                trace_main("Detected reflective markers near positions")
                trace_main("Predicted positions:\n {}".format(self.predicted_positions))
                trace_main("Predicted positions to draw: \n {}".format(self.predicted_positions_to_draw))
                # remove the old position if near
                if self.reflmarkers_not_near_predict_series in self.scatter.seriesList():
                    self.reflmarkers_not_near_predict_series.dataProxy().removeItems(0,self.reflmarkers_not_near_predict_series.dataProxy().itemCount())
                if self.reflmarkers_near_predicted_series in self.scatter.seriesList():
                    self.reflmarkers_near_predicted_series.dataProxy().removeItems(0,self.reflmarkers_near_predicted_series.dataProxy().itemCount())
                if self.reflective_markers_position_series in self.scatter.seriesList():
                    self.reflective_markers_position_series.dataProxy().removeItems(0,self.reflective_markers_position_series.dataProxy().itemCount())
                self.add_list_to_scatterdata(self.reflmarkers_near_predicted_series, self.reflmarkers_in_predicted_positions)
                self.add_list_to_scatterdata(self.Predicted21_series, self.predicted_positions_to_draw)
                self.add_list_to_scatterdata(self.reflmarkers_not_near_predict_series, self.reflective_markers_positions_to_draw)
                
            else: # None of them are near reflective markers
                # Remove those old positions
                if self.reflmarkers_not_near_predict_series in self.scatter.seriesList():
                    self.reflmarkers_not_near_predict_series.dataProxy().removeItems(0,self.reflmarkers_not_near_predict_series.dataProxy().itemCount())
                if self.reflmarkers_near_predicted_series in self.scatter.seriesList():
                    self.reflmarkers_near_predicted_series.dataProxy().removeItems(0,self.reflmarkers_near_predicted_series.dataProxy().itemCount())
                if self.reflective_markers_position_series in self.scatter.seriesList():
                    self.reflective_markers_position_series.dataProxy().removeItems(0,self.reflective_markers_position_series.dataProxy().itemCount())

                # Show those reflective markers that are not near predicted point
                # self.reflmarkers_not_near_predict_series = self.create_new_scatter_series(self.grey_qcolor, self.itemsize)
                # self.add_list_to_scatterdata(self.reflmarkers_not_near_predict_series, self.reflective_markers_positions_to_draw)
                self.add_list_to_scatterdata(self.reflmarkers_not_near_predict_series, self.reflective_markers_positions_to_draw)

                trace_main("reflective markers to draw are: \n {}".format(self.reflective_markers_positions_to_draw))

        # remove items with old positions on the series
        self.remove_series_items(self.stylus_position_series)
        self.remove_series_items(self.specs_series)

        # Add items to the new series
        self.add_list_to_scatterdata(self.stylus_position_series, self.live_stylus_position)
        self.add_list_to_scatterdata(self.specs_series, self.specs_live_position)

        if self.app_mode == AppConfigs.mode_idle:
            # Show only the position of the glasses and stylus remove the rest
            self.remove_series_items(self.reflmarkers_not_near_predict_series)
            self.remove_series_items(self.reflmarkers_near_predicted_series)
            self.remove_series_items(self.reflective_markers_position_series)
            # self.remove_series_items(self.NZIZpoints_series)
            self.remove_series_items(self.Predicted21_series)
            self.delete_labels()
            # self.remove_series_items(self.NZIZscatter_series_trace)
            # self.remove_series_items(self.CIRCUMscatter_series_trace)
            # self.remove_series_items(self.EarToEarscatter_series_trace)
        elif self.app_mode == AppConfigs.mode_show_trace:
            # Show only trace
            self.remove_series_items(self.reflmarkers_not_near_predict_series)
            self.remove_series_items(self.reflmarkers_near_predicted_series)
            self.remove_series_items(self.reflective_markers_position_series)
            self.remove_series_items(self.NZIZpoints_series)
            # self.remove_series_items(self.Predicted21_series)
            # self.delete_labels()
            # self.remove_series_items(self.NZIZscatter_series_trace)
            # self.remove_series_items(self.CIRCUMscatter_series_trace)
            # self.remove_series_items(self.EarToEarscatter_series_trace)
        elif self.app_mode == AppConfigs.mode_show_NZIZ:
            self.remove_series_items(self.reflmarkers_not_near_predict_series)
            self.remove_series_items(self.reflmarkers_near_predicted_series)
            self.remove_series_items(self.reflective_markers_position_series)
            # self.remove_series_items(self.NZIZpoints_series)
            self.remove_series_items(self.Predicted21_series)
            animate_fpz_in_global_frame()
            # self.remove_series_items(self.NZIZscatter_series_trace)
            # self.remove_series_items(self.CIRCUMscatter_series_trace)
            # self.remove_series_items(self.EarToEarscatter_series_trace)
            # Show only NZIZ
        elif self.app_mode == AppConfigs.mode_show_21:
            # Show only 21
            self.remove_series_items(self.reflmarkers_not_near_predict_series)
            self.remove_series_items(self.reflmarkers_near_predicted_series)
            self.remove_series_items(self.reflective_markers_position_series)
            self.remove_series_items(self.NZIZpoints_series)
            # self.remove_series_items(self.Predicted21_series)
            self.remove_series_items(self.NZIZscatter_series_trace)
            self.remove_series_items(self.CIRCUMscatter_series_trace)
            self.remove_series_items(self.EarToEarscatter_series_trace)
            animate_21_predicted_points_in_global_frame()
        elif self.app_mode == AppConfigs.mode_attach_electrode:
            # Show predicted with reflective markers
            # self.remove_series_items(self.reflmarkers_not_near_predict_series)
            # self.remove_series_items(self.reflmarkers_near_predicted_series)
            # self.remove_series_items(self.reflective_markers_position_series)
            self.remove_series_items(self.NZIZpoints_series)
            # self.remove_series_items(self.Predicted21_series)
            # self.remove_series_items(self.NZIZscatter_series_trace)
            # self.remove_series_items(self.CIRCUMscatter_series_trace)
            # self.remove_series_items(self.EarToEarscatter_series_trace)
            animate_reflective_markers_attaching()
            animate_21_predicted_points_in_global_frame()

        # if self.live_predicted_nziz_positions == True:
        #     if self.NZIZpoints_series not in self.scatter.seriesList():
        #         self.NZIZpoints_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        #         self.scatter.addSeries(self.NZIZpoints_series)
        #         self.global_predicted_nziz_positions = self.transform_spec_to_global_frame(self.fpz_positon, self.specs_live_rotation, self.specs_live_position)
        #         self.add_list_to_scatterdata(self.NZIZpoints_series, self.global_predicted_nziz_positions)
        #     else:
        #         self.global_predicted_nziz_positions = self.transform_spec_to_global_frame(self.fpz_positon, self.specs_live_rotation, self.specs_live_position)
        #         self.add_list_to_scatterdata(self.NZIZpoints_series, self.global_predicted_nziz_positions)
        # else:
        #     if self.NZIZpoints_series in self.scatter.seriesList():
        #         remove_series_items(self.NZIZpoints_series)

        self.scatter.show()

    def draw_labels(self):
        self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_live_rotation, self.specs_live_position)
        idx = 0
        
        for eeg_position in self.global_predicted_eeg_positions:
            self.customlabel1 = QCustom3DLabel(text= self.eeg_list[idx].name, position=QVector3D(eeg_position[0]+0.015, eeg_position[1]+0.025, eeg_position[2]), scaling=QVector3D(0.5,0.5,0.5)) 
            self.customlabel1.setFacingCamera(True)
            self.scatter.addCustomItem(self.customlabel1)
            idx += 1

        self.scatter.show()
    def delete_labels(self):
        if self.scatter.customItems().count == 0:
            pass 
        else:
            self.scatter.removeCustomItems()

    def update_label_position(self): 
        if self.scatter.customItems().count == 0:
            self.draw_labels()
            return
        idx = 0
        for eeg_position in self.global_predicted_eeg_positions:
            position = QVector3D(eeg_position[0]+0.015, eeg_position[1]+0.025, eeg_position[2])
            self.scatter.customItems()[idx].setPosition(position)
            idx += 1

    def remove_series_items(self,series):
        if series in self.scatter.seriesList():
            series.dataProxy().removeItems(0,series.dataProxy().itemCount())

    def draw_21_predicted_positions(self):
        self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_live_rotation, self.specs_live_position)
        self.add_list_to_scatterdata(self.Predicted21_series, self.global_predicted_eeg_positions)
        self.update_label_position()

    def draw_fpz_positions(self):
        self.global_fpz_positions = self.transform_spec_to_global_frame(self.fpz_positon, self.specs_live_rotation, self.specs_live_position)
        self.add_list_to_scatterdata(self.NZIZpoints_series, self.global_fpz_positions)


    @Slot(float)
    def adjust_axis_min_max(self, message):
        position = message / 10
        # Make bigger range
        self.scatter.axisX().setRange(self.axis_minimum - position, self.axis_maximum + position)
        self.scatter.axisY().setRange(self.axis_minimum - position, self.axis_maximum + position)
        self.scatter.axisZ().setRange(self.axis_minimum - position, self.axis_maximum + position)

    @Slot(bool)
    def show_trace_data(self, message):
        if message == True:
            self.app_mode = AppConfigs.mode_show_trace

            NZIZ_trace_data =  np.genfromtxt('data_NZIZstylus.csv', delimiter=',')
            self.add_list_to_scatterdata(self.NZIZscatter_series_trace, NZIZ_trace_data)

            CIRCUM_trace_data =  np.genfromtxt('data_CIRCUMstylus.csv', delimiter=',')
            self.add_list_to_scatterdata(self.CIRCUMscatter_series_trace, CIRCUM_trace_data)

            EarToEar_trace_data =  np.genfromtxt('data_EarToEarstylus.csv', delimiter=',')
            self.add_list_to_scatterdata(self.EarToEarscatter_series_trace, EarToEar_trace_data)
        else:
            self.app_mode = AppConfigs.mode_show_21

    # Function that is called from the menu widget to save trace data into csv files
    @Slot(int)
    def save_trace_data (self, message):
        # Get the data from the optitrack thread
        self.app_mode = AppConfigs.mode_show_trace
        self.stylus_data = self.optitrack_main_thread.stylus_data 
        self.specs_trace_position = self.optitrack_main_thread.specs_data 
        self.specs_trace_rotation = self.optitrack_main_thread.specs_rotation_data

        #strip of all the zeroes
        self.stylus_data = self.stylus_data[~np.all(self.stylus_data == 0, axis=1)]
        self.specs_trace_position = self.specs_trace_position[~np.all(self.specs_trace_position == 0, axis=1)]
        self.specs_trace_rotation = self.specs_trace_rotation[~np.all(self.specs_trace_rotation == 0, axis=1)]

        if (message == self.NZIZ_BUTTON): # NZIZ
            self.NZIZ_data = self.stylus_data
            self.NZIZ_specs_data = self.specs_trace_position
            self.NZIZ_specs_rotate = self.specs_trace_rotation

            trace_main("Saving NZIZ data")
            np.savetxt("data_NZIZstylus.csv", self.NZIZ_data, delimiter=',')
            np.savetxt("data_NZIZspecs.csv", self.NZIZ_specs_data, delimiter=',')
            np.savetxt("rotation_data_NZIZspecs.csv", self.NZIZ_specs_rotate, delimiter=',')

            self.stylus_data[:,0] *= -1 # Rectify the x axis
            self.update_and_add_scatterNZIZ(self.stylus_data)

        elif (message == self.CIRCUM_BUTTON): # Circum
            self.CIRCUM_data = self.stylus_data
            self.CIRCUM_specs_data = self.specs_trace_position
            self.CIRCUM_specs_rotate = self.specs_trace_rotation

            trace_main("Saving Circum data")
            np.savetxt("data_CIRCUMstylus.csv", self.CIRCUM_data, delimiter=',')
            np.savetxt("data_CIRCUMspecs.csv", self.CIRCUM_specs_data, delimiter=',')
            np.savetxt("rotation_data_CIRCUMspecs.csv", self.CIRCUM_specs_rotate, delimiter=',')

            self.stylus_data[:,0] *= -1 # Rectify the x axis
            self.update_and_add_scatterCIRCUM(self.stylus_data)

        elif (message == self.EARTOEAR_BUTTON): # Ear to Ear
            self.EartoEar_data = self.stylus_data
            self.EartoEar_specs_data = self.specs_trace_position
            self.EartoEar_specs_rotate = self.specs_trace_rotation

            trace_main("Saving Ear to Ear data")
            np.savetxt("data_EarToEarstylus.csv", self.EartoEar_data, delimiter=',')
            np.savetxt("data_EarToEarspecs.csv", self.EartoEar_specs_data, delimiter=',')
            np.savetxt("rotation_data_EarToEarspecs.csv", self.EartoEar_specs_rotate, delimiter=',')

            self.stylus_data[:,0] *= -1 # Rectify the x axis
            self.update_and_add_scatterEarToEar(self.stylus_data)

    # Clear all data shown in the graph
    @Slot()
    def clear_data(self):
        # set it to false
        self.app_mode = AppConfigs.mode_idle
        self.live_predicted_eeg_positions = False
        self.live_predicted_nziz_positions = False

        if self.NZIZpoints_series in self.scatter.seriesList():
            self.scatter.removeSeries(self.NZIZpoints_series) 
        if self.NZIZscatter_series_trace in self.scatter.seriesList():
            self.scatter.removeSeries(self.NZIZscatter_series_trace) 
        if self.CIRCUMscatter_series_trace in self.scatter.seriesList():
            self.scatter.removeSeries(self.CIRCUMscatter_series_trace)
        if self.EarToEarscatter_series_trace in self.scatter.seriesList():
            self.scatter.removeSeries(self.EarToEarscatter_series_trace)
        if self.Predicted21_series in self.scatter.seriesList():
            self.scatter.removeSeries(self.Predicted21_series)
        if self.reflective_markers_position_series in self.scatter.seriesList():
            self.scatter.removeSeries(self.reflective_markers_position_series)

        self.delete_labels()

        self.NZIZpoints_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.NZIZscatter_series_trace = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.CIRCUMscatter_series_trace = self.create_new_scatter_series(self.green_qcolor, self.itemsize)
        self.EarToEarscatter_series_trace = self.create_new_scatter_series(self.black_qcolor, self.itemsize)
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.itemsize)
        
        trace_main("Run finished!")

    @Slot(np.ndarray)
    def update_save_predicted_eeg_positions(self, message):
        self.predicted_positions = message
        self.predicted_positions[:,0]  *= -1
        np.savetxt("21_predicted_positions_specs_frame_from_copy_py.csv", message, delimiter=',')
        if self.Predicted21_series in self.scatter.seriesList():
            self.remove_series_items(self.Predicted21_series)
        idx = 0
        for position in message:
            self.eeg_list.append(EEGPosition(position, self.predicted_names_order[idx]))
            idx += 1
        for eeg_position in self.eeg_list:
            trace_main("The eeg position is: {} name is: {}".format(eeg_position.position, eeg_position.name))

        self.remove_series_items(self.Predicted21_series)
        self.add_list_to_scatterdata(self.Predicted21_series, self.predicted_positions)
        self.scatter.addSeries(self.Predicted21_series)

        self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_live_rotation, self.specs_live_position)
        self.draw_labels()
        np.savetxt("21_predicted_positions_global_frame_from_copy_py.csv", message, delimiter=',')

    @Slot(np.ndarray)
    def update_fpz_position(self, message):
        self.fpz_positon = message
        self.fpz_positon[:,0]  *= -1 # Rectify the x axis
        self.NZIZpoints_series = self.create_new_scatter_series(self.red_qcolor, self.itemsize)
        self.add_list_to_scatterdata(self.NZIZpoints_series, self.fpz_positon)

    @Slot(np.ndarray)
    def update_current_stylus_position(self, message):
        message[0] *= -1 
        self.live_stylus_position = message 

    @Slot(list)
    def update_current_specs_position_rotation(self, message):
        self.specs_live_position = message[0]
        self.specs_live_position[0] *= -1
        self.specs_live_rotation = message[1]
        self.specs_live_rotation[1]*= -1
        self.specs_live_rotation[2]*= -1

    @Slot(np.ndarray)
    def update_reflective_markers_positions(self, message):
        message[:,0] *= -1 # Rectify the x axis to match qt
        self.reflective_markers_positions = message

    @Slot(np.ndarray)
    def update_and_add_scatterNZIZ(self, message):
        trace_main("Update and scattering done!")
        self.add_list_to_scatterdata(self.NZIZscatter_series_trace, message)
        self.scatter.show()

    @Slot(np.ndarray)
    def update_and_add_scatterCIRCUM(self, message):
        self.add_list_to_scatterdata(self.CIRCUMscatter_series_trace, message)
        self.scatter.show()

    @Slot(np.ndarray)
    def update_and_add_scatterEarToEar(self, message):
        self.add_list_to_scatterdata(self.EarToEarscatter_series_trace, message)
        self.scatter.show()

    @Slot(bool)
    def set_live_predicted_eeg_positions(self, message):
        self.live_predicted_eeg_positions = message
        if self.live_predicted_eeg_positions == True:
            self.app_mode = AppConfigs.mode_show_21
            self.signals_to_status.signal_list.emit(["Mode", AppConfigs.mode_show_21])

    @Slot(bool)
    def set_reflective_markers(self, message):
        trace_main("Reflective Markers can be seen now!")
        self.live_reflective_markers = message
        if self.live_reflective_markers == True:
            self.app_mode = AppConfigs.mode_attach_electrode
            self.signals_to_status.signal_list.emit(["Mode", AppConfigs.mode_show_21])
        else:
            self.app_mode = AppConfigs.mode_show_21

    @Slot(bool)
    def set_live_fpz_positions(self, message):
        self.live_predicted_nziz_positions = message
        if self.live_predicted_nziz_positions == True:
            self.app_mode = AppConfigs.mode_show_NZIZ
        
    def add_list_to_scatterdata(self, scatter_series, data):
        if data is None:
            pass
        elif data.ndim == 1: # if its one dimensional
            scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(data[0], data[1], data[2])))
        else:
            for d in data:
                scatter_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[1], d[2])))

    def create_new_scatter_series(self, colour, size):
        scatter_series_new_series = QScatter3DSeries()
        scatter_series_new_series.setBaseColor(colour)
        scatter_series_new_series.setItemSize(size)

        return scatter_series_new_series

    def create_axis(self, title, segment_count, sub_segment_count, axis_min, axis_max):
        new_axis = QValue3DAxis()
        new_axis.setTitle(title)
        new_axis.setTitleVisible(True)
        new_axis.setSegmentCount(segment_count)
        new_axis.setRange(axis_min, axis_max)
        new_axis.setSubSegmentCount(sub_segment_count)

        return new_axis

    # Used in the predicted data set
    def transform_spec_to_global_frame(self, predicted_positions, specs_rotation, specs_position):
        # DIfference between optitrack and qt
        r = R.from_quat(specs_rotation) # rotate the orientation back to the axis
        new_predicted_positions = r.apply(predicted_positions)
        new_predicted_positions = new_predicted_positions + specs_position # Add the offset
        return new_predicted_positions

    # Remove markers which are near reflective markers
    def near_predicted_points(self, sample_data):
        predicted_positions_to_remove = []
        tmp_reflmarkers_near_predicted = [] # contains all the reflective markers that are near the predicted positions
        sucess = False
        for sample in sample_data: 
            for position in self.global_predicted_eeg_positions:
                magnitude_difference = np.absolute(np.linalg.norm(sample - position))
                # print("position is ", position, "Sample is ", sample, " magnitude diff is: ", magnitude_difference)

                if magnitude_difference < self.threshold_placement_range:
                    predicted_positions_to_remove.append(np.array(position))
                    tmp_reflmarkers_near_predicted.append(np.array(sample))
                    sucess = True
        if sucess:
            np_predicted_positions_to_remove = np.array(predicted_positions_to_remove)
            self.reflmarkers_in_predicted_positions = np.array(tmp_reflmarkers_near_predicted)

            ## I couldn't find a built in numpy function remove a specific subarray from a numpy array so...
            # find the predicted positions to remove
            self.predicted_positions_to_draw = self.global_predicted_eeg_positions
            index = 0
            idx_positions1 = []
            for predicted_position in self.predicted_positions_to_draw:
                for position_to_remove in np_predicted_positions_to_remove:
                    # print(position_to_remove, predicted_position)
                    if np.equal(position_to_remove,predicted_position).all(): 
                        idx_positions1.append(index)
                index += 1 
            
            # find the refl markers position to remove
            self.reflective_markers_positions_to_draw = self.reflective_markers_positions
            index = 0
            idx_positions2 = []
            for reflmarkers_position in self.reflective_markers_positions_to_draw:
                for position_to_remove in self.reflmarkers_in_predicted_positions:
                    if np.equal(position_to_remove, reflmarkers_position).all():
                        idx_positions2.append(index)
                index += 1 
            self.predicted_positions_to_draw = np.delete(self.predicted_positions_to_draw, idx_positions1, 0)
            self.reflective_markers_positions_to_draw = np.delete(self.reflective_markers_positions_to_draw, idx_positions2, 0)

            trace_main("Predicted positions to draw: {} \n".format(self.predicted_positions_to_draw))
            trace_main("Reflective marker positions to draw:\n {}".format(self.reflective_markers_positions_to_draw))
        else:
            self.predicted_positions_to_draw = self.predicted_positions
            self.reflective_markers_positions_to_draw = self.reflective_markers_positions
        return sucess

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())