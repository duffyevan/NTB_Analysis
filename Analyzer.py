import os
import posixpath

from HeatPumpReadout import HeatPumpReadout
from HostpointLib import HostpointClient



## Checks to see if a given number is a number and not a string.
# @param n {} Number or a string.
# @return A boolean true if it is a number, else false.
def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`,
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True


## Interpolates with the given values to find the desired coordinate value.
# @param x1 {number} First x coordinate value.
# @param y1 {number} First y coordinate value of the corresponding first x value.
# @param x2 {number} X coordinate value of the desired result.
# @param x3 {number} Third x coordinate value.
# @param y3 {number} Third y coordinate value of the corresponding third x value.
# @return The unknown value at the desired coordinate.
def interpolation(x1, y1, x2, x3, y3):
    y2 = (((x2-x1)*(y3-y1))/(x3-x1))+y1
    return y2


## Does a single interpolation for all other thermodynamic properties for the desired thermodynamic property value.
# @param constantVal1 {number} Desired thermodynamic property value.
# @param constantVal1Title {string} Table title for the desired thermodynamic property.
# @param typeOf {string} Type of thermodynamic properties looked for, "Liquid" state properties or "Vapor" state properties.
# @param table {table} Thermodynamic properties table used, which could either be a saturation table or a superheated table.
# @param numberOfRows {number} number of rows in the given thermodynamic properties table.
# @return The other unknown thermodynamic properties for the desired thermodynamic property value.
def singleInterpolation(constantVal1, constantVal1Title, typeOf, table, numberOfRows):
    pressure = "Pressure " + typeOf
    enthalpy = "Enthalpy " + typeOf
    entropy = "Entropy " + typeOf

    i = 0
    while(i < numberOfRows):
        currentRow = table.get_row(i)

        if(i == 0):
            minValues = currentRow
            i += 1

        elif(float(currentRow[constantVal1Title]) == float(constantVal1)):

            if(constantVal1Title == pressure):
                pI1 = float(constantVal1)
            else:
                pI1 = float(currentRow[pressure])

            if(constantVal1Title == "Temperature"):
                tI1 = float(constantVal1)
            else:
                tI1 = float(currentRow["Temperature"])

            if(constantVal1Title == enthalpy):
                hI1 = float(constantVal1)
            else:
                hI1 = float(currentRow[enthalpy])

            if(constantVal1Title == entropy):
                sI1 = float(constantVal1)
            else:
                sI1 = float(currentRow[entropy])

            return (pI1,tI1,hI1,sI1)

        elif(float(currentRow[constantVal1Title]) < float(constantVal1)):
            minValues = currentRow
            i += 1

        elif(float(currentRow[constantVal1Title]) > float(constantVal1)):
            higherValuePoints = currentRow
            break

    if(constantVal1Title == pressure):
        pI1 = float(constantVal1)
    else:
        pI1 = interpolation(float(minValues[constantVal1Title]), float(minValues[pressure]), float(constantVal1), float(higherValuePoints[constantVal1Title]), float(higherValuePoints[pressure]))

    if(constantVal1Title == "Temperature"):
        tI1 = float(constantVal1)
    else:
        tI1 = interpolation(float(minValues[constantVal1Title]), float(minValues["Temperature"]), float(constantVal1), float(higherValuePoints[constantVal1Title]), float(higherValuePoints["Temperature"]))

    if(constantVal1Title == enthalpy):
        hI1 = float(constantVal1)
    else:
        hI1 = interpolation(float(minValues[constantVal1Title]), float(minValues[enthalpy]), float(constantVal1), float(higherValuePoints[constantVal1Title]), float(higherValuePoints[enthalpy]))

    if(constantVal1Title == entropy):
        sI1 = float(constantVal1)
    else:
        sI1 = interpolation(float(minValues[constantVal1Title]), float(minValues[entropy]), float(constantVal1), float(higherValuePoints[constantVal1Title]), float(higherValuePoints[entropy]))

    return (pI1,tI1,hI1,sI1)


## Does a double interpolation for all other thermodynamic properties using the two desired thermodynamic property values.
# @param constantVal1 {number} First desired thermodynamic property value.
# @param constantVal1Title {string} Table title for the first desired thermodynamic property.
# @param constantVal2 {number} Second desired thermodynamic property value.
# @param constantVal2Title {string} Table title for the second desired thermodynamic property.
# @param typeOf {string} Type of thermodynamic properties looked for, "Liquid" state properties or "Vapor" state properties.
# @param varianceRange {number} The range at which thermodynamic properties will be recorded away from the first desired thermodynamic property value, plus and minus.
# @param table {table} Thermodynamic properties table used, which could either be a saturation table or a superheated table.
# @param numberOfRows {number} number of rows in the given thermodynamic properties table.
# @return The other unknown thermodynamic properties for the desired two thermodynamic property values.
def doubleInterpolation(constantVal1, constantVal1Title, constantVal2, constantVal2Title, typeOf, varianceRange, table, numberOfRows):
    pressure = "Pressure " + typeOf
    enthalpy = "Enthalpy " + typeOf
    entropy = "Entropy " + typeOf


    arrayI1Values = []

    #Set the upper and lower search limit the first constant
    upperLimit = float(constantVal1 + varianceRange)
    lowerLimit = float(constantVal1 - varianceRange)

    #Initialize variables
    curretRow = table.get_row(0)
    nextRow = table.get_row(1)

    #Go through the table and get the all the interpolated property values within the upper/lower limits of the first consonant
    currentRowNum = 0
    while (currentRowNum < (numberOfRows - 2)):
        currentRowNum += 1

        if(float(curretRow[constantVal1Title]) == float(constantVal1) and float(curretRow[constantVal2Title]) == float(constantVal2)):
            pI1 = float(curretRow[pressure])
            tI1 = float(curretRow["Temperature"])
            hI1 = float(curretRow[enthalpy])
            sI1 = float(curretRow[entropy])
            return (pI1,tI1,hI1,sI1)

        #Check to see if there is a pressure change and if so, set the current and next rows to the next ones
        if(curretRow[pressure] != nextRow[pressure]):
            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)

        else:
            if(((float(curretRow[constantVal1Title])) <= upperLimit) and ((float(curretRow[constantVal1Title])) >= lowerLimit)):
                if(((float(curretRow[constantVal2Title])) <= float(constantVal2)) and ((float(nextRow[constantVal2Title])) >= float(constantVal2))):
                    pI1 = float(curretRow[pressure])

                    if(constantVal2Title == "Temperature"):
                        tI1 = float(constantVal2)
                    else:
                        tI1 = interpolation(float(curretRow[constantVal2Title]), float(curretRow["Temperature"]), float(constantVal2), float(nextRow[constantVal2Title]), float(nextRow["Temperature"]))

                    if(constantVal2Title == enthalpy):
                        hI1 = float(constantVal2)
                    else:
                        hI1 = interpolation(float(curretRow[constantVal2Title]), float(curretRow[enthalpy]), float(constantVal2), float(nextRow[constantVal2Title]), float(nextRow[enthalpy]))

                    if(constantVal2Title == entropy):
                        sI1 = float(constantVal2)
                    else:
                        sI1 = interpolation(float(curretRow[constantVal2Title]), float(curretRow[entropy]), float(constantVal2), float(nextRow[constantVal2Title]), float(nextRow[entropy]))

                    arrayI1Values.append((pI1,tI1,hI1,sI1))

            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)

    thermoPointsMin = None
    thermoPointsMax = None
    C1min = float(constantVal1)
    C1max = float(constantVal1)

    #Find the closest Minimum and Maximum value to Contant variable 2
    if(1 < len(arrayI1Values)):
        for i in range(0, len(arrayI1Values)):
            thermoPoints = arrayI1Values[i]

            if(constantVal1Title == pressure):
                C =  float(thermoPoints[0])

            if(constantVal1Title == "Temperature"):
                C =  float(thermoPoints[1])

            if(constantVal1Title == enthalpy):
                C =  float(thermoPoints[2])

            if(constantVal1Title == entropy):
                C =  float(thermoPoints[3])

            if(C <= float(constantVal1)):
                if(C1min == float(constantVal1)):
                    C1min = C
                    thermoPointsMin = thermoPoints

                elif(C1min <= C and C <= float(constantVal1)):
                    C1min = C
                    thermoPointsMin = thermoPoints


            elif(C >= float(constantVal1)):
                    if(C1max == float(constantVal1)):
                        C1max = C
                        thermoPointsMax = thermoPoints

                    elif(C1min >= C and C >= float(constantVal1)):
                        C1max = C
                        thermoPointsMax = thermoPoints

    if(constantVal2Title == pressure):
        pI2 = float(constantVal2)
    elif(constantVal1Title == pressure):
        pI2 = float(constantVal1)
    elif(constantVal1Title == "Temperature"):
        pI2 = interpolation(float(thermoPointsMin[1]), float(thermoPointsMin[0]), float(constantVal1), float(thermoPointsMax[1]), float(thermoPointsMax[0]))
    elif(constantVal1Title == enthalpy):
        pI2 = interpolation(float(thermoPointsMin[2]), float(thermoPointsMin[0]), float(constantVal1), float(thermoPointsMax[2]), float(thermoPointsMax[0]))
    else:
        pI2 = interpolation(float(thermoPointsMin[3]), float(thermoPointsMin[0]), float(constantVal1), float(thermoPointsMax[3]), float(thermoPointsMax[0]))

    if(constantVal2Title == "Temperature"):
        tI2 = float(constantVal2)
    elif(constantVal1Title == "Temperature"):
        tI2 = float(constantVal1)
    elif(constantVal1Title == pressure):
        tI2 = interpolation(float(thermoPointsMin[0]), float(thermoPointsMin[1]), float(constantVal1), float(thermoPointsMax[0]), float(thermoPointsMax[1]))
    elif(constantVal1Title == enthalpy):
        tI2 = interpolation(float(thermoPointsMin[2]), float(thermoPointsMin[1]), float(constantVal1), float(thermoPointsMax[2]), float(thermoPointsMax[1]))
    else:
        tI2 = interpolation(float(thermoPointsMin[3]), float(thermoPointsMin[1]), float(constantVal1), float(thermoPointsMax[3]), float(thermoPointsMax[1]))

    if(constantVal2Title == enthalpy):
        hI2 = float(constantVal2)
    elif(constantVal1Title == enthalpy):
        hI2 = float(constantVal1)
    elif(constantVal1Title == pressure):
        hI2 = interpolation(float(thermoPointsMin[0]), float(thermoPointsMin[2]), float(constantVal1), float(thermoPointsMax[0]), float(thermoPointsMax[2]))
    elif(constantVal1Title == "Temperature"):
        hI2 = interpolation(float(thermoPointsMin[1]), float(thermoPointsMin[2]), float(constantVal1), float(thermoPointsMax[1]), float(thermoPointsMax[2]))
    else:
        hI2 = interpolation(float(thermoPointsMin[3]), float(thermoPointsMin[2]), float(constantVal1), float(thermoPointsMax[3]), float(thermoPointsMax[2]))

    if(constantVal2Title == entropy):
        sI2 = float(constantVal2)
    elif(constantVal1Title == entropy):
        sI2 = float(constantVal1)
    elif(constantVal1Title == pressure):
        sI2 = interpolation(float(thermoPointsMin[0]), float(thermoPointsMin[3]), float(constantVal1), float(thermoPointsMax[0]), float(thermoPointsMax[3]))
    elif(constantVal1Title == "Temperature"):
        sI2 = interpolation(float(thermoPointsMin[1]), float(thermoPointsMin[3]), float(constantVal1), float(thermoPointsMax[1]), float(thermoPointsMax[3]))
    else:
        sI2 = interpolation(float(thermoPointsMin[2]), float(thermoPointsMin[3]), float(constantVal1), float(thermoPointsMax[2]), float(thermoPointsMax[3]))

    return (pI2,tI2,hI2,sI2)


## Calculates the coefficient of performances of the system and the efficiency of the compressor.
# @param state1_Enthalpy {number} Enthalpy value at state one.
# @param state2_Enthalpy {number} Enthalpy value at state two.
# @param state2_Prime_Enthalpy {number} Enthalpy value at state two prime.
# @param state3_Enthalpy {number} Enthalpy value at state three.
# @return The values of the calculated coefficient of performances and compressor efficiency.
def effencisyCalc(state1_Enthalpy, state2_Enthalpy, state2_Prime_Enthalpy, state3_Enthalpy):
    COP_I = (state2_Enthalpy - state3_Enthalpy)/(state2_Enthalpy - state1_Enthalpy)
    COP_A = (state2_Prime_Enthalpy - state3_Enthalpy)/(state2_Prime_Enthalpy - state1_Enthalpy)
    n_Compressor = (state2_Enthalpy - state1_Enthalpy)/(state2_Prime_Enthalpy - state1_Enthalpy)
    return (COP_I, COP_A, n_Compressor)


## Calculates the amount of thermal energy dissipated at the condenser.
# @param flowrate {number} Flow rate of the fluid that needs heating in l/min.
# @param coldTemp {number} Temperature of the fluid entering the condenser that needs heating in degree C.
# @param hotTemp {number} Temperature of the fluid exiting the condenser that needs heating in degree C.
# @param Cp {number} Specific heat capacity value of the fluid that needs heating in kJ per kg per degree kelvin.
# @return The amount of thermal energy dissipated at the condenser in kW.
def thermalEnergyCalc(flowrate, coldTemp, hotTemp, Cp):
    f = flowrate * 0.017
    c = coldTemp + 273.4
    h = hotTemp + 273.4

    return (f * Cp * (h - c))


## Calculate the enthalpy value at state two prime.
# @param thermalEnergy {number} The amount of thermal energy dissipated at the condenser in kW.
# @param powerConsumption {number} Electrical power consumed by the compressor in kW.
# @param state1_Enthalpy {number} Enthalpy value at state one.
# @param state3_Enthalpy {number} Enthalpy value at state three.
# @return Enthalpy value at state two prime.
def state2_Prime_Enthalpy_Calc(thermalEnergy, powerConsumption, state1_Enthalpy, state3_Enthalpy):
    h3 = float(((thermalEnergy * state1_Enthalpy) - (powerConsumption * state3_Enthalpy))/(thermalEnergy - powerConsumption))
    return h3


## Finds the thermodynamic properties for all the states, one through four, along with the performance of the system.
# @param dataSheet {table} Data table that needs to analyzed with sensor measurements.
# @param saturatedTable {table} Saturation table of the given refrigerant type.
# @param superHeatedTable {number} Superheated vapor table of the given refrigerant type.
# @param resultFileDestination {string} Path of where the produced excel file will be placed with all the thermodynamic data.
# @param resultFileName {string} Name of the produced excel file.
# @param HeatCapacityOfFluidBeingHeated {number} Specific heat capacity value of the fluid that needs heating in kJ per kg per degree kelvin.
def dataCalc(dataSheet, saturatedTable, superHeatedTable, resultFileDestination, resultFileName, HeatCapacityOfFluidBeingHeated):

    if not posixpath.exists(resultFileDestination):
        os.makedirs(resultFileDestination)

    rawData = HeatPumpReadout(dataSheet)
    numberOfRows = len(rawData.get_col("Datum/Winterzeit"))

    saturated = HeatPumpReadout(saturatedTable)
    numberOfRows1 = len(saturated.get_col("Temperature"))

    superheat = HeatPumpReadout(superHeatedTable)
    numberOfRows2 = len(superheat.get_col("Temperature"))

    arrayResults = []

    i=0
    while(i < numberOfRows):
        curretRow = rawData.get_row(i)
        dateTime = curretRow["Datum/Winterzeit"]

        if(curretRow["22_Vaufl"] > 0):
            typeOfFlow = curretRow["22_Vaufl"]
            tempOut = curretRow["09_Aaus1"]
            heatingType = "Water Heater Is Running"

        else:
            typeOfFlow = curretRow["21_Vsenke"]
            tempOut = curretRow["01_Saus1"]
            heatingType = "House Heating Is Running"

        if(is_number(curretRow["03_Sein1"]) and is_number(tempOut) and is_number(typeOfFlow) and is_number(curretRow["07_Qein1"]) and is_number(curretRow["27_PelV"])):
            if("d10010001" == curretRow["47_Dig"]):
                waterInletTemp = float(curretRow["03_Sein1"])/100
                condenserTemp = waterInletTemp + 20
                waterOutletTemp = float(tempOut)/100
                waterFlowRate = float(typeOfFlow)/60
                airInletTemp = float(curretRow["07_Qein1"])/100
                evaporatorTemp = airInletTemp - 20
                compressorPower = float(curretRow["27_PelV"])/1000

                ThermalEnergy = thermalEnergyCalc(waterFlowRate, waterInletTemp, waterOutletTemp, HeatCapacityOfFluidBeingHeated)
                if(ThermalEnergy > 0):
                    state1_Result = singleInterpolation(evaporatorTemp, "Temperature", "Vapor", saturated, numberOfRows1)
                    state2_Result = doubleInterpolation(condenserTemp, "Temperature", state1_Result[3], "Entropy Vapor", "Vapor", 50, superheat, numberOfRows2)
                    state3_Result = singleInterpolation(state2_Result[0], "Pressure Liquid", "Liquid", saturated, numberOfRows1)
                    state4_Result = (state1_Result[0], state1_Result[1], state3_Result[2], "Not Found")
                    state2_Prime_Enthalpy = state2_Prime_Enthalpy_Calc(ThermalEnergy, compressorPower, state1_Result[2], state3_Result[2])
                    if(state2_Prime_Enthalpy > state2_Result[2] and state2_Prime_Enthalpy <= 560):
                        state2_Prime_Result = doubleInterpolation(state3_Result[0], "Pressure Vapor", state2_Prime_Enthalpy, "Enthalpy Vapor", "Vapor", 200, superheat, numberOfRows2)
                        preformanceResult = effencisyCalc(state1_Result[2], state2_Result[2], state2_Prime_Result[2], state3_Result[2])
                        info = "No Errors"
                        arrayResults.append((dateTime, preformanceResult, state1_Result, state2_Result, state2_Prime_Result, state3_Result, state4_Result, waterInletTemp, waterOutletTemp, waterFlowRate, airInletTemp, compressorPower, ThermalEnergy, condenserTemp, evaporatorTemp, info, heatingType))
                        i +=1

                    else:
                        info = "Error: State-2' Enthalpy Is Either Less Then State-2 Enthalpy or It Is Too Large"
                        arrayResults.append((dateTime, tuple(("","","")), state1_Result, state2_Result, tuple(("","", state2_Prime_Enthalpy,"")), state3_Result, state4_Result, waterInletTemp, waterOutletTemp, waterFlowRate, airInletTemp, compressorPower, ThermalEnergy, condenserTemp, evaporatorTemp, info, heatingType))
                        i +=1

                else:
                    info = "Error: Thermal Energy Out Is Negative For Heat Pump"
                    arrayResults.append((dateTime, tuple(("","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), waterInletTemp, waterOutletTemp, waterFlowRate, airInletTemp, compressorPower, ThermalEnergy, condenserTemp, evaporatorTemp, info, heatingType))
                    i +=1

            else:
                info = "Compressor Is Off"
                arrayResults.append((dateTime, tuple(("","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), "", "", "", "", "", "", "", "", info, ""))
                i +=1
        else:
            info = "Sensor Values Not Valid"
            arrayResults.append((dateTime, tuple(("","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), tuple(("","","","")), "", "", "", "", "", "", "", "", info, ""))
            i +=1



    printToExcel(arrayResults, resultFileDestination, resultFileName)


## Produces the excel file at the given location and writes the given results to it.
# @param arrayOfResults {array[results]} Array with the results for each data point in the given data table.
# @param destination {string} Path of where the produced excel file will be placed with all the thermodynamic data.
# @param fileName {string} Name of the produced excel file.
def printToExcel(arrayOfResults, destination, fileName):
    fileName = fileName + ".xls"
    sizeOfArray = len(arrayOfResults)

    dir_path = os.path.join(destination, fileName)
    with open(dir_path, "w") as output:
        i = -1
        while(i < sizeOfArray):
            if(i == -1):
                print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("Date and Time", "Error Checking", "Heating Method", "Ideal COP", "Actual COP", "Compressor Efficiency", "State-1 Pressure", "State-1 Temperature", "State-1 Enthalpy", "State-1 Entropy", "State-2 Pressure", "State-2 Temperature", "State-2 Enthalpy", "State-2 Entropy", "State-2' Pressure", "State-2' Temperature", "State-2' Enthalpy", "State-2' Entropy", "State-3 Pressure", "State-3 Temperature", "State-3 Enthalpy", "State-3 Entropy", "State-4 Pressure", "State-4 Temperature", "State-4 Enthalpy", "Water Inlet Temperature", "Water Outlet Temperature","Water Flowrate", "Air Inlet Temperature", "Compressor Power Usage","Calculated Thermal Energy Put Into The Water", "Assumed Temperature Of The Refrigerant Entering Condenser", "Assumed Temperature Of The Refrigerant Entering Evaporator"), file = output)

            else:
                data = arrayOfResults[i]

                if(data[15] == "No Errors"):
                    print ("%s\t%s\t%s\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f" % (str(data[0]), str(data[15]), str(data[16]), data[1][0], data[1][1], data[1][2], data[2][0], data[2][1], data[2][2], data[2][3], data[3][0], data[3][1], data[3][2], data[3][3], data[4][0], data[4][1], data[4][2], data[4][3], data[5][0], data[5][1], data[5][2], data[5][3], data[6][0], data[6][1], data[6][2], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]), file = output)

                elif(data[15] == "Error: State-2' Enthalpy Is Either Less Then State-2 Enthalpy or It Is Too Large"):
                    print ("%s\t%s\t%s\t%s\t%s\t%s\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%s\t%s\t%6.2f\t%s\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f" % (str(data[0]), str(data[15]), str(data[16]), data[1][0], data[1][1], data[1][2], data[2][0], data[2][1], data[2][2], data[2][3], data[3][0], data[3][1], data[3][2], data[3][3], data[4][0], data[4][1], data[4][2], data[4][3], data[5][0], data[5][1], data[5][2], data[5][3], data[6][0], data[6][1], data[6][2], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]), file = output)

                elif(data[15] == "Error: Thermal Energy Out Is Negative For Heat Pump"):
                    print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f" % (str(data[0]), str(data[15]), str(data[16]), data[1][0], data[1][1], data[1][2], data[2][0], data[2][1], data[2][2], data[2][3], data[3][0], data[3][1], data[3][2], data[3][3], data[4][0], data[4][1], data[4][2], data[4][3], data[5][0], data[5][1], data[5][2], data[5][3], data[6][0], data[6][1], data[6][2], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]), file = output)

                elif(data[15] == "Compressor Is Off"):
                    print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (str(data[0]), str(data[15]), str(data[16]), data[1][0], data[1][1], data[1][2], data[2][0], data[2][1], data[2][2], data[2][3], data[3][0], data[3][1], data[3][2], data[3][3], data[4][0], data[4][1], data[4][2], data[4][3], data[5][0], data[5][1], data[5][2], data[5][3], data[6][0], data[6][1], data[6][2], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]), file = output)

                elif(data[15] == "Sensor Values Not Valid"):
                    print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (str(data[0]), str(data[15]), str(data[16]), data[1][0], data[1][1], data[1][2], data[2][0], data[2][1], data[2][2], data[2][3], data[3][0], data[3][1], data[3][2], data[3][3], data[4][0], data[4][1], data[4][2], data[4][3], data[5][0], data[5][1], data[5][2], data[5][3], data[6][0], data[6][1], data[6][2], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]), file = output)

            i += 1


    output.close()
