# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1117, 889)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.traceStartButton = QPushButton(self.centralwidget)
        self.traceStartButton.setObjectName(u"traceStartButton")
        self.traceStartButton.setGeometry(QRect(40, 680, 141, 51))
        font = QFont()
        font.setPointSize(12)
        self.traceStartButton.setFont(font)
        self.traceStartButton.setIconSize(QSize(18, 18))
        self.traceStopButton = QPushButton(self.centralwidget)
        self.traceStopButton.setObjectName(u"traceStopButton")
        self.traceStopButton.setGeometry(QRect(40, 760, 141, 51))
        self.traceStopButton.setFont(font)
        self.traceStopButton.setIconSize(QSize(18, 18))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1117, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionSave)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save data", None))
        self.traceStartButton.setText(QCoreApplication.translate("MainWindow", u"Start Tracing", None))
        self.traceStopButton.setText(QCoreApplication.translate("MainWindow", u"Stop Tracing", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

