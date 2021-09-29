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

        # Instantiate signals and connect signals to the Slots at the StatusWidget (parent)
        self.matlab_signals = MatlabSignals()
        self.optitrack_signals = OptitrackSignals()
        
        # This will create a new NatNet client
        self.streamingClient = NatNetClient()

        # Control variables 
        self.record = False
        self.stylus_record = None
        self.specs_record = None

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
            print(id, position)
            if (id == 1004):
                self.stylus_data[self.index_counter,:] = position 
            elif (id == 1005):
                self.specs_data[self.index_counter,:] = position 
                self.index_counter += 1 # Increment the index counter everytime the final rigidbody is sent
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
        # print("bool signal recieved from menu widget with bool ", message)
        self.record = message
        print(self.record)