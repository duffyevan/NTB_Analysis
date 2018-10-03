from Analysis import HeatPumpAnalysis


def doubleInteripolation(constant1, constant2, table, numberOfRows):
    
    curretRow = table.get_row(0)
    nextRow = table.get_row(1)
    currentRowNum = 0
    
    while (currentRowNum < numberOfRows):
        
        currentRowNum += 1

        if(curretRow["Superheated Pressure"] is not nextRow["Superheated Pressure"]):
            print("Current Row is" + str(curretRow))
            print("nextRow Row is" + str(nextRow))
            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)

        else:
            curretRow = nextRow
            nextRow = table.get_row(currentRowNum + 1)





superheat = HeatPumpAnalysis("D:\\reposatory\\me-program\\Files\\F001\\R410a Superheated Table.txt")
numberOfRows = len(superheat.get_col("Superheated Pressure"))
print("Number of row =" + str(numberOfRows))
doubleInteripolation(2, 8, superheat, numberOfRows)



        
        

















# def withenBounds(targetMax, targetMin, tempTarget):
#     if targetMax >= tempTarget and tempTarget >= targetMin:
#         return True
#     else:
#         return Falses