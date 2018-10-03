from Analysis import HeatPumpAnalysis

def interipolation(x1, y1, x2, x3, y3):
    y2 = (((x2-x1)*(y3-y1))/(x3-x1))+y1
    return y2


def doubleInteripolation(constant1, constant2, table, numberOfRows):

    arrayI1Values = []

    upperLimitTemp = float(constant1 + 10)
    lowerLimitTemp = float(constant1 - 10)
    
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
                if(((float(curretRow["Entropy "])) <= constant2) and ((float(nextRow["Entropy "])) >= constant2)):
                    print("Current Row is" + str(curretRow))
                    print("nextRow Row is" + str(nextRow))
                    pI1 = curretRow["Superheated Pressure"]
                    tI1 = interipolation(float(curretRow["Entropy "]), float(curretRow["Temprature"]), constant2, float(nextRow["Entropy "]), float(nextRow["Temprature"]))
                    hI1 = interipolation(float(curretRow["Entropy "]), float(curretRow["Enthalpy "]), constant2, float(nextRow["Entropy "]), float(nextRow["Enthalpy "]))
                    arrayI1Values.append((pI1,tI1,hI1,constant2))

            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)
            
    print(arrayI1Values)

    thermoPointsMin = []
    thermoPointsMax = []
    Tmin = constant1
    Tmax = constant1

    for i in range(0, len(arrayI1Values)):
        thermoPoints = arrayI1Values[i]
        t =  thermoPoints[1]

        if(t <= constant1):
            if(Tmin == constant1):
                Tmin = t
                thermoPointsMin.append(thermoPoints)

            elif(Tmin <= t and t <= constant1):
                Tmin = t
                thermoPointsMin.append(thermoPoints)

        
        elif(t >= constant1):
                if(Tmax == constant1):
                    Tmax = t
                    thermoPointsMax.append(thermoPoints)

                elif(Tmin >= t and t >= constant1):
                    Tmax = t
                    thermoPointsMax.append(thermoPoints)

    print(thermoPointsMin)
    print(thermoPointsMax)



superheat = HeatPumpAnalysis("D:\\reposatory\\me-program\\Files\\F001\\R410a Superheated Table.txt")
numberOfRows = len(superheat.get_col("Superheated Pressure"))
print("Number of row =" + str(numberOfRows))
doubleInteripolation(28.2, 1.925, superheat, numberOfRows)




# y2 = interipolation(5, 20, 8, 10, 50)       
# print(y2)
        

















