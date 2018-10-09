import os
import posixpath
from configparser import ConfigParser
import ntpath


class Folder:
    ## Checks to see of the given path is valid on the local PC storage. If it is not, then it creates the path and folders.
    # @param destination {string} Path to the directory on the local storage
    def path_exist(self, destination):
        if not os.path.exists(destination):
            os.makedirs(destination)

    def __init__(self, config_file_path):
        self.configFile = ConfigParser()
        self.configFile.read(config_file_path)

    def foldersSetup(self):
        analysisFolderLocation = self.configFile['setup']['analyzationFolderLocation'].replace("~", "c:\\Users\\" +
                                                                                           os.getlogin())
        self.path_exist(analysisFolderLocation)

        downloadFolderLocation = posixpath.join(analysisFolderLocation,"Files Download Folder")
        self.path_exist(downloadFolderLocation)

        outputFolderLocation =  posixpath.join(analysisFolderLocation,"Analyzation Result's Folder")
        self.path_exist(outputFolderLocation)

        saturationTableFolder = posixpath.join(analysisFolderLocation,"Saturation Tables")
        self.path_exist(saturationTableFolder)

        superheatedTableFolder = posixpath.join(analysisFolderLocation,"Superheated Tables")
        self.path_exist(superheatedTableFolder)


    def getPLC_tables(self, PLC_number):
        saturationTableName = self.configFile[PLC_number]['saturationTable']
        saturationTableFolder = posixpath.join(self.configFile['setup']['analyzationFolderLocation'].replace("~",
                                "c:\\Users\\" + os.getlogin()),"Saturation Tables")
        saturationTablePath = posixpath.join(saturationTableFolder, saturationTableName)

        superheatedTableName = self.configFile[PLC_number]['superHeatedTable']
        superheatedTableFolder = posixpath.join(self.configFile['setup']['analyzationFolderLocation']
                                           .replace("~","c:\\Users\\" + os.getlogin()),"Superheated Tables")
        superheatedTablePath = posixpath.join(superheatedTableFolder, superheatedTableName)

        return (saturationTablePath, superheatedTablePath)


    def get_PLC_Name(self, file, numberOfFirstCharacters):
        nameOfFile = ntpath.basename(file)
        PLC_number = nameOfFile[:numberOfFirstCharacters]
        return PLC_number



if __name__ == '__main__':

    #setup reading the config file
    f = Folder('setup.conf')
    f.foldersSetup()
    tablePaths = f.getPLC_tables('F001')
    print(tablePaths[0])
    print(tablePaths[1])
    PLCnumber = f.get_PLC_Name("C:\\Users\\c-patel\\Desktop\\MQP\\me-program\\Files\\F001\\Files\\F001_20180829_000002"
                              ".xls", 4)
    print(PLCnumber)

    # if(os.path.exists(tablePaths[0])):
    #     print("saturation file exists")

    # if(os.path.exists(tablePaths[1])):
    #     print("superheated file exists")