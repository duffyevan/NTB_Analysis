from Analysis import HeatPumpAnalysis

def interipolation(x1, y1, x2, x3, y3):
    y2 = (((x2-x1)*(y3-y1))/(x3-x1))+y1
    return y2


def state2_Calc(targetTemp, targetEntropy, table, numberOfRows):

    arrayI1Values = []

    upperLimitTemp = float(targetTemp + 10)
    lowerLimitTemp = float(targetTemp - 10)
    
    curretRow = table.get_row(0)
    nextRow = table.get_row(1)
    currentRowNum = 0
    
    while (currentRowNum < (numberOfRows - 2)):
        
        currentRowNum += 1

        if(curretRow["Superheated Pressure"] != nextRow["Superheated Pressure"]):
            # print("Current Row is" + str(curretRow))
            # print("nextRow Row is" + str(nextRow))
            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)

        else:
            if(((float(curretRow["Temprature"])) <= upperLimitTemp) and ((float(curretRow["Temprature"])) >= lowerLimitTemp)):
                # print("Current Row is" + str(curretRow))
                if(((float(curretRow["Entropy "])) <= targetEntropy) and ((float(nextRow["Entropy "])) >= targetEntropy)):
                    # print("Current Row is" + str(curretRow))
                    # print("nextRow Row is" + str(nextRow))
                    pI1 = curretRow["Superheated Pressure"]
                    tI1 = interipolation(float(curretRow["Entropy "]), float(curretRow["Temprature"]), targetEntropy, float(nextRow["Entropy "]), float(nextRow["Temprature"]))
                    hI1 = interipolation(float(curretRow["Entropy "]), float(curretRow["Enthalpy "]), targetEntropy, float(nextRow["Entropy "]), float(nextRow["Enthalpy "]))
                    arrayI1Values.append((pI1,tI1,hI1,targetEntropy))

            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)
            
    # print(arrayI1Values)

    thermoPointsMin = None
    thermoPointsMax = None
    Tmin = targetTemp
    Tmax = targetTemp

    for i in range(0, len(arrayI1Values)):
        thermoPoints = arrayI1Values[i]
        t =  thermoPoints[1]

        if(t <= targetTemp):
            if(Tmin == targetTemp):
                Tmin = t
                thermoPointsMin = thermoPoints

            elif(Tmin <= t and t <= targetTemp):
                Tmin = t
                thermoPointsMin = thermoPoints

        
        elif(t >= targetTemp):
                if(Tmax == targetTemp):
                    Tmax = t
                    thermoPointsMax = thermoPoints

                elif(Tmin >= t and t >= targetTemp):
                    Tmax = t
                    thermoPointsMax = thermoPoints

    # print(thermoPointsMin)
    # print(thermoPointsMax)
    
    p2 = interipolation(thermoPointsMin[1], float(thermoPointsMin[0]), targetTemp, thermoPointsMax[1], float(thermoPointsMax[0]))
    t2 = targetTemp
    h2 = interipolation(thermoPointsMin[1], thermoPointsMin[2], targetTemp, thermoPointsMax[1], thermoPointsMax[2])
    s2 = targetEntropy

    # Result = (p2,t2,h2,s2)
    # print("the result is" + str(Result))
    return (p2,t2,h2,s2)


def state1_Calc(targetTemp, table, numberOfRows):
    i = 0
 
    while(i < numberOfRows):
        rowData = table.get_row(i)

        if(i == 0):
            lowerValuePoints = rowData
            i += 1

        elif(float(rowData["Temprature"]) == targetTemp):
            return rowData

        elif(float(rowData["Temprature"]) < targetTemp):
            lowerValuePoints = rowData
            i += 1

        elif(float(rowData["Temprature"]) > targetTemp):
            higherValuePoints = rowData
            break

    pI1 = interipolation(float(lowerValuePoints["Temprature"]), float(lowerValuePoints["Pressure Gas"]), targetTemp, float(higherValuePoints["Temprature"]), float(higherValuePoints["Pressure Gas"]))
    t = targetTemp
    hI1 = interipolation(float(lowerValuePoints["Temprature"]), float(lowerValuePoints["Enthalpy Gas"]), targetTemp, float(higherValuePoints["Temprature"]), float(higherValuePoints["Enthalpy Gas"]))
    sI1 = interipolation(float(lowerValuePoints["Temprature"]), float(lowerValuePoints["Entropy Gas"]), targetTemp, float(higherValuePoints["Temprature"]), float(higherValuePoints["Entropy Gas"]))

    return (pI1,t,hI1,sI1)


