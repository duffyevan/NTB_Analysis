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
            pI1 = float(rowData["Pressure Gas"])
            t = targetTemp
            hI1 = float(rowData["Enthalpy Gas"])
            sI1 = float(rowData["Entropy Gas"])
            return (pI1,t,hI1,sI1)

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
            pI1 = targetPressure
            t = float(rowData["Temprature"])
            hI1 = float(rowData["Enthalpy Liqid"])
            sI1 = float(rowData["Entropy Liquid"])
            return (pI1,t,hI1,sI1)

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

def state2_Prime_Calc2(thermalEnergy, powerConsumption, state1_Enthalpy, state3_Enthalpy, state3_Pressure, table, numberOfRows):
    h3 = ((thermalEnergy * state1_Enthalpy) - (powerConsumption * state3_Enthalpy))/(thermalEnergy - powerConsumption)

    arrayI1Values = []
    upperLimitTemp = float(state3_Pressure + 200)
    lowerLimitTemp = float(state3_Pressure - 200)
    
    curretRow = table.get_row(0)
    nextRow = table.get_row(1)
    currentRowNum = 0
    
    while (currentRowNum < (numberOfRows - 2)):
        
        currentRowNum += 1

        if(curretRow["Superheated Pressure"] != nextRow["Superheated Pressure"]):
            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)

        else:
            if(((float(curretRow["Superheated Pressure"])) <= upperLimitTemp) and ((float(curretRow["Superheated Pressure"])) >= lowerLimitTemp)):
                if(((float(curretRow["Enthalpy "])) <= h3) and ((float(nextRow["Enthalpy "])) >= h3)):
                    pI1 = curretRow["Superheated Pressure"]
                    tI1 = interipolation(float(curretRow["Enthalpy "]), float(curretRow["Temprature"]), h3, float(nextRow["Enthalpy "]), float(nextRow["Temprature"]))
                    hI1 = h3
                    sI1 = interipolation(float(curretRow["Enthalpy "]), float(curretRow["Entropy "]), h3, float(nextRow["Enthalpy "]), float(nextRow["Entropy "]))
                    arrayI1Values.append((pI1,tI1,hI1,sI1))

            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)
            
    print(arrayI1Values)

    thermoPointsMin = None
    thermoPointsMax = None
    Pmin = state3_Pressure
    Pmax = state3_Pressure

    for i in range(0, len(arrayI1Values)):
        thermoPoints = arrayI1Values[i]
        p =  float(thermoPoints[0])
        
        if(p <= state3_Pressure):
            if(Pmin == state3_Pressure):
                Pmin = p
                thermoPointsMin = thermoPoints

            elif(Pmin <= p and p <= state3_Pressure):
                Pmin = p
                thermoPointsMin = thermoPoints

        
        elif(p >= state3_Pressure):
                if(Pmax == state3_Pressure):
                    Pmax = p
                    thermoPointsMax = thermoPoints

                elif(Pmin >= p and p >= state3_Pressure):
                    Pmax = p
                    thermoPointsMax = thermoPoints

    print(thermoPointsMin)
    print(thermoPointsMax)
    
    p2 = state3_Pressure
    t2 = interipolation(float(thermoPointsMin[0]), float(thermoPointsMin[1]), float(state3_Pressure), float(thermoPointsMax[0]), float(thermoPointsMax[1]))
    h2 = h3
    s2 = interipolation(float(thermoPointsMin[0]), thermoPointsMin[3], float(state3_Pressure), float(thermoPointsMax[0]), thermoPointsMax[3])

    Result = (p2,t2,h2,s2)
    print("the result is" + str(Result))
    # return (p2,t2,h2,s2)

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


