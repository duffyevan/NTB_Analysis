import datetime
import ftplib
import logging
import os
import posixpath
import sys
from threading import Thread
from typing import List

from PyQt5.QtCore import QDate, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QMessageBox, QWidget, QVBoxLayout

from Functions import dataCalc
from HostpointLib import HostpointClient
from folder import Folder
from frontend.mainwindow import Ui_MainWindow

config_file_path = './setup.conf'


class Main(QObject):
    window = None
    ui = None
    config = None
    checkBoxes: List[QCheckBox] = []
    showDialogSignal = pyqtSignal(str, str)
    downloadingSignal = pyqtSignal(bool)
    progressBarSignal = pyqtSignal(bool)

    ## Constructor
    # Loads configuration and initializes superclass
    def __init__(self):
        super(Main, self).__init__()
        self.ui = None
        self.log_path = './log.txt'
        loginInfo = open('login.csv').readlines()[1].strip().split(',')
        logging.basicConfig(filename=self.log_path, level=logging.INFO,
                            format='%(asctime)s: %(levelname)s : %(message)s')
        # TODO add a log file
        logging.info("Starting...")
        self.folder = Folder('setup.conf')

        try:
            self.HPClient = HostpointClient(loginInfo[0], loginInfo[1], loginInfo[2])
        except ftplib.all_errors as e:
            logging.error("An FTP Error Has Occurred While Logging Into HostPoint: %s" % (str(e)))
            print("An FTP Error Has Occurred While Logging Into HostPoint: %s" % (str(e)))
            exit(-1)

        logging.info('Logged into hostpoint')

    ## Opens the configuration in Notepad so the user can edit it.
    def open_conf_file(self):
        # Thread(target=os.system, args=("notepad " + config_file_path,)).start()
        os.system("notepad " + config_file_path)
        QMessageBox.about(self.window, "Notice", "Please Restart The Program For Changes To Take Effect")

    ## Opens the log file in Notepad so the user can view it.
    def open_log_file(self):
        Thread(target=os.system, args=("notepad " + self.log_path,)).start()
        # os.system("notepad " + config_file_path)
        # QMessageBox.about(self.window, "Notice", "Please Restart The Program For Changes To Take Effect")

    ## Opens windows explorer for the analysis folder so the user can view it.
    def open_analysis_folder(self):
        Thread(target=os.system, args=("explorer " + self.folder.analysisFolderLocation,)).start()
        # os.system("notepad " + config_file_path)
        # QMessageBox.about(self.window, "Notice", "Please Restart The Program For Changes To Take Effect")

    ## Threaded option for Analyze for day
    def threadAnalyzeForDay(self):
        Thread(target=self.analyzeFilesForDay).start()

    ## Threaded option for Analyze for month
    def threadAnalyzeForMonth(self):
        Thread(target=self.analyzeFilesForMonth).start()

    ## Threaded option for Analyze for year
    def threadAnalyzeForYear(self):
        Thread(target=self.analyzeFilesForYear).start()

    ## Threaded function tied to a signal for showing a dialog with the given informaiton
    # @param title The title of the dialog
    # @param message The message of the dialog
    def showDialog(self, title, message):
        QMessageBox.about(self.window, title, message)

    ## As the name states
    # @param plc The name of PLC in F00x Format
    # @param dt The datetime.date representing the date to get the files for
    def analyzeFilesForDayAndPLC(self, plc, dt):
        files = self.HPClient.download_files_for_plc_and_day(plc, dt,
                                                             download_location=self.folder.downloadFolderLocation)
        print(files)
        for local_file in files:
            try:
                spread_sheets = self.folder.getPLC_tables(plc)
                dataCalc(local_file,
                         spread_sheets[0],
                         spread_sheets[1],
                         posixpath.join(self.folder.outputFolderLocation, plc),
                         posixpath.splitext(posixpath.basename(local_file))[0] + '_analyzed_efficiency',
                         float(self.folder.configFile[plc]["specificHeatCapacity"]))
                os.remove(local_file)
            except KeyError as e:
                self.progressBarSignal.emit(False)

                self.showDialogSignal.emit("Error!",
                                           "A Key Error Occurred During The Processing For " + plc + ". " +
                                           str(e) + ". Make Sure The Configuration File Lists The Correct "
                                                    "Thermodynamic Table Names")
                logging.error("A Key Error Occurred During The Processing For " + plc + ". " + str(e) +
                              ". Make Sure The Configuration File Lists The Correct Thermodynamic Table Names")
                self.progressBarSignal.emit(True)

    ## Analyze all files for a given day
    def analyzeFilesForDay(self):
        selected_plcs = self.getSelectedPLCs()

        if len(selected_plcs) is 0:
            self.showDialogSignal.emit("Error!", "No PLC Selected")
            return

        self.downloadingSignal.emit(True)
        for plc in selected_plcs:
            try:
                qdate = self.ui.daySelector.date()
                dt = datetime.date(qdate.year(), qdate.month(), qdate.day())
                self.analyzeFilesForDayAndPLC(plc, dt)

            except ftplib.all_errors as e:
                self.progressBarSignal.emit(False)

                self.showDialogSignal.emit("Error!",
                                           "An FTP Error Occurred During The Download For " + plc + ". " + str(e))
                logging.error("An FTP Error Occurred During The Download For " + plc + ". " + str(e))

                self.progressBarSignal.emit(True)

        self.showDialogSignal.emit("Done!", "Analysis Process Is Complete")
        self.folder.deleteDownloadFolder()
        logging.info("Analysis Process Is Complete")
        self.downloadingSignal.emit(False)

    ## Analyze all files for a given month
    def analyzeFilesForMonth(self):
        selected_plcs = self.getSelectedPLCs()

        if len(selected_plcs) is 0:
            self.showDialogSignal.emit("Error!", "No PLC Selected")
            return

        self.downloadingSignal.emit(True)
        for plc in selected_plcs:
            try:
                qdate = self.ui.monthSelector.date()
                dt = datetime.date(qdate.year(), qdate.month(), 1)
                calc_month = dt.month
                while dt.month is calc_month:
                    print(dt)
                    self.analyzeFilesForDayAndPLC(plc, dt)
                    dt = dt + datetime.timedelta(1)

            except ftplib.all_errors as e:
                self.progressBarSignal.emit(False)

                self.showDialogSignal.emit("Error!",
                                           "An FTP Error Occurred During The Download For " + plc + ". " + str(e))
                logging.error("An FTP Error Occurred During The Download For " + plc + ". " + str(e))

                self.progressBarSignal.emit(True)

        self.showDialogSignal.emit("Done!", "Analysis Process Is Complete")
        self.folder.deleteDownloadFolder()
        logging.info("Analysis Process Is Complete")
        self.downloadingSignal.emit(False)

    ## Analyze all files for a given year
    def analyzeFilesForYear(self):
        selected_plcs = self.getSelectedPLCs()

        if len(selected_plcs) is 0:
            self.showDialogSignal.emit("Error!", "No PLC Selected")
            return

        self.downloadingSignal.emit(True)
        for plc in selected_plcs:
            try:
                qdate = self.ui.yearSelector.date()
                dt = datetime.date(qdate.year(), 1, 1)
                calc_year = dt.year
                print(calc_year, dt.year)
                while dt.year.__eq__(calc_year):
                    print(dt)
                    self.analyzeFilesForDayAndPLC(plc, dt)
                    dt = dt + datetime.timedelta(1)

            except ftplib.all_errors as e:
                self.progressBarSignal.emit(False)

                self.showDialogSignal.emit("Error!",
                                           "An FTP Error Occurred During The Download For " + plc + ". " + str(e))
                logging.error("An FTP Error Occurred During The Download For " + plc + ". " + str(e))

                self.progressBarSignal.emit(True)

        self.showDialogSignal.emit("Done!", "Analysis Process Is Complete")
        self.folder.deleteDownloadFolder()
        logging.info("Analysis Process Is Complete")
        self.downloadingSignal.emit(False)

    ## Iterate through the list of checkboxes and get a list of all those selected
    # @return An array of strings containing the addresses
    def getSelectedPLCs(self):
        selected_addresses: List[str] = []
        for checkBox in self.checkBoxes:
            if checkBox.isChecked():
                selected_addresses.append(checkBox.text())  # this is bad, but whatever
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

    ## Sets the enabled status of all the buttons that can create a thread. Used to prevent multiple async commands
    # @param enabled the boolean value whether its enabled or not
    def setAllButtonsEnabled(self, enabled):
        self.ui.pushButtonAnalyzeForDay.setEnabled(enabled)
        self.ui.pushButtonAnalyzeForMonth.setEnabled(enabled)
        self.ui.pushButtonAnalyzeForYear.setEnabled(enabled)
        self.ui.pushButtonDisselectAll.setEnabled(enabled)
        self.ui.pushButtonSelectAll.setEnabled(enabled)
        for checkbox in self.checkBoxes:
            checkbox.setEnabled(enabled)

    def prepareForDownload(self, starting):
        self.setProgressBarEnabled(starting)
        self.setAllButtonsEnabled(not starting)

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
        self.ui.actionOpen_Analysis_Folder.triggered.connect(self.open_analysis_folder)

        self.ui.actionQuit.triggered.connect(exit)

        self.checkBoxes.clear()

        self.ui.scrollArea.setWidgetResizable(True)

        scroll_content = QWidget(self.ui.scrollArea)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)

        try:
            for name in sorted(self.HPClient.get_plc_names()):
                ccb = QCheckBox(scroll_content)
                ccb.setObjectName(name.replace('.', '_') + "Checkbox")
                ccb.setText(name)
                scroll_layout.addWidget(ccb)
                self.checkBoxes.append(ccb)
        except ftplib.all_errors as e:
            logging.error("An FTP Error Has Occurred While Getting Metadata From HostPoint: %s" % (str(e)))
            print("An FTP Error Has Occurred While Getting Metadata From HostPoint: %s" % (str(e)))
            exit(-1)

        self.ui.scrollArea.setWidget(scroll_content)

        self.setProgressBarEnabled(False)

        self.showDialogSignal.connect(self.showDialog)
        self.progressBarSignal.connect(self.setProgressBarEnabled)
        self.downloadingSignal.connect(self.prepareForDownload)


if __name__ == '__main__':  # This main is required to start the UI
    main = Main()
    app = QApplication(sys.argv)
    main.window = QMainWindow()
    main.ui = Ui_MainWindow()
    main.ui.setupUi(main.window)
    main.setup_ui()
    main.window.show()
    logging.debug("Handing Process Over To UI Thread...")
    sys.exit(app.exec_())
