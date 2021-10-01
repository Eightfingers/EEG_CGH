import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import matlab.engine
from matlab_signal import MatlabSignals
from optitrack_signal import OptitrackSignals
from PythonClient.NatNetClient import NatNetClient


# Create the main Thread
class OptitrackMainThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self.streamingClient = NatNetClient()

        self.status_optitrack_signals = OptitrackSignals()
        self.status_optitrack_signals.signal_list.connect(parent.left_dock_status_widget.change_label)

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
        self.columns = 3
        self.index_counter = 0 # used to loopthrough numpy array and replace the values inside
        self.stylus_data = np.zeros(shape=[self.row, self.columns])
        self.specs_data = np.zeros(shape=[self.row, self.columns])

    def run(self):
        try:
            # Configure the streaming client to call our rigid body handler on the emulator to send data out.
            self.streamingClient.newFrameListener = self.receiveNewFrame
            self.streamingClient.rigidBodyListener = self.receiveRigidBodyFrame
            # Start up the streaming client now that the callbacks are set up.
            # This will run perpetually, and operate on a separate thread.
            self.streamingClient.run()
            self.status_optitrack_signals.signal_list.emit(["Optitrack","Okay"])
        except:
            print("ERROR ON THE OPTITRACKMAIN THREAD")

    # This is a callback function that gets connected to the NatNet client and called once per mocap frame.
    def receiveNewFrame(self, frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        # print( "Received frame", frameNumber )
        pass 

    # This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
    def receiveRigidBodyFrame(self, id, position, rotation ):
        # print( "Received frame for rigid body", id )
        if self.record == True:
            # Record the positions into numpy array
            # print(id, position)
            position = np.round(position, 4)
            rotation = np.round(rotation, 4)
            
            if (id == 1004):
                self.stylus_data[self.index_counter,:] = position
                if np.all(self.stylus_previous_position != position):  # if its not the same update to the new position
                    self.stylus_previous_position = position # update the new position
                    self.status_optitrack_signals.signal_list.emit(["Stylus","Detected"])
                    self.stylus_lose_track_counter = 0
                else:  # if the new position is the same as the old one, there is a big chance that it has lost detection.
                    self.stylus_lose_track_counter += 1
                    print("STYLUS NOT SHOWING!")
                    if (self.stylus_lose_track_counter > 100):
                        self.status_optitrack_signals.signal_list.emit(["Stylus","Lost detection"])
            elif (id == 1005):
                self.specs_data[self.index_counter,:] = position
                self.index_counter += 1 # Increment the index counter everytime the final rigidbody is sent
                if np.all(self.specs_previous_position != position): 
                    self.specs_previous_position = position 
                    self.status_optitrack_signals.signal_list.emit(["Specs","Detected"])
                    self.specs_lose_track_counter = 0
                else:
                    self.specs_lose_track_counter += 1
                    print("specs NOT SHOWING!")
                    if (self.specs_lose_track_counter > 100):
                        self.status_optitrack_signals.signal_list.emit(["Specs","Lost detection"])

            print(self.index_counter)
            if self.index_counter > self.row:
                print("Handle overflow error!!") 
        else:
            pass

    @Slot()
    def spawn_thread(self, message):
        print("Spawn matlab thread called!!!")
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

