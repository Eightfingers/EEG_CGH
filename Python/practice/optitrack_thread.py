import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox
import matlab.engine
from debug_trace import trace_opitrack_status
from debug_trace import trace_opitrack_status_bodies

from . import Main.PythonClient4_0.NatNetClient import NatNetClient
# from PythonClient.NatNetClient import NatNetClient
from app_signals import AppSignals
import time

# Create the main Thread
class OptitrackMainThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        # This will create a new NatNet client

        self.streaming_client = NatNetClient()
        self.optionsDict = {}
        self.optionsDict["clientAddress"] = "127.0.0.1"
        self.optionsDict["serverAddress"] = "127.0.0.1"
        self.optionsDict["use_multicast"] = True

        self.optionsDict = self.my_parse_args(sys.argv, self.optionsDict)
        self.streaming_client.set_client_address(self.optionsDict["clientAddress"])
        self.streaming_client.set_server_address(self.optionsDict["serverAddress"])
        self.streaming_client.set_use_multicast(self.optionsDict["use_multicast"])

        self.signals_to_status = AppSignals()
        self.signals_to_main_stylus_pos = AppSignals()
        self.signals_to_main_specs_pos_rotation = AppSignals()
        self.signals_to_main_show_electrode_placements = AppSignals()

        self.signals_to_main_stylus_pos.signal_numpy.connect(parent.update_current_stylus_position) # rotation is not needed for now
        self.signals_to_main_specs_pos_rotation.signal_list.connect(parent.update_current_specs_position_rotation)
        self.signals_to_status.signal_list.connect(parent.left_dock_status_widget.change_label)
        self.signals_to_main_show_electrode_placements.signal_numpy.connect(parent.update_reflective_markers_positions)

        # Control variables 
        self.record = False
        self.show_all_markers = False
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
        # Configure the streaming client to call our rigid body handler on the emulator to send data out.
        self.streaming_client.new_frame_listener = self.receiveNewFrame
        self.streaming_client.rigid_body_listener = self.receiveRigidBodyFrame
        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.
        is_running = self.streaming_client.run()
        
        if not is_running:
            trace_opitrack_status("ERROR: Could not start streaming client.")
            self.signals_to_status.signal_list.emit(["Optitrack","Error"])
            try:
                sys.exit(1)
            except SystemExit:
                trace_opitrack_status("...")
            finally:
                trace_opitrack_status("exiting")
        time.sleep(1)
        if self.streaming_client.connected() is False:
            trace_opitrack_status("ERROR: Could not connect properly.  Check that Motive streaming is on.")
            self.signals_to_status.signal_list.emit(["Optitrack","Error"])
            try:
                sys.exit(2)
            except SystemExit:
                trace_opitrack_status("...")
            finally:
                trace_opitrack_status("exiting")
        else:
            self.signals_to_status.signal_list.emit(["Optitrack","Okay"])

    def my_parse_args(self, arg_list, args_dict):
        # set up base values
        arg_list_len=len(arg_list)
        if arg_list_len>1:
            args_dict["serverAddress"] = arg_list[1]
            if arg_list_len>2:
                args_dict["clientAddress"] = arg_list[2]
            if arg_list_len>3:
                if len(arg_list[3]):
                    args_dict["use_multicast"] = True
                    if arg_list[3][0].upper() == "U":
                        args_dict["use_multicast"] = False

        return args_dict

    # This is a callback function that gets connected to the NatNet client and called once per mocap frame.
    # This callback function is used to get marker positions that are not part of the rigidbody.
    def receiveNewFrame(self, data_dict ):
        order_list=[ "frameNumber", "markerSetCount", "unlabeledMarkersCount", "rigidBodyCount", "skeletonCount",
                "labeledMarkerCount", "marker_modelID_0_positions", "timecode", "timecodeSub", "timestamp", "isRecording", "trackedModelsChanged" ]
        if (self.show_all_markers == True):
            marker_modelID_0_positions = data_dict["marker_modelID_0_positions"]
            labeledMarkerPositions = np.round(marker_modelID_0_positions, 5)
            if labeledMarkerPositions.size > 0: # Only emit the data when its not empty
                self.signals_to_main_show_electrode_placements.signal_numpy.emit(labeledMarkerPositions) 
                trace_opitrack_status_bodies("Labeled Marker Positions are")
                trace_opitrack_status_bodies(labeledMarkerPositions)
        pass 

    # This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
    def receiveRigidBodyFrame(self, id, position, rotation ):
        position = np.array(position)
        rotation = np.array(rotation)

        # trace_opitrack_status( "Received frame for rigid body", id," ",position," ",rotation )
        if (id == 1004): # if the id is 1004, it is the stylus data
            self.stylus_position = position 
            self.signals_to_main_stylus_pos.signal_numpy.emit(position)
            if self.record == True: # Record the positions into numpy array
                self.stylus_data[self.index_counter,:] = position
                if np.all(self.stylus_previous_position != position):    # if its not the same as the old position update to the new position
                    self.stylus_previous_position = position 
                    self.signals_to_status.signal_list.emit(["Stylus","Detected"])
                    self.stylus_lose_track_counter = 0
                else:  # if the new position is the same as the old one, there is a big chance that it has lost detection.
                    self.stylus_lose_track_counter += 1
                    trace_opitrack_status("Optitrack: Stylus is not detected!")
                    if (self.stylus_lose_track_counter > 100):
                        self.signals_to_status.signal_list.emit(["Stylus","Lost detection"])
        elif (id == 1005): # specs data
            specs_pos_rotation = [position, rotation]
            self.signals_to_main_specs_pos_rotation.signal_list.emit(specs_pos_rotation)
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
                    trace_opitrack_status("Optitrack: Specs is not detected!!")
                    if (self.specs_lose_track_counter > 100):
                        self.signals_to_status.signal_list.emit(["Specs","Lost detection"])

        # trace_opitrack_status("Optitrack: index counter is at", self.index_counter)
        if self.index_counter > self.row:
            trace_opitrack_status("Optitrack: Overflow of data!") 
            
    @Slot()
    def spawn_thread(self, message):
        trace_opitrack_status("Optitrack: Spawn matlab thread called!!!")
        trace_opitrack_status(message)

    @Slot(bool)
    def set_recording(self, message):
        self.record = message
        if (message == False):
            self.clear_data()

    @Slot(bool)
    def set_show_all_markers(self, message):
        self.show_all_markers = message
        print("Optitrack: Showing all markers ", message)

    def clear_data(self):
        self.index_counter = 0
        self.stylus_data = np.zeros(shape=[self.row, self.columns])
        self.specs_data = np.zeros(shape=[self.row, self.columns])

