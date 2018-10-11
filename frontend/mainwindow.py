# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(385, 326)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(385, 326))
        MainWindow.setMaximumSize(QtCore.QSize(385, 326))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.masterProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.masterProgressBar.setGeometry(QtCore.QRect(10, 250, 361, 23))
        self.masterProgressBar.setProperty("value", 0)
        self.masterProgressBar.setTextVisible(False)
        self.masterProgressBar.setFormat("")
        self.masterProgressBar.setObjectName("masterProgressBar")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 253, 140))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 251, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(6, 8, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.pushButtonAnalyzeForDay = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonAnalyzeForDay.setObjectName("pushButtonAnalyzeForDay")
        self.gridLayout_2.addWidget(self.pushButtonAnalyzeForDay, 4, 1, 1, 1)
        self.pushButtonAnalyzeForMonth = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonAnalyzeForMonth.setObjectName("pushButtonAnalyzeForMonth")
        self.gridLayout_2.addWidget(self.pushButtonAnalyzeForMonth, 5, 1, 1, 1)
        self.daySelector = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.daySelector.setObjectName("daySelector")
        self.gridLayout_2.addWidget(self.daySelector, 4, 0, 1, 1)
        self.pushButtonAnalyzeForYear = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonAnalyzeForYear.setObjectName("pushButtonAnalyzeForYear")
        self.gridLayout_2.addWidget(self.pushButtonAnalyzeForYear, 6, 1, 1, 1)
        self.yearSelector = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.yearSelector.setObjectName("yearSelector")
        self.gridLayout_2.addWidget(self.yearSelector, 6, 0, 1, 1)
        self.monthSelector = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.monthSelector.setObjectName("monthSelector")
        self.gridLayout_2.addWidget(self.monthSelector, 5, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButtonSelectAll = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonSelectAll.setObjectName("pushButtonSelectAll")
        self.verticalLayout_2.addWidget(self.pushButtonSelectAll)
        self.pushButtonDisselectAll = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonDisselectAll.setObjectName("pushButtonDisselectAll")
        self.verticalLayout_2.addWidget(self.pushButtonDisselectAll)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 385, 21))
        self.menubar.setObjectName("menubar")
        self.menuNTB_Datacollection_Automation = QtWidgets.QMenu(self.menubar)
        self.menuNTB_Datacollection_Automation.setObjectName("menuNTB_Datacollection_Automation")
        self.menuConfiguration = QtWidgets.QMenu(self.menubar)
        self.menuConfiguration.setObjectName("menuConfiguration")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openConfFileButton = QtWidgets.QAction(MainWindow)
        self.openConfFileButton.setObjectName("openConfFileButton")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSetup_Scheduled_Task = QtWidgets.QAction(MainWindow)
        self.actionSetup_Scheduled_Task.setObjectName("actionSetup_Scheduled_Task")
        self.actionReload_Configuration_File = QtWidgets.QAction(MainWindow)
        self.actionReload_Configuration_File.setObjectName("actionReload_Configuration_File")
        self.openLogFileButton = QtWidgets.QAction(MainWindow)
        self.openLogFileButton.setObjectName("openLogFileButton")
        self.actionOpen_Analysis_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Analysis_Folder.setObjectName("actionOpen_Analysis_Folder")
        self.menuNTB_Datacollection_Automation.addAction(self.actionQuit)
        self.menuConfiguration.addAction(self.openConfFileButton)
        self.menuTools.addAction(self.openLogFileButton)
        self.menubar.addAction(self.menuNTB_Datacollection_Automation.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NTB Data Collection Automation"))
        self.pushButtonAnalyzeForDay.setText(_translate("MainWindow", "Analyze For Day"))
        self.pushButtonAnalyzeForMonth.setText(_translate("MainWindow", "Analyze For Month"))
        self.pushButtonAnalyzeForYear.setText(_translate("MainWindow", "Analyze For Year"))
        self.yearSelector.setDisplayFormat(_translate("MainWindow", "yyyy"))
        self.monthSelector.setDisplayFormat(_translate("MainWindow", "M/yyyy"))
        self.pushButtonSelectAll.setText(_translate("MainWindow", "Select All"))
        self.pushButtonDisselectAll.setText(_translate("MainWindow", "Disselect All"))
        self.menuNTB_Datacollection_Automation.setTitle(_translate("MainWindow", "File"))
        self.menuConfiguration.setTitle(_translate("MainWindow", "Configuration"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.openConfFileButton.setText(_translate("MainWindow", "Open Configuration File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionSetup_Scheduled_Task.setText(_translate("MainWindow", "Setup Scheduled Task"))
        self.actionReload_Configuration_File.setText(_translate("MainWindow", "Reload Configuration File"))
        self.openLogFileButton.setText(_translate("MainWindow", "Open Log"))
        self.actionOpen_Analysis_Folder.setText(_translate("MainWindow", "Open Analysis Folder"))

