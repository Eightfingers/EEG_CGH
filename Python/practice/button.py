import sys
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Slot

import matlab.engine

# Greetings
# @Slot()
# def say_hello():
#     print("Button clicked, Hello!")

# # Create the Qt Application
# app = QApplication(sys.argv)
# # Create a button
# button = QPushButton("Click me")
# # Connect the button to the function
# button.clicked.connect(say_hello)
# # Show the button
# button.show()

print("Starting matlab engine")
eng = matlab.engine.start_matlab()
print("Finished matlab engine")

# # Run the main Qt loop
# app.exec()
