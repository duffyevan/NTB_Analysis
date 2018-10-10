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

    def foldersSetup(self):
        self.path_exist(self.analysisFolderLocation)
        self.path_exist(self.downloadFolderLocation)
        self.path_exist(self.outputFolderLocation)
        self.path_exist(self.saturationTableFolder)
        self.path_exist(self.superheatedTableFolder)

    def getPLC_tables(self, PLC_number):
        saturationTableName = self.configFile[PLC_number]['saturationTable']
        saturationTableFolder = self.saturationTableFolder
        saturationTablePath = posixpath.join(saturationTableFolder, saturationTableName)

        superheatedTableName = self.configFile[PLC_number]['superHeatedTable']
        superheatedTableFolder = self.superheatedTableFolder
        superheatedTablePath = posixpath.join(superheatedTableFolder, superheatedTableName)

        return (saturationTablePath, superheatedTablePath)

    def get_PLC_Name(self, file, numberOfFirstCharacters):
        nameOfFile = ntpath.basename(file)
        PLC_number = nameOfFile[:numberOfFirstCharacters]
        return PLC_number

    def deleteDownloadFolder(self):
        rmtree(self.downloadFolderLocation)

if __name__ == '__main__':
    # setup reading the config file
    f = Folder('setup.conf')
    # f.cleanFolder()
    # f.foldersSetup()
    # tablePaths = f.getPLC_tables('F001')
    # print(tablePaths[0])
    # print(tablePaths[1])
    # PLCnumber = f.get_PLC_Name("C:\\Users\\c-patel\\Desktop\\MQP\\me-program\\Files\\F001\\Files\\F001_20180829_000002"
    #                            ".xls", 4)
    # print(PLCnumber)

    # if(os.path.exists(tablePaths[0])):
    #     print("saturation file exists")

    # if(os.path.exists(tablePaths[1])):
    #     print("superheated file exists")