def state3_Calc(targetPressure, table, numberOfRows):
    i = 0
 
    while(i < numberOfRows):
        rowData = table.get_row(i)

        if(i == 0):
            lowerValuePoints = rowData
            i += 1

        elif(float(rowData["Pressure Liquid"]) == targetPressure):
            return rowData

        elif(float(rowData["Pressure Liquid"]) < targetPressure):
            lowerValuePoints = rowData
            i += 1

        elif(float(rowData["Pressure Liquid"]) > targetPressure):
            higherValuePoints = rowData
            break

    p = targetPressure
    tI1 = interipolation(float(lowerValuePoints["Pressure Liquid"]), float(lowerValuePoints["Temprature"]), targetPressure, float(higherValuePoints["Pressure Liquid"]), float(higherValuePoints["Temprature"]))
    hI1 = interipolation(float(lowerValuePoints["Pressure Liquid"]), float(lowerValuePoints["Enthalpy Liqid"]), targetPressure, float(higherValuePoints["Pressure Liquid"]), float(higherValuePoints["Enthalpy Liqid"]))
    sI1 = interipolation(float(lowerValuePoints["Pressure Liquid"]), float(lowerValuePoints["Entropy Liquid"]), targetPressure, float(higherValuePoints["Pressure Liquid"]), float(higherValuePoints["Entropy Liquid"]))

    return (p,tI1,hI1,sI1)


def state2_Prime_Calc(thermalEnergy, powerConsumption, state1_Enthalpy, state3_Enthalpy):
    return ((thermalEnergy * state1_Enthalpy) - (powerConsumption * state3_Enthalpy))/(thermalEnergy - powerConsumption)

def effencisyCalc(state1_Enthalpy, state2_Enthalpy, state2_Prime_Enthalpy, state3_Enthalpy):
    COP_I = (state2_Enthalpy - state3_Enthalpy)/(state2_Enthalpy - state1_Enthalpy)
    COP_A = (state2_Prime_Enthalpy - state3_Enthalpy)/(state2_Prime_Enthalpy - state1_Enthalpy)
    n_Compressor = (state2_Enthalpy - state1_Enthalpy)/(state2_Prime_Enthalpy - state1_Enthalpy)
    return (COP_I, COP_A, n_Compressor)


saturated = HeatPumpAnalysis("D:\\reposatory\\me-program\\Files\\F001\\R410a Saturated Table.txt")
numberOfRows1 = len(saturated.get_col("Temprature"))

superheat = HeatPumpAnalysis("D:\\reposatory\\me-program\\Files\\F001\\R410a Superheated Table.txt")
numberOfRows2 = len(superheat.get_col("Superheated Pressure"))
# print("Number of row =" + str(numberOfRows))

Result1 = state1_Calc(-0.7, saturated, numberOfRows1)
print("The result for state 1 is: " + str(Result1))

Result2 = state2_Calc(71.14, Result1[3], superheat, numberOfRows2)
print("The result for state 2 is: " + str(Result2))

Result3 = state3_Calc(Result2[0], saturated, numberOfRows1)
print("The result for state 3 is: " + str(Result3))

Result2_Prime = state2_Prime_Calc(10.46, 3.664, Result1[2], Result3[2])
print("The result for state 2 prime is: " + str(Result2_Prime))

Profermance = effencisyCalc(Result1[2], Result2[2], Result2_Prime, Result3[2])
print("The profermance is a follows: Ideal COP = " + str(Profermance[0]) + ", Actual COP = " + str(Profermance[1]) + ", Isentropic Efficiency for Comprosser = " + str(Profermance[2]))















