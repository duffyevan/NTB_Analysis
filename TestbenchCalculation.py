import os
import posixpath

from HeatPumpReadout import HeatPumpReadout
from HostpointLib import HostpointClient
from Analyzer import thermalEnergyCalc
from Analyzer import singleInterpolation
from Analyzer import doubleInterpolation
from Analyzer import state2_Prime_Enthalpy_Calc
from Analyzer import effencisyCalc


## Finds the thermodynamic properties for all the states, one through four, along with the performance of the system  with actual measurements and assumed values.
# @param dataSheet {table} Data table that needs to analyzed with sensor measurements.
# @param saturatedTable {table} Saturation table of the given refrigerant type.
# @param superHeatedTable {number} Superheated vapor table of the given refrigerant type.
# @param resultFileDestination {string} Path of where the produced excel file will be placed with all the thermodynamic data.
# @param resultFileName {string} Name of the produced excel file.
# @param HeatCapacityOfFluidBeingHeated {number} Specific heat capacity value of the fluid that needs heating in kJ per kg per degree kelvin.
def dataCalc_TestBench(dataSheet, saturationTable, superHeatedTable, resultFileDestination, resultFileName):
    rawData = HeatPumpReadout(dataSheet)
    numberOfRows = len(rawData.get_col("Zeit"))

    saturated = HeatPumpReadout(saturationTable)
    numberOfRows1 = len(saturated.get_col("Temperature"))

    superheat = HeatPumpReadout(superHeatedTable)
    numberOfRows2 = len(superheat.get_col("Temperature"))

    HeatCapacityOfWater = 4.1855
    arrayResults1 = []
    arrayResults2 = []

    i=0
    while(i < numberOfRows):
        curretRow = rawData.get_row(i)

        dateTime = curretRow["Zeit"]
        waterInletTemp = float(curretRow["T_Wasser_Vorlauf"])
        waterOutletTemp = float(curretRow["T_Wasser_Ruecklauf"])
        waterFlowRate = float(curretRow["V_dot_Wasser"])
        airInletTemp = float(curretRow["T_luft_ein"])
        compressorPower = float(curretRow["P_elek_Verdichter"])/1000

        condenserTemp = waterInletTemp + 20
        evaporatorTemp = airInletTemp - 20

        tempAtState1 = float(curretRow["T_ueberhitzt"])
        pressureAtState1 = float(curretRow["p_Verdampfung"]) * 100
        pressureAtState2 = float(curretRow["p_Kondenation"]) * 100
        
        ThermalEnergy = thermalEnergyCalc(waterFlowRate, waterInletTemp, waterOutletTemp, HeatCapacityOfWater)

        if(ThermalEnergy > 0 and pressureAtState1 < pressureAtState2 and pressureAtState1 < 850):
            state1_Result1 = singleInterpolation(evaporatorTemp, "Temperature", "Vapor", saturated, numberOfRows1)
            state1_Result2 = doubleInterpolation(pressureAtState1, "Pressure Vapor", tempAtState1, "Temperature", "Vapor", 100, superheat, numberOfRows2)

            state2_Result1 = doubleInterpolation(condenserTemp, "Temperature", state1_Result1[3], "Entropy Vapor", "Vapor", 50, superheat, numberOfRows2)
            state2_Result2 = doubleInterpolation(pressureAtState2, "Pressure Vapor", state1_Result2[3], "Entropy Vapor", "Vapor", 200, superheat, numberOfRows2)

            state3_Result1 = singleInterpolation(state2_Result1[0], "Pressure Liquid", "Liquid", saturated, numberOfRows1)
            state3_Result2 = singleInterpolation(pressureAtState2, "Pressure Liquid", "Liquid", saturated, numberOfRows1)

            state4_Result1 = (state1_Result1[0], state1_Result1[1], state3_Result1[2], "Not Found")
            state4_Result2 = (state1_Result2[0], state1_Result2[1], state3_Result2[2], "Not Found")

            state2_Prime_Enthalpy1 = state2_Prime_Enthalpy_Calc(ThermalEnergy, compressorPower, state1_Result1[2], state3_Result1[2])
            state2_Prime_Enthalpy2 = state2_Prime_Enthalpy_Calc(ThermalEnergy, compressorPower, state1_Result2[2], state3_Result2[2])

            if(state2_Prime_Enthalpy1 > state2_Result1[2] and state2_Prime_Enthalpy1 <= 560 and state2_Prime_Enthalpy2 > state2_Result2[2] and state2_Prime_Enthalpy2 <= 560):

                state2_Prime_Result1 = doubleInterpolation(state3_Result1[0], "Pressure Vapor", state2_Prime_Enthalpy1, "Enthalpy Vapor", "Vapor", 200, superheat, numberOfRows2)
                state2_Prime_Result2 = doubleInterpolation(pressureAtState2, "Pressure Vapor", state2_Prime_Enthalpy2, "Enthalpy Vapor", "Vapor", 200, superheat, numberOfRows2)

                preformanceResult1 = effencisyCalc(state1_Result1[2], state2_Result1[2], state2_Prime_Result1[2], state3_Result1[2])
                preformanceResult2 = effencisyCalc(state1_Result2[2], state2_Result2[2], state2_Prime_Result2[2], state3_Result2[2])

                arrayResults1.append((dateTime, preformanceResult1, state1_Result1, state2_Result1, state2_Prime_Result1, state3_Result1, state4_Result1, waterInletTemp, waterOutletTemp, waterFlowRate, airInletTemp, compressorPower, ThermalEnergy, condenserTemp, evaporatorTemp))
                arrayResults2.append((dateTime, preformanceResult2, state1_Result2, state2_Result2, state2_Prime_Result2, state3_Result2, state4_Result2, waterInletTemp, waterOutletTemp, waterFlowRate, airInletTemp, compressorPower, ThermalEnergy, tempAtState1, pressureAtState2))
        i +=1

    printToExcel_TestBench(arrayResults1, arrayResults2, resultFileDestination, resultFileName)


