import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import matlab.engine

# Signals must inherit QObject
class MatlabSignals(QObject):
    signal_str = Signal(str)
    signal_int = Signal(int)
    signal_np = Signal(np.ndarray)
    signal_list = Signal(list)
    signal_dict = Signal(dict)
