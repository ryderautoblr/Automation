import xlrd
import os
import pathInit

class studdsDatabase():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "studdsMRPDetailsUpdated.xlsx"
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0)

        startRow = 1
        rows = sheet.nrows

        self.productInfoListBusy = [[] for i in range(4)]
        cNos = [6,10,8,9]

        for r in range(startRow,rows):
            for index,c in enumerate(cNos):
                if sheet.cell_value(r, cNos[0]).strip():
                    if index == 1: #Insert EAN as integer
                        x = str(sheet.cell_value(r, c)).strip() 
                        if x:
                            self.productInfoListBusy[index].append(int(float(x)))
                        else:
                            self.productInfoListBusy[index].append(-1)
                    else:#other fields 
                        self.productInfoListBusy[index].append(str(sheet.cell_value(r, c)))

    def queryEAN(self,EAN):
        matchFound = False
        matchData = ['' for i in range(6)]
        itemType = ''
        for i,x in enumerate(self.productInfoListBusy[1]):
            if x == int(EAN):
                matchFound = True
                for jIndex in range(len(self.productInfoListBusy)):
                    matchData[jIndex] = self.productInfoListBusy[jIndex][i]
                matchData[-1] = float(matchData[-3])*(1-0.28)
                matchData[-2] = "Studds" 

        return matchData, matchFound
