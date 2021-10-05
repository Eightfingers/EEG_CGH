import numpy as np
from PySide6.QtCore import QObject, Signal

# Signals must inherit QObject
class AppSignals(QObject):
    signal_bool = Signal(bool)
    signal_int = Signal(int)
    signal_list = Signal(list)
    signal_numpy = Signal(np.ndarray)
    signal_str = Signal(str)
    signal_dict = Signal(dict)
