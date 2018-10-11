# Heat Pump Analysis
This program processes sensor data gathered at the field unit heat pumps and predicts the thermodynamic cycle of it. It does by reading in data files retrieved from PLCs on a given day, parcing that data file into specific sensor readings, and then using some of those sensor readings, it find the thermodynamic properties of the cycle. The program then goes on to find the coefficient of performance for the system and the efficiency of the compressor. The program curretly does not accurately find the thermodynamic properties becase the high and low pressures of the systems are not measured. Furthermore, the temperatures of the refrigerant in the vapor compresson cycle are also not measured. To overcome these challanges, assumptions are made which include: temperature of the refrigerant entering the evaporator being 20 degree celius below the fluid entering the evaporator, refrigerant exiting the evaporator being at saturated vapor state, temprature of the refrigerant entering the condensor being 20 degrees above the fluid entering the condensor, and lastly, refrigrent exiting the condenser being at saturated liquid state. If the actual values of the heat pump cycle are measured, then this code can be tweeked to make the results more accurate. 
The program is run from a user interface (UI) window. There are three major options available to analyze files. First option allows for files, of the selected PLCs, to be analyzed for the selected day. The second option allows for files, of the selected PLCs, to be analyzed for the selected month. And the final option allows for files, of the selected PLCs, to be analyzed for the selected year. Each of these option also allows for the ability of selecting multiple PLCs at once. 
Once an option is selected and desired PLC(s) from the UI, the program will then iterate through each day for each PLC selected and retrieve available files from HostPoint's backup repository. It will then analyze each of the files retrieved, one at a time, and export the analyzed results, one at a time, into an excel file that will be placed inside the designated PLC's results folder.
Furthermore, the program also requires the refrigerant saturation table and the super heated vapor table to be available for each field unit that needs to be analyzed. Once the saturation tables are created and put into the saturation tables folder, they must be configured in the setup configuration file under the associated PLC's section. Same must be done for superheated tables after they are created and put into the superheated tables folder.
Specific heat capacity value of the fluid being heated for each heat pump must also be specified in the configuration file under the correct PLC section for the program to run correctly. 



# Installation
This section will walk you through the steps required to get the program up and running.
### Installing Python 3
If python is not already installed, please follow these instructions:

The program is written for python 3, specifically 3.5 and above. 
1. Go To [The Python Install Page](https://www.python.org/downloads/) and chose the most recent version of python3 
(currently 3.7)
2. Run the installer that is downloaded, and follow the steps for a default installation (if asked, make sure you add 
python to PATH and associate .py files with the python launcher, these should be done by default)
    1. If prompted, make sure you chose to install `pip` as well.
3. Open up CMD and make sure python is in the path by running python (or python3 if that doesn't work). If a prompt 
comes up, then python is installed correctly. Type `exit()` to close python.


### Installing Required Python Packages
1. In the command window, navigate to the `NTB-WPZ-Automation` folder that came out of the zip file and then navigate to
the `Setup` folder.
2. Run the command `python -m pip -r requirements.txt` to install the required packages.
    1. You may need to have admin privileges to run this command. If so, reopen CMD in administrator mode

?
?
?
?
### Configuring The Program
Before running the program, you must first configure the settings. In the User directory, create `login.csv`. 
Fill in the following section:
1. __HOSTPOINT__: The hostname, username and password must be set to those of the HostPoint FTP client so that the 
upload can be done automatically (Note: The GUI program will not automatically upload to HostPoint).

### Creating A Shortcut to The Main Program
You're almost there! All that needs to be done now is creating an easy way to launch the program. 
1. Navigate to the `NTB-WPZ-Automation` folder that came out of the zip file and then navigate to the `ProgramFiles` 
folder.
2. Right click the `main_frontend.py` file, and chose `Send To... -> Desktop (Create Shortcut)`.
3. Rename the shortcut on the desktop to something memorable
?
?
?
?

# Running The Program
To run the program, double click the shortcut created in the previous section or just run `main_frontend.py`. On the first 
run the folders hierchy will be created but the program will fail to complete because there are no thermodynamic tables avalabe for it to use and the configuration file is not configured yet. However, the tables can now be put into the correct folders and the configuration file can then be configred. To configure the configuration file, go to the `Configuration` tab in the menubar and select `Open Configuration File`. Once it opens in notepad, create the `PLC section` with PLC names and fill in the assotiated data underneath it. Once satisfied with the config file, save and close notepad. You will be prompted by the program to restart the program for the changed to take effect. Please do so.
On the next run, the program should run correctly if all is configured and setup correctly. You can now select a day, month or 
year, select a subset of PLCs and then press the analyze button. This will analyze all files from the PLCs selected for that given
time period. Furthermore, the analyzed results can be found inside the "Analysis" folder.