def dataCalc(dataSheet, saturatedTable, superHeatedTable):
    rawData = HeatPumpAnalysis(dataSheet)
    numberOfRows = len(rawData.get_col("Datum/Winterzeit"))
    print("number of rows in data sheet = " + str(numberOfRows))

    saturated = HeatPumpAnalysis(saturatedTable)
    numberOfRows1 = len(saturated.get_col("Temprature"))
    print("number of rows in saturated table = " + str(numberOfRows1))

    superheat = HeatPumpAnalysis(superHeatedTable)
    numberOfRows2 = len(superheat.get_col("Superheated Pressure"))
    print("number of rows in supersaturated table = " + str(numberOfRows2))

    HeatCapacityOfWater = 4.1855
    arrayResults = []

    i=0
    while(i < numberOfRows):
        curretRow = rawData.get_row(i)
        
        if("d10010001" == curretRow["47_Dig"]):
            dateTime = curretRow["Datum/Winterzeit"]
            print(dateTime)
            waterInletTemp = float(curretRow["03_Sein1"])/100
            condensorTemp = waterInletTemp + 20
            waterOutletTemp = float(curretRow["09_Aaus1"])/100
            waterFlowRate = float(curretRow["22_Vaufl"])/60
            airInletTemp = float(curretRow["07_Qein1"])/100
            evaporatorTemp = airInletTemp - 20
            compressorPower = float(curretRow["27_PelV"])/1000
            
            ThermalEnergy = thermalEnergyCalc(waterFlowRate, waterInletTemp, waterOutletTemp, HeatCapacityOfWater)
            
            state1_Result = state1_Calc(evaporatorTemp, saturated, numberOfRows1)
            state2_Result = state2_Calc(condensorTemp, state1_Result[3], superheat, numberOfRows2)
            state3_Result = state3_Calc(state2_Result[0], saturated, numberOfRows1)
            state4_Result = (state1_Result[0], state1_Result[1], state3_Result[0], "Not Found")
            state2_Prime_Result = state2_Prime_Calc(ThermalEnergy, compressorPower, state1_Result[2], state3_Result[2])
            preformanceResult = effencisyCalc(state1_Result[2], state2_Result[2], state2_Prime_Result, state3_Result[2])

            arrayResults.append((preformanceResult, state1_Result, state2_Result, state2_Prime_Result, state3_Result, state4_Result, dateTime, waterInletTemp, waterOutletTemp, waterFlowRate, airInletTemp, compressorPower, ThermalEnergy, condensorTemp, evaporatorTemp))

            i +=1

        else:
            i +=1

    return arrayResults




superheat = HeatPumpAnalysis("D:\\reposatory\\me-program\\Files\\F001\\Properties Tables\\R410a Superheated Table.txt")
numberOfRows2 = len(superheat.get_col("Superheated Pressure"))

state2_Prime_Calc2(10.16, 3.06, 422.2, 274.8, 2662.4, superheat, numberOfRows2)

# Results = dataCalc("D:\\reposatory\\me-program\\Files\\F001\\Files\\F001_20180829_000002 - Copy.xls", "D:\\reposatory\\me-program\\Files\\F001\\Properties Tables\\R410a Saturated Table.txt", "D:\\reposatory\\me-program\\Files\\F001\\Properties Tables\\R410a Superheated Table.txt")
# print(Results)

    # saturated = HeatPumpAnalysis("D:\\reposatory\\me-program\\Files\\F001\\Properties Tables\\R410a Saturated Table.txt")
    # numberOfRows1 = len(saturated.get_col("Temprature"))

    # superheat = HeatPumpAnalysis("D:\\reposatory\\me-program\\Files\\F001\\Properties Tables\\R410a Superheated Table.txt")
    # numberOfRows2 = len(superheat.get_col("Superheated Pressure"))


    # Result1 = state1_Calc(-1.0, saturated, numberOfRows1)
    # print("The result for state 1 is: " + str(Result1))

    # Result2 = state2_Calc(64.04, Result1[3], superheat, numberOfRows2)
    # print("The result for state 2 is: " + str(Result2))

    # Result3 = state3_Calc(Result2[0], saturated, numberOfRows1)
    # print("The result for state 3 is: " + str(Result3))

    # ThermalEnergy = thermalEnergyCalc(27.8, 51.14, 56.43, 4.1855)
    # print("The Thermal Energy is: " + str(ThermalEnergy))

    # Result2_Prime = state2_Prime_Calc(ThermalEnergy, 3.664, Result1[2], Result3[2])
    # print("The result for state 2 prime is: " + str(Result2_Prime))

    # Profermance = effencisyCalc(Result1[2], Result2[2], Result2_Prime, Result3[2])
    # print("The profermance is a follows: Ideal COP = " + str(Profermance[0]) + ", Actual COP = " + str(Profermance[1]) + ", Isentropic Efficiency for Comprosser = " + str(Profermance[2]))















