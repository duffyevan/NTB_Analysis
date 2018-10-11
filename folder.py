import os
import posixpath
from configparser import ConfigParser
import ntpath
from shutil import rmtree


class Folder:

    ## Checks to see of the given path is valid on the local PC storage. If it is not, then it creates the path and folders.
    # @param destination {string} Path to the directory on the local storage
    def path_exist(self, destination):
        if not os.path.exists(destination):
            os.makedirs(destination)

    ## Uses the configuration file to configure all the folder paths.
    # @param config_file_path {string} Path to the configuration file.
    def __init__(self, config_file_path):
        self.configFile = ConfigParser()
        self.configFile.read(config_file_path)
        self.analysisFolderLocation = posixpath.join(self.configFile['setup']['analyzationFolderLocation'],
                                                     'Analyzer')
        self.downloadFolderLocation = posixpath.join(self.analysisFolderLocation, "Files Download Folder")
        self.outputFolderLocation = posixpath.join(self.analysisFolderLocation, "Analysis Results Folder")
        self.saturationTableFolder = posixpath.join(self.analysisFolderLocation, "Saturation Tables")
        self.superheatedTableFolder = posixpath.join(self.analysisFolderLocation, "Superheated Tables")

        self.foldersSetup()

    ## Sets up the folders.
    def foldersSetup(self):
        self.path_exist(self.analysisFolderLocation)
        self.path_exist(self.downloadFolderLocation)
        self.path_exist(self.outputFolderLocation)
        self.path_exist(self.saturationTableFolder)
        self.path_exist(self.superheatedTableFolder)

    ## Reads in a PLC number and finds the corresponding attributes needed for analyzation.
    # @param PLC_number {string} PLC number.
    def getPLC_tables(self, PLC_number):
        saturationTableName = self.configFile[PLC_number]['saturationTable']
        saturationTableFolder = self.saturationTableFolder
        saturationTablePath = posixpath.join(saturationTableFolder, saturationTableName)

        superheatedTableName = self.configFile[PLC_number]['superHeatedTable']
        superheatedTableFolder = self.superheatedTableFolder
        superheatedTablePath = posixpath.join(superheatedTableFolder, superheatedTableName)

        return (saturationTablePath, superheatedTablePath)


    ## Finds the PLC number from the given data file name.
    # @param file {string} Path of the data file.
    # @param numberOfFirstCharacters {number} How many characters of a string need to be kept starting from the first character in the string.
    def get_PLC_Name(self, file, numberOfFirstCharacters):
        nameOfFile = ntpath.basename(file)
        PLC_number = nameOfFile[:numberOfFirstCharacters]
        return PLC_number


    ## Delete the temporary downloads folder.
    def deleteDownloadFolder(self):
        rmtree(self.downloadFolderLocation)




if __name__ == '__main__':
    f = Folder('setup.conf')
