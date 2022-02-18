import sys
from PySide6.QtCore import (Signal, QMutex, QElapsedTimer, QMutexLocker,
                            QPoint, QPointF, QSize, Qt, QThread,
                            QWaitCondition)
from PySide6.QtGui import QGuiApplication, QVector3D, QColor
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget
from PySide6.QtDataVisualization import (Q3DBars, Q3DScatter, QBar3DSeries, QBarDataItem,
                                         QCategory3DAxis, QScatter3DSeries, QValue3DAxis, QScatterDataItem)
import numpy as np

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Qt DataVisualization 3D scatter')
        self.threshold_placement_range = 0.17

        self.scatter = Q3DScatter()

        # Predicted positions
        self.predicted_positions = None
        self.fpz_positon = None
        self.reflective_markers_positions = None 

        self.reflmarkers_in_predicted_positions = None # A list to store reflective markers in predicted positions
        self.reflective_markers_positions_to_draw = None
        self.predicted_positions_to_draw = None

        self.x_axis = QValue3DAxis()
        self.x_axis.setTitle('X')
        self.x_axis.setTitleVisible(True)

        self.y_axis = QValue3DAxis()
        self.y_axis.setTitle('Y')
        self.y_axis.setTitleVisible(True)    

        self.z_axis = QValue3DAxis()
        self.z_axis.setTitle('Z')
        self.z_axis.setTitleVisible(True)

        self.scatter.setAxisX(self.x_axis)
        self.scatter.setAxisY(self.y_axis)
        self.scatter.setAxisZ(self.z_axis)

        # create 10000 random spatial positions 
        self.predicted_positions = np.array([[10,10,10], [5,5,5], [1,1,1]])
        self.reflective_markers_positions = np.array([[10.13,10,10], [1.13,1,1], [2,2,2], [3,3,3]])

        self.predicted_series = QScatter3DSeries()
        self.predicted_series.setBaseColor(QColor(255, 165, 0))

        self.reflmarkers_not_near_predict = QScatter3DSeries()
        self.reflmarkers_not_near_predict.setBaseColor(QColor(128,128,128))

        self.reflmarkers_near_predicted = QScatter3DSeries()
        self.reflmarkers_near_predicted.setBaseColor(QColor(0, 255, 0))

        self.container = QWidget.createWindowContainer(self.scatter)
        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.container.setMinimumSize(size, size)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        
        self.setCentralWidget(self.container)

        if (self.predicted_series.dataProxy().itemCount() != 0 ):
            print("The number of items is.. ", self.predicted_series.dataProxy().itemCount())

        if self.near_predicted_points(self.reflective_markers_positions):
            print("Detected reflective markers near positions")

        print("Predicted positions to draw", self.predicted_positions_to_draw)
        print("Reflective positions to draw", self.reflective_markers_positions_to_draw)
        print("Reflective positions near predicted positions", self.reflmarkers_in_predicted_positions)

        self.predicted_series.setItemSize(0.15)
        self.add_list_to_scatterdata(self.predicted_series, self.predicted_positions_to_draw)
        self.scatter.addSeries(self.predicted_series)

        self.reflmarkers_near_predicted.setItemSize(0.15)
        self.add_list_to_scatterdata(self.reflmarkers_near_predicted, self.reflmarkers_in_predicted_positions)
        self.scatter.addSeries(self.reflmarkers_near_predicted)

        self.reflmarkers_not_near_predict.setItemSize(0.15)
        self.add_list_to_scatterdata(self.reflmarkers_not_near_predict, self.reflective_markers_positions_to_draw)
        self.scatter.addSeries(self.reflmarkers_not_near_predict)

        camera = self.scatter.scene().activeCamera()
        camera.setYRotation(25)
        self.scatter.show()
        self.NZIZ_specs_rotation = np.array([0,0,0,0])

    def add_list_to_scatterdata(self, predicted_series, data):
        if data is None:
            pass
        elif data.size == 0:
            pass
        elif data.size == 1: # if its one dimensional
            predicted_series.dataProxy().addItem(QScatterDataItem(QVector3D(data[0], data[1], data[2])))
        else:
            for d in data:
                predicted_series.dataProxy().addItem(QScatterDataItem(QVector3D(d[0], d[1], d[2])))

    # Remove markers which are near reflective markers
    def near_predicted_points(self, sample_data):
        predicted_positions_to_remove = []
        tmp_reflmarkers_near_predicted = [] # contains all the reflective markers that are near the predicted positions
        sucess = False

        for sample in sample_data:  
            for position in self.predicted_positions:
                magnitude_difference = np.absolute(np.linalg.norm(sample - position))
                print("position is ", position, "Sample is ", sample, " magnitude diff is: ", magnitude_difference)

                if magnitude_difference < self.threshold_placement_range:
                    predicted_positions_to_remove.append(np.array(position))
                    tmp_reflmarkers_near_predicted.append(np.array(sample))
                    sucess = True

        np_predicted_positions_to_remove = np.array(predicted_positions_to_remove)
        self.reflmarkers_in_predicted_positions = np.array(tmp_reflmarkers_near_predicted)

        ## I couldn't find a built in numpy function remove a specific subarray from a numpy array so...
        # find the predicted positions to remove
        self.predicted_positions_to_draw = self.predicted_positions
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
        # print(idx_positions1)
        # print(idx_positions2)
        return sucess


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
