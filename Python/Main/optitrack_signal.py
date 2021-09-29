import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import matlab.engine

# Signals must inherit QObject
class OptitrackSignals(QObject):
    signal_bool = Signal(bool)
    signal_int = Signal(int)