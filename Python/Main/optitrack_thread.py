import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import matlab.engine
from matlab_signal import MatlabSignals
from PythonClient.NatNetClient import NatNetClient

# Create the main Thread
class OptitrackMainThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        # Instantiate signals and connect signals to the Slots at the StatusWidget (parent)
        self.signals = MatlabSignals()

        # This will create a new NatNet client
        self.streamingClient = NatNetClient()

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
    def receiveNewFrame( frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        print( "Received frame", frameNumber )

    # This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
    def receiveRigidBodyFrame( id, position, rotation ):
        print( "Received frame for rigid body", id )

    @Slot()
    def spawn_thread(self, message):
        print("Spawn matlab thread called!!!")
        print(message)