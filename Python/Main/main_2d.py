import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QPointF, QSize, QStringConverter, Qt, Slot
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

# https://doc.qt.io/qtforpython/PySide6/QtDataVisualization/QAbstract3DGraph.html#PySide6.QtDataVisualization.PySide6.QtDataVisualization.QAbstract3DGraph.currentFps
# Numpy data is processed in Nx3 format

# 2D GUI format

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

        # Size of graph markers
        self.marker_size = 7
        self.bigger_marker_size = 10

        # electrode accuracy placement range 
        self.threshold_placement_range = 0.008 # 0.008m , 8mm 
        self.predicted_eeg_positions_with_electrodes = [] #empty list that contains the 21 predicted positions with reflective markers attached on it
        self.unassigned_electrode_markers = None

        # Axis range
        self.axis_range = 5

        # The 3 scatter series used
        self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.marker_size)
        self.NZIZscatter_series.setName("NZIZ")
        self.coordinates = np.random.randint(self.axis_range * -1, self.axis_range, size=(100, 2)) 
        self.add_list_to_scatterdata2D(self.NZIZscatter_series, self.coordinates)

        self.CIRCUMscatter_series = self.create_new_scatter_series(self.green_qcolor, self.marker_size)
        self.CIRCUMscatter_series.setName("Circumference")
        self.coordinates = np.random.randint(self.axis_range * -1, self.axis_range, size=(100, 2)) 
        self.add_list_to_scatterdata2D(self.CIRCUMscatter_series, self.coordinates)

        self.EarToEarscatter_series = self.create_new_scatter_series(self.blue_qcolor, self.marker_size)
        self.EarToEarscatter_series.setName("Ear to Ear")
        self.coordinates = np.random.randint(self.axis_range * -1, self.axis_range, size=(100, 2)) 
        self.add_list_to_scatterdata2D(self.EarToEarscatter_series, self.coordinates)

        # Axis and Chart properties
        self.axisX = QValueAxis()
        self.axisX.setRange(self.axis_range * -1, self.axis_range)
        self.axisX.setTitleText("X")

        self.axisY = QValueAxis()
        self.axisY.setRange(self.axis_range * -1, self.axis_range)
        self.axisY.setTitleText("Y")

        self.chart = QChart()
        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)
        self.chart.addSeries(self.NZIZscatter_series)
        self.chart.addSeries(self.CIRCUMscatter_series)
        self.chart.addSeries(self.EarToEarscatter_series)
        self.chart.setTitle("Triple Random Scatter")
        self.chart.legend().setAlignment(Qt.AlignTop)
        self.chart.legend().setVisible(True)

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        # Main central widget
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.chart.setMinimumSize(size, size) # GUI size
        self.chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chart.setFocusPolicy(Qt.StrongFocus)

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

        self.setCentralWidget(self._chart_view)

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
        self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.marker_size) # reset the seties
        self.add_list_to_scatterdata2D(self.Predicted21_series, self.predicted_positions)
        self.scatter.addSeries(self.Predicted21_series)

        self.predicted_eeg_positions_global_frame = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_position)
        np.savetxt("21_predicted_positions_global_frame.csv", message, delimiter=',')

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
        self.scatter.removeSeries(self.reflective_markers_series)

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
    def show_current_stylus_position(self, message):
        self.scatter.removeSeries(self.stylus_position_series) # remove the old position
        self.stylus_position_series = self.create_new_scatter_series(self.yellow_qcolor, self.bigger_marker_size)
        self.add_list_to_scatterdata2D(self.stylus_position_series, message)
        self.scatter.addSeries(self.stylus_position_series)
        self.scatter.show()

    @Slot(list)
    def update_current_specs_position_rotation(self, message):
        self.specs_position = message[0]
        self.specs_rotation = message[1]
        self.scatter.removeSeries(self.specs_series) # remove the old position
        self.specs_series = self.create_new_scatter_series(self.black_qcolor, self.bigger_marker_size) # reset the seties
            
        self.add_list_to_scatterdata2D(self.specs_series, self.specs_position)
        self.scatter.addSeries(self.specs_series)
        self.scatter.show()

        if (self.live_predicted_eeg_positions == True):
            # Convert predicted eeg_position from spec frame to global frame 
            self.global_predicted_eeg_positions = self.transform_spec_to_global_frame(self.predicted_positions, self.specs_rotation, self.specs_position)
            self.scatter.removeSeries(self.Predicted21_series) # remove the old series
            self.Predicted21_series = self.create_new_scatter_series(self.orange_qcolor, self.marker_size) # reset the seties
            self.add_list_to_scatterdata2D(self.Predicted21_series, self.global_predicted_eeg_positions)
            self.scatter.addSeries(self.Predicted21_series)
            self.scatter.show()

        if (self.live_predicted_nziz_positions == True):
            # Convert predicted nziz from spec frame to global frame 
            self.global_predicted_nziz_positions = self.transform_spec_to_global_frame(self.fpz_positon, self.specs_rotation, self.specs_position)
            if self.NZIZscatter_series_trace in self.scatter.seriesList():
                self.scatter.removeSeries(self.NZIZscatter_series_trace) # remove the trace if its still there
            self.scatter.removeSeries(self.NZIZscatter_series)
            self.NZIZscatter_series = self.create_new_scatter_series(self.red_qcolor, self.marker_size)
            self.add_list_to_scatterdata2D(self.NZIZscatter_series, self.global_predicted_nziz_positions)
            self.scatter.addSeries(self.NZIZscatter_series)

            self.scatter.show()

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
        self.scatter.removeSeries(self.reflective_markers_series) # remove the old position

        self.reflective_markers_series = self.create_new_scatter_series(self.grey_qcolor, self.marker_size)
        self.reflective_marker_in_eeg_position = self.create_new_scatter_series(self.green_qcolor, self.marker_size) # reflective marker in eeg position

        # Check if the optitrack markers are near any electrode positions
        if self.near_predicted_points(message):
            self.add_list_to_scatterdata2D(self.reflective_marker_in_eeg_position, self.predicted_eeg_positions_with_electrodes)
            self.scatter.addSeries(self.reflective_marker_in_eeg_position)
        else:
            self.add_list_to_scatterdata2D(self.reflective_markers_series, self.unassigned_electrode_markers)
            self.scatter.addSeries(self.reflective_markers_series)
            

        self.scatter.addSeries(self.reflective_markers_series)
        self.scatter.show()

    @Slot(np.ndarray)
    def update_and_add_scatterNZIZ(self, message):
        self.add_list_to_scatterdata2D(self.NZIZscatter_series_trace, message)
        self.scatter.addSeries(self.NZIZscatter_series_trace)
        self.scatter.show()

    @Slot(np.ndarray)
    def update_and_add_scatterCIRCUM(self, message):
        self.add_list_to_scatterdata2D(self.CIRCUMscatter_series, message)
        self.scatter.addSeries(self.CIRCUMscatter_series)
        self.scatter.show()

    @Slot(np.ndarray)
    def update_and_add_scatterEarToEar(self, message):
        self.add_list_to_scatterdata2D(self.EarToEarscatter_series, message)
        self.scatter.addSeries(self.EarToEarscatter_series)
        self.scatter.show()

    def add_list_to_scatterdata2D(self,scatter_series, data):
        for d in data:
            scatter_series.append(d[0], d[1])

    def create_new_scatter_series(self, colour, size):
        self.scatter_series_new_series = QScatterSeries()
        self.scatter_series_new_series.setColor(colour)
        self.scatter_series_new_series.setMarkerSize(size)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.resize(440, 300)
    sys.exit(app.exec())