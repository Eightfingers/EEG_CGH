import sys
import numpy as np
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

# Create a basic window with a layout and a button
class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Form")
        self.layout = QVBoxLayout()
        self.button = QPushButton("Click me!")
        self.button.clicked.connect(self.start_thread) # start a thread when the button is clicked
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.coordinates = np.random.randint(0, 100, size=(1000, 3)) 

    # Instantiate and start a new thread
    def start_thread(self):
        instanced_thread = WorkerThread(self)
        instanced_thread.start()

    # Create the Slots that will receive signals from the worker Thread
    @Slot(str)
    def update_str_field(self, message):
        print(message)

    @Slot(int)
    def update_int_field(self, value):
        print(value)

    # slot for numpy n dimensional array
    @Slot(np.ndarray)
    def update_np_field(self, value):
        print(value)

    # slot for numpy n dimensional array
    @Slot(list)
    def update_list_field(self, value):
        print(value)


# Signals must inherit QObject
class MySignals(QObject):
    signal_str = Signal(str)
    signal_int = Signal(int)
    signal_np = Signal(np.ndarray) 
    signal_list = Signal(list)

# Create the Worker Thread
class WorkerThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        # Instantiate signals and connect signals to the Slots at the MainForm Widget
        self.signals = MySignals()
        self.signals.signal_str.connect(parent.update_str_field)
        self.signals.signal_int.connect(parent.update_int_field)
        self.signals.signal_np.connect(parent.update_np_field)
        self.signals.signal_list.connect(parent.update_list_field)

    def run(self):
        # Do something on the worker thread
        a = 1 + 1
        b = 3
        c = [a,b] # 
        coordinates = np.random.randint(0, 100, size=(3, 3)) 
        # Emit signals whenever you want
        self.signals.signal_int.emit(a) 
        self.signals.signal_np.emit(coordinates) # emit np
        self.signals.signal_str.emit("This text comes to Main thread from our Worker thread.")
        self.signals.signal_list.emit([a,b,c]) # emit list

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec())