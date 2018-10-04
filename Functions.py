from Analysis import HeatPumpAnalysis

def interpolation(x1, y1, x2, x3, y3):
    y2 = (((x2-x1)*(y3-y1))/(x3-x1))+y1
    return y2

def doubleInterpolation(constantVal1, constantVal1Title, constantVal2, constantVal2Title, varianceRange, table, numberOfRows):
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

        if(curretRow[constantVal1Title] == constantVal1 and curretRow[constantVal2Title] == constantVal2):
            pI1 = float(curretRow["Superheated Pressure"])
            tI1 = float(curretRow["Temperature"])
            hI1 = float(curretRow["Enthalpy"])
            sI1 = float(curretRow["Entropy"])
            #return (pI1,tI1,hI1,sI1)

        #Check to see if there is a pressure change and if so, set the current and next rows to the next ones
        if(curretRow["Superheated Pressure"] != nextRow["Superheated Pressure"]):
            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)

        else:
            if(((float(curretRow[constantVal1Title])) <= upperLimit) and ((float(curretRow[constantVal1Title])) >= lowerLimit)):
                if(((float(curretRow[constantVal2Title])) <= constantVal2) and ((float(nextRow[constantVal2Title])) >= constantVal2)):
                    pI1 = float(curretRow["Superheated Pressure"])

                    if(constantVal2Title == "Temperature"):
                        tI1 = float(constantVal2)
                    else:
                        tI1 = interpolation(float(curretRow[constantVal2Title]), float(curretRow["Temperature"]), float(constantVal2), float(nextRow[constantVal2Title]), float(nextRow["Temperature"]))

                    if(constantVal2Title == "Enthalpy"):
                        hI1 = float(constantVal2)
                    else:
                        hI1 = interpolation(float(curretRow[constantVal2Title]), float(curretRow["Enthalpy"]), float(constantVal2), float(nextRow[constantVal2Title]), float(nextRow["Enthalpy"]))

                    if(constantVal2Title == "Entropy"):
                        sI1 = float(constantVal2)
                    else:
                        sI1 = interpolation(float(curretRow[constantVal2Title]), float(curretRow["Entropy"]), float(constantVal2), float(nextRow[constantVal2Title]), float(nextRow["Entropy"]))
                    
                    arrayI1Values.append((pI1,tI1,hI1,sI1))

            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)
            
    print(arrayI1Values)

    thermoPointsMin = None
    thermoPointsMax = None
    C1min = constantVal1
    C1max = constantVal1

    if(1 < len(arrayI1Values)):
        for i in range(0, len(arrayI1Values)):
            thermoPoints = arrayI1Values[i]
            C =  thermoPoints[1]

            if(C <= constantVal1):
                if(C1min == constantVal1):
                    C1min = C
                    thermoPointsMin = thermoPoints

                elif(C1min <= C and C <= constantVal1):
                    C1min = C
                    thermoPointsMin = thermoPoints

            
            elif(C >= constantVal1):
                    if(C1max == constantVal1):
                        C1max = C
                        thermoPointsMax = thermoPoints

                    elif(C1min >= C and C >= constantVal1):
                        C1max = C
                        thermoPointsMax = thermoPoints

    print(thermoPointsMin)
    print(thermoPointsMax)
    
    if(constantVal2Title == "Superheated Pressure"):
        pI2 = float(constantVal2)
    elif(constantVal1Title == "Superheated Pressure"):
        pI2 = float(constantVal1)
    elif(constantVal1Title == "Temperature"):
        pI2 = interpolation(float(thermoPointsMin[1]), float(thermoPointsMin[0]), float(constantVal1), float(thermoPointsMax[1]), float(thermoPointsMax[0]))
    elif(constantVal1Title == "Enthalpy"):
        pI2 = interpolation(float(thermoPointsMin[2]), float(thermoPointsMin[0]), float(constantVal1), float(thermoPointsMax[2]), float(thermoPointsMax[0]))
    else:
        pI2 = interpolation(float(thermoPointsMin[3]), float(thermoPointsMin[0]), float(constantVal1), float(thermoPointsMax[3]), float(thermoPointsMax[0]))

    if(constantVal2Title == "Temperature"):
        tI2 = float(constantVal2)
    elif(constantVal1Title == "Temperature"):
        tI2 = float(constantVal1)
    elif(constantVal1Title == "Superheated Pressure"):
        tI2 = interpolation(float(thermoPointsMin[0]), float(thermoPointsMin[1]), float(constantVal1), float(thermoPointsMax[0]), float(thermoPointsMax[1]))
    elif(constantVal1Title == "Enthalpy"):
        tI2 = interpolation(float(thermoPointsMin[2]), float(thermoPointsMin[1]), float(constantVal1), float(thermoPointsMax[2]), float(thermoPointsMax[1]))
    else:
        tI2 = interpolation(float(thermoPointsMin[3]), float(thermoPointsMin[1]), float(constantVal1), float(thermoPointsMax[3]), float(thermoPointsMax[1]))

    if(constantVal2Title == "Enthalpy"):
        hI2 = float(constantVal2)
    elif(constantVal1Title == "Enthalpy"):
        hI2 = float(constantVal1)
    elif(constantVal1Title == "Superheated Pressure"):
        hI2 = interpolation(float(thermoPointsMin[0]), float(thermoPointsMin[2]), float(constantVal1), float(thermoPointsMax[0]), float(thermoPointsMax[2]))
    elif(constantVal1Title == "Temperature"):
        hI2 = interpolation(float(thermoPointsMin[1]), float(thermoPointsMin[2]), float(constantVal1), float(thermoPointsMax[1]), float(thermoPointsMax[2]))
    else:
        hI2 = interpolation(float(thermoPointsMin[3]), float(thermoPointsMin[2]), float(constantVal1), float(thermoPointsMax[3]), float(thermoPointsMax[2]))

    if(constantVal2Title == "Entropy"):
        sI2 = float(constantVal2)
    elif(constantVal1Title == "Entropy"):
        sI2 = float(constantVal1)
    elif(constantVal1Title == "Superheated Pressure"):
        sI2 = interpolation(float(thermoPointsMin[0]), float(thermoPointsMin[3]), float(constantVal1), float(thermoPointsMax[0]), float(thermoPointsMax[3]))
    elif(constantVal1Title == "Temperature"):
        sI2 = interpolation(float(thermoPointsMin[1]), float(thermoPointsMin[3]), float(constantVal1), float(thermoPointsMax[1]), float(thermoPointsMax[3]))
    else:
        sI2 = interpolation(float(thermoPointsMin[2]), float(thermoPointsMin[3]), float(constantVal1), float(thermoPointsMax[2]), float(thermoPointsMax[3]))

    Result = (pI2,tI2,hI2,sI2)
    print("the result is" + str(Result))
    # return (p2,t2,h2,s2)





superheat = HeatPumpAnalysis("D:\\reposatory\\me-program\\Files\\F001\\Properties Tables\\R410a Superheated Table.txt")
numberOfRows2 = len(superheat.get_col("Superheated Pressure"))

doubleInterpolation(71.14, "Temperature", 1.8161, "Entropy", 10, superheat, numberOfRows2)





