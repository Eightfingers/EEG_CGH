import sys

from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked2)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("This is a simple dialog")
        button = dlg.exec_()

        if button == QMessageBox.Ok:
            print("OK!")

    def button_clicked2(self, s):

        button = QMessageBox.question(self, "Question dialog", "The longer message")

        if button == QMessageBox.Yes:
            print("Yes!")
        else:
            print("No!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()