## Produces the excel file at the given location and writes the given results to it.
# @param arrayOfResults {array[results]} Array with the results for each data point in the given data table.
# @param destination {string} Path of where the produced excel file will be placed with all the thermodynamic data.
# @param fileName {string} Name of the produced excel file.
def printToExcel_TestBench(arrayOfResults1, arrayOfResults2, destination, fileName):
    fileName = fileName + ".xls"

    sizeOfArray = len(arrayOfResults1)
    sizeOfArray2 = len(arrayOfResults2)

    if(sizeOfArray == sizeOfArray2):
        dir_path = posixpath.join(destination, fileName)
        with open(dir_path, "w") as output:
            i = -1
            while(i < sizeOfArray and i < sizeOfArray2):
                if(i == -1):
                    print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("Date and Time", "Ideal COP (Assumed)", "Ideal COP (Measured)", "Actual COP (Assumed)", "Actual COP (Measured)", "Compressor Efficiency (Assumed)", "Compressor Efficiency (Measured)", "State-1 Pressure (Assumed)", "State-1 Pressure (Measured)", "State-1 Temperature (Assumed)", "State-1 Temperature (Measured)", "State-1 Enthalpy (Assumed)", "State-1 Enthalpy (Measured)", "State-1 Entropy (Assumed)", "State-1 Entropy (Measured)", "State-2 Pressure (Assumed)", "State-2 Pressure (Measured)", "State-2 Temperature (Assumed)", "State-2 Temperature (Measured)", "State-2 Enthalpy (Assumed)", "State-2 Enthalpy (Measured)", "State-2 Entropy (Assumed)", "State-2 Entropy (Measured)", "State-2' Pressure (Assumed)", "State-2' Pressure (Measured)", "State-2' Temperature (Assumed)", "State-2' Temperature (Measured)", "State-2' Enthalpy (Assumed)", "State-2' Enthalpy (Measured)", "State-2' Entropy (Assumed)", "State-2' Entropy (Measured)", "State-3 Pressure (Assumed)", "State-3 Pressure (Measured)", "State-3 Temperature (Assumed)", "State-3 Temperature (Measured)", "State-3 Enthalpy (Assumed)", "State-3 Enthalpy (Measured)", "State-3 Entropy (Assumed)", "State-3 Entropy (Measured)", "State-4 Pressure (Assumed)", "State-4 Pressure (Measured)", "State-4 Temperature (Assumed)", "State-4 Temperature (Measured)", "State-4 Enthalpy (Assumed)", "State-4 Enthalpy (Measured)", "Water Inlet Temperature", "Water Outlet Temperature","Water Flowrate", "Air Inlet Temperature", "Compressor Power Usage","Calculated Thermal Energy Put Into The Water", "Assumed Temperature Of The Refrigerant Entering Condenser", "Measured State 2 Pressure", "Assumed Temperature Of The Refrigerant Entering Evaporator", "Measured State 1 Temperature"), file = output)
                    i += 1
                else:
                    data1 = arrayOfResults1[i]
                    data2 = arrayOfResults2[i]

                    print ("%s\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f" % (str(data1[0]), data1[1][0], data2[1][0], data1[1][1], data2[1][1], data1[1][2], data2[1][2], data1[2][0], data2[2][0], data1[2][1], data2[2][1], data1[2][2], data2[2][2], data1[2][3], data2[2][3], data1[3][0], data2[3][0], data1[3][1], data2[3][1], data1[3][2], data2[3][2], data1[3][3], data2[3][3], data1[4][0], data2[4][0], data1[4][1], data2[4][1], data1[4][2], data2[4][2], data1[4][3], data2[4][3], data1[5][0], data2[5][0], data1[5][1], data2[5][1], data1[5][2], data2[5][2], data1[5][3], data2[5][3], data1[6][0], data2[6][0], data1[6][1], data2[6][1], data1[6][2], data2[6][2], data1[7], data1[8], data1[9], data1[10], data1[11], data1[12], data1[13], data2[13], data1[14], data2[14]), file = output)
                i += 1 
        output.close()

dataCalc_TestBench("D:\\reposatory\\me-program\\Files\\Test_Bench\\Files\\Test Bench Data Collection 1.xls", "D:\\reposatory\\me-program\\Files\\Test_Bench\\Properties Tables\\R407c Saturation Table.txt", "D:\\reposatory\\me-program\\Files\\Test_Bench\\Properties Tables\\R407c Superheated Table.txt", "D:\\reposatory\\me-program\\Files\\Test_Bench\\Results", "output1.xls")