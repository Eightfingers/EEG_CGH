import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import matlab.engine
from PythonClient.NatNetClient import NatNetClient
from app_signals import AppSignals

# Create the main Thread
class OptitrackMainThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self.streamingClient = NatNetClient()

        self.signals_to_status = AppSignals()
        self.signals_to_main = AppSignals()
        self.signals_to_main.signal_numpy.connect(parent.show_current_stylus_position)
        self.signals_to_status.signal_list.connect(parent.left_dock_status_widget.change_label)

        # Control variables 
        self.record = False
        self.stylus_record = None
        self.specs_record = None
        self.stylus_lose_track_counter = 0
        self.specs_lose_track_counter = 0

        self.stylus_previous_position = np.array([0,0,0])
        self.specs_previous_position = np.array([0,0,0])

        # Allocate numpy array for rigidbody data
        self.row = 2000 # max number of data sets
        self.columns = 3 #
        self.rot_columns = 4 # quaternions

        self.index_counter = 0 # used to loopthrough numpy array and replace the values inside
        self.stylus_position = np.zeros((0, 0, 0))
        self.stylus_data = np.zeros(shape=[self.row, self.columns])
        self.specs_data = np.zeros(shape=[self.row, self.columns])
        self.specs_rotation_data = np.zeros(shape=[self.row, self.rot_columns])

    def run(self):
        try:
            # Configure the streaming client to call our rigid body handler on the emulator to send data out.
            self.streamingClient.newFrameListener = self.receiveNewFrame
            self.streamingClient.rigidBodyListener = self.receiveRigidBodyFrame
            # Start up the streaming client now that the callbacks are set up.
            # This will run perpetually, and operate on a separate thread.
            self.streamingClient.run()
            self.signals_to_status.signal_list.emit(["Optitrack","Okay"])
        except ConnectionResetError:
            print("Optitrack: Optitrack thread returned an error")

    # This is a callback function that gets connected to the NatNet client and called once per mocap frame.
    def receiveNewFrame(self, frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        # print( "Received frame", frameNumber )
        pass 

    # This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
    def receiveRigidBodyFrame(self, id, position, rotation ):
        # print( "Received frame for rigid body", id )
        # print(id, position)
        position = np.round(position, 5)
        rotation = np.round(rotation, 5)
        if (id == 1004):
            self.stylus_position = position 
            self.signals_to_main.signal_numpy.emit(position)
            if self.record == True: # Record the positions into numpy array
                self.stylus_data[self.index_counter,:] = position
                if np.all(self.stylus_previous_position != position):  # if its not the same as the old position update to the new position
                    self.stylus_previous_position = position 
                    self.signals_to_status.signal_list.emit(["Stylus","Detected"])
                    self.stylus_lose_track_counter = 0
                else:  # if the new position is the same as the old one, there is a big chance that it has lost detection.
                    self.stylus_lose_track_counter += 1
                    print("Optitrack: Stylus is not detected!")
                    if (self.stylus_lose_track_counter > 100):
                        self.signals_to_status.signal_list.emit(["Stylus","Lost detection"])
        elif (id == 1005):
            if self.record == True:
                self.specs_data[self.index_counter,:] = position
                self.specs_rotation_data[self.index_counter,:] = rotation
                self.index_counter += 1 # Increment the index counter everytime the final rigidbody is sent
                if np.all(self.specs_previous_position != position): 
                    self.specs_previous_position = position 
                    self.signals_to_status.signal_list.emit(["Specs","Detected"])
                    self.specs_lose_track_counter = 0
                else:
                    self.specs_lose_track_counter += 1
                    print("Optitrack: Specs is not detected!!")
                    if (self.specs_lose_track_counter > 100):
                        self.signals_to_status.signal_list.emit(["Specs","Lost detection"])

        # print("Optitrack: index counter is at", self.index_counter)
        if self.index_counter > self.row:
            print("Optitrack: Overflow of data!") 
            
    @Slot()
    def spawn_thread(self, message):
        print("Optitrack: Spawn matlab thread called!!!")
        print(message)

    @Slot(bool)
    def set_recording(self, message):
        self.record = message
        if (message == False):
            self.clear_data()

    def clear_data(self):
        self.index_counter = 0
        self.stylus_data = np.zeros(shape=[self.row, self.columns])
        self.specs_data = np.zeros(shape=[self.row, self.columns])

