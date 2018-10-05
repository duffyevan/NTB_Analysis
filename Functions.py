import os
from Analysis import HeatPumpAnalysis

def interpolation(x1, y1, x2, x3, y3):
    y2 = (((x2-x1)*(y3-y1))/(x3-x1))+y1
    return y2


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

    # print(arrayI1Values)

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

    # print(thermoPointsMin)
    # print(thermoPointsMax)


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

    # Result = (pI2,tI2,hI2,sI2)
    # print("the result is" + str(Result))
    return (pI2,tI2,hI2,sI2)


def effencisyCalc(state1_Enthalpy, state2_Enthalpy, state2_Prime_Enthalpy, state3_Enthalpy):
    COP_I = (state2_Enthalpy - state3_Enthalpy)/(state2_Enthalpy - state1_Enthalpy)
    COP_A = (state2_Prime_Enthalpy - state3_Enthalpy)/(state2_Prime_Enthalpy - state1_Enthalpy)
    n_Compressor = (state2_Enthalpy - state1_Enthalpy)/(state2_Prime_Enthalpy - state1_Enthalpy)
    return (COP_I, COP_A, n_Compressor)


def thermalEnergyCalc(flowrate, coldTemp, hotTemp, Cp):
    f = flowrate * 0.017
    c = coldTemp + 273.4
    h = hotTemp + 273.4
    
    return (f * Cp * (h - c))


def state2_Prime_Enthalpy_Calc(thermalEnergy, powerConsumption, state1_Enthalpy, state3_Enthalpy):
    h3 = float(((thermalEnergy * state1_Enthalpy) - (powerConsumption * state3_Enthalpy))/(thermalEnergy - powerConsumption))
    return h3


def dataCalc(dataSheet, saturatedTable, superHeatedTable, resultFileDestination, resultFileName):
    rawData = HeatPumpAnalysis(dataSheet)
    numberOfRows = len(rawData.get_col("Datum/Winterzeit"))

    saturated = HeatPumpAnalysis(saturatedTable)
    numberOfRows1 = len(saturated.get_col("Temperature"))

    superheat = HeatPumpAnalysis(superHeatedTable)
    numberOfRows2 = len(superheat.get_col("Temperature"))

    HeatCapacityOfWater = 4.1855
    arrayResults = []

    i=0
    while(i < numberOfRows):
        curretRow = rawData.get_row(i)
        
        if("d10010001" == curretRow["47_Dig"]):
            dateTime = curretRow["Datum/Winterzeit"]
            waterInletTemp = float(curretRow["03_Sein1"])/100
            condenserTemp = waterInletTemp + 20
            waterOutletTemp = float(curretRow["09_Aaus1"])/100
            waterFlowRate = float(curretRow["22_Vaufl"])/60
            airInletTemp = float(curretRow["07_Qein1"])/100
            evaporatorTemp = airInletTemp - 20
            compressorPower = float(curretRow["27_PelV"])/1000
            
            ThermalEnergy = thermalEnergyCalc(waterFlowRate, waterInletTemp, waterOutletTemp, HeatCapacityOfWater)
            if(ThermalEnergy > 0):
                state1_Result = singleInterpolation(evaporatorTemp, "Temperature", "Vapor", saturated, numberOfRows1)
                state2_Result = doubleInterpolation(condenserTemp, "Temperature", state1_Result[3], "Entropy Vapor", "Vapor", 50, superheat, numberOfRows2)
                state3_Result = singleInterpolation(state2_Result[0], "Pressure Liquid", "Liquid", saturated, numberOfRows1)
                state4_Result = (state1_Result[0], state1_Result[1], state3_Result[2], "Not Found")
                state2_Prime_Enthalpy = state2_Prime_Enthalpy_Calc(ThermalEnergy, compressorPower, state1_Result[2], state3_Result[2])
                if(state2_Prime_Enthalpy > state2_Result[2] and state2_Prime_Enthalpy <= 560):
                    state2_Prime_Result = doubleInterpolation(state3_Result[0], "Pressure Vapor", state2_Prime_Enthalpy, "Enthalpy Vapor", "Vapor", 200, superheat, numberOfRows2)
                    preformanceResult = effencisyCalc(state1_Result[2], state2_Result[2], state2_Prime_Result[2], state3_Result[2])
                    arrayResults.append((dateTime, preformanceResult, state1_Result, state2_Result, state2_Prime_Result, state3_Result, state4_Result, waterInletTemp, waterOutletTemp, waterFlowRate, airInletTemp, compressorPower, ThermalEnergy, condenserTemp, evaporatorTemp))
            i +=1

        else:
            i +=1

    printToExcel(arrayResults, resultFileDestination, resultFileName)


def printToExcel(arrayOfResults, destination, fileName):
    sizeOfArray = len(arrayOfResults)
    
    dir_path = os.path.join(destination, fileName)
    with open(dir_path, "w") as output:
        i = -1
        while(i < sizeOfArray):
            if(i == -1):
                print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("Date and Time", "Ideal COP", "Actual COP", "Compressor Efficiency", "State-1 Pressure", "State-1 Temperature", "State-1 Enthalpy", "State-1 Entropy", "State-2 Pressure", "State-2 Temperature", "State-2 Enthalpy", "State-2 Entropy", "State-2' Pressure", "State-2' Temperature", "State-2' Enthalpy", "State-2' Entropy", "State-3 Pressure", "State-3 Temperature", "State-3 Enthalpy", "State-3 Entropy", "State-4 Pressure", "State-4 Temperature", "State-4 Enthalpy", "Water Inlet Temperature", "Water Outlet Temperature","Water Flowrate", "Air Inlet Temperature", "Compressor Power Usage","Calculated Thermal Energy Put Into The Water", "Assumed Temperature Of The Refrigerant Entering Condenser", "Assumed Temperature Of The Refrigerant Entering Evaporator"), file = output)
                i += 1
            else:
                data = arrayOfResults[i]
                print ("%s\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t%6.2f" % (str(data[0]), data[1][0], data[1][1], data[1][2], data[2][0], data[2][1], data[2][2], data[2][3], data[3][0], data[3][1], data[3][2], data[3][3], data[4][0], data[4][1], data[4][2], data[4][3], data[5][0], data[5][1], data[5][2], data[5][3], data[6][0], data[6][1], data[6][2], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]), file = output)
                i += 1 
    output.close()



dataCalc("D:\\reposatory\\me-program\\Files\\F001\\Files\\F001_20180829_000002 - Copy.xls", "D:\\reposatory\\me-program\\Files\\F001\\Properties Tables\\R410a Saturation Table.txt", "D:\\reposatory\\me-program\\Files\\F001\\Properties Tables\\R410a Superheated Table.txt", "D:\\reposatory\\me-program\\Files\\F001\\Results", "output.xls")
