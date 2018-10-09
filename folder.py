import os
import configparser
import ntpath


## Checks to see of the given path is valid on the local PC storage. If it is not, then it creates the path and folders.
# @param destination {string} Path to the directory on the local storage
def path_exist(destination):
    if not os.path.exists(destination):
        os.makedirs(destination)



def foldersSetup(configFile):
    analysisFolderLocation = configFile['setup']['analyzationFolderLocation'].replace("~", "c:\\Users\\" + os.getlogin())
    path_exist(analysisFolderLocation)

    downloadFolderLocation = analysisFolderLocation + "Files Download Folder\\"
    path_exist(downloadFolderLocation)

    outputFolderLocation =  analysisFolderLocation + "Analyzation Result's Folder\\"
    path_exist(outputFolderLocation)

    saturationTableFolder = analysisFolderLocation + "Saturation Tables\\"
    path_exist(saturationTableFolder)

    superheatedTableFolder = analysisFolderLocation + "Superheated Tables\\"
    path_exist(superheatedTableFolder)


def getPLC_tables(configFile, PLC_number):
    saturationTableName = configFile[PLC_number]['saturationTable']
    saturationTableFolder = configFile['setup']['analyzationFolderLocation'].replace("~", "c:\\Users\\" + os.getlogin()) + "Saturation Tables\\"
    saturationTablePath = os.path.join(saturationTableFolder, saturationTableName)
    
    superheatedTableName = configFile[PLC_number]['superHeatedTable']
    superheatedTableFolder = configFile['setup']['analyzationFolderLocation'].replace("~", "c:\\Users\\" + os.getlogin()) + "Superheated Tables\\"
    superheatedTablePath = os.path.join(superheatedTableFolder, superheatedTableName)

    return (saturationTablePath, superheatedTablePath) 
    

def get_PLC_Name(file, numberOfFirstCharacters): 
    nameOfFile = ntpath.basename(file)
    PLC_number = nameOfFile[:numberOfFirstCharacters]
    return PLC_number




#setup reading the config file
config = configparser.ConfigParser()
config.read('setup.conf')
foldersSetup(config)
tablePaths = getPLC_tables(config, 'F001')
print(tablePaths[0])
print(tablePaths[1])
PLCnumber = get_PLC_Name("C:\\Users\\c-patel\\Desktop\\MQP\\me-program\\Files\\F001\\Files\\F001_20180829_000002.xls", 4)
print(PLCnumber)

# if(os.path.exists(tablePaths[0])):
#     print("saturation file exists")

# if(os.path.exists(tablePaths[1])):
#     print("superheated file exists")