import datetime
import logging
import os
import sys
from threading import Thread
from typing import List

from PyQt5.QtCore import QDate, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QMessageBox, QWidget, QVBoxLayout

from HostpointLib import HostpointClient
from frontend.mainwindow import Ui_MainWindow

config_file_path = 'insert conf here'.replace('~', 'c:\\Users\\' + os.getlogin())


class Main(QObject):
    window = None
    ui = None
    config = None
    checkBoxes: List[QCheckBox] = []
    showDialogSignal = pyqtSignal(str, str)

    ## Constructor
    # Loads configuration and initializes superclass
    def __init__(self):
        super(Main, self).__init__()
        self.ui = None
        self.log_path = './log.txt'
        loginInfo = open('login.csv').readlines()[1].strip().split(',')
        logging.basicConfig(filename=self.log_path, level=logging.INFO, format='%(asctime)s: %(levelname)s : %(message)s')
        #TODO add a log file
        logging.info("Starting...")
        self.HPClient = HostpointClient(loginInfo[0],loginInfo[1],loginInfo[2])
        logging.info('Logged into hostpoint')

    ## Opens the configuration in Notepad so the user can edit it.
    def open_conf_file(self):
        # Thread(target=os.system, args=("notepad " + config_file_path,)).start()
        os.system("notepad " + config_file_path)
        QMessageBox.about(self.window, "Notice", "Please Restart The Program For Changes To Take Effect")

    def open_log_file(self):
        Thread(target=os.system, args=("notepad " + self.log_path,)).start()
        # os.system("notepad " + config_file_path)
        # QMessageBox.about(self.window, "Notice", "Please Restart The Program For Changes To Take Effect")

    ## Threaded option for download for day
    def threadAnalyzeForDay(self):
        Thread(target=self.downloadFilesForDay).start()

    ## Threaded option for download for month
    def threadAnalyzeForMonth(self):
        Thread(target=self.downloadFilesForMonth).start()

    ## Threaded option for download for year
    def threadAnalyzeForYear(self):
        Thread(target=self.downloadFilesForYear).start()

    ## Threaded function tied to a signal for showing a dialog with the given informaiton
    # @param title The title of the dialog
    # @param message The message of the dialog
    def showDialog(self, title, message):
        QMessageBox.about(self.window, title, message)

    ## Download all files for a given day
    def downloadFilesForDay(self):
        pass


    ## Download all files for a given month
    def downloadFilesForMonth(self):
        pass

    ## Download all files for a given year
    def downloadFilesForYear(self):
        pass

    ## Iterate through the list of checkboxes and get a list of all those selected
    # @return An array of strings containing the addresses
    def getSelectedPLCs(self):
        selected_addresses: List[str] = []
        for checkBox in self.checkBoxes:
            if checkBox.isChecked():
                selected_addresses.append(checkBox.text())  # TODO FIXME this is bad
        return selected_addresses

    ## Set all checkboxes' checked values to a given value
    # @param selected Boolean to set the checked values to
    def setCheckedAllPLCs(self, selected: bool):
        for checkBox in self.checkBoxes:
            checkBox.setChecked(selected)

    ## Check all the host check boxes
    def selectAllPLCs(self):
        self.setCheckedAllPLCs(True)

    ## Uncheck all the host check boxes
    def disselectAllPLCs(self):
        self.setCheckedAllPLCs(False)

    ## Set the enabled status of the master progress bar. Enabled makes it pulsing and green. Disabled makes it greyed out
    # @param enabled the boolean value whether its enabled or not
    def setProgressBarEnabled(self, enabled: bool):
        if enabled:
            self.ui.masterProgressBar.setRange(0, 0)
            self.ui.masterProgressBar.setEnabled(True)
        else:
            self.ui.masterProgressBar.setRange(0, 10)
            self.ui.masterProgressBar.setDisabled(True)

    ## Sets the enabled status of all the buttons that can create a thread. Used to prevent multiple async downloads
    # @param enabled the boolean value whether its enabled or not
    def setAllButtonsEnabled(self, enabled):
        self.ui.pushButtonAnalyzeForDay.setEnabled(enabled)
        self.ui.pushButtonDownloadForMonth.setEnabled(enabled)
        self.ui.pushButtonDownloadForYear.setEnabled(enabled)
        self.ui.pushButtonDisselectAll.setEnabled(enabled)
        self.ui.pushButtonSelectAll.setEnabled(enabled)
        for checkbox in self.checkBoxes:
            checkbox.setEnabled(enabled)

    ## Set up the UI elements and do any needed config setup before starting the UI
    def setup_ui(self):
        logging.debug("Setting Up UI")
        self.ui.pushButtonAnalyzeForDay.clicked.connect(self.threadAnalyzeForDay)
        self.ui.pushButtonAnalyzeForMonth.clicked.connect(self.threadAnalyzeForMonth)
        self.ui.pushButtonAnalyzeForYear.clicked.connect(self.threadAnalyzeForYear)

        self.ui.pushButtonSelectAll.clicked.connect(self.selectAllPLCs)
        self.ui.pushButtonDisselectAll.clicked.connect(self.disselectAllPLCs)

        self.ui.daySelector.setDate(QDate(datetime.datetime.today()))
        self.ui.monthSelector.setDate(QDate(datetime.datetime.today()))
        self.ui.yearSelector.setDate(QDate(datetime.datetime.today()))

        self.ui.openConfFileButton.triggered.connect(self.open_conf_file)
        self.ui.openLogFileButton.triggered.connect(self.open_log_file)

        self.checkBoxes.clear()

        self.ui.scrollArea.setWidgetResizable(True)

        scroll_content = QWidget(self.ui.scrollArea)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)

        for name in self.HPClient.get_plc_names():
            ccb = QCheckBox(scroll_content)
            ccb.setObjectName(name.replace('.', '_') + "Checkbox")
            ccb.setText(name)
            scroll_layout.addWidget(ccb)
            self.checkBoxes.append(ccb)

        self.ui.scrollArea.setWidget(scroll_content)

        self.setProgressBarEnabled(False)

        self.showDialogSignal.connect(self.showDialog)


if __name__ == '__main__':
# def run():
    main = Main()
    app = QApplication(sys.argv)
    main.window = QMainWindow()
    main.ui = Ui_MainWindow()
    main.ui.setupUi(main.window)
    main.setup_ui()
    main.window.show()
    logging.debug("Handing Process Over To UI Thread...")
    sys.exit(app.exec_())
