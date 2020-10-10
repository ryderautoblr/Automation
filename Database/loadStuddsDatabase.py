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

        flipkartTitle = []
        busyName = []
        flipkartFSN = []
        EANs = []
        busyEAN = []
        flipkartSize = []
        busySize = []
        supplierMRP = []
        busyMRP = []
        supplierPrice = []
        qty = []

        self.productInfoListBusy = [busyName,busyEAN,busySize,busyMRP]
        cNos = [6,10,8,9]

        for r in range(startRow,rows):
            for index,c in enumerate(cNos):
                if sheet.cell_value(r, 6).strip():
                    if index == 1: #Insert EAN as integer
                        x = str(sheet.cell_value(r, c)).strip() 
                        if x:
                            self.productInfoListBusy[index].append(int(float(x)))
                        else:
                            self.productInfoListBusy[index].append(-1)
                    else:#other fields 
                        self.productInfoListBusy[index].append(str(sheet.cell_value(r, c)))

    def queryEAN(self,EAN):
        matchData = ['' for i in range(5)]
        for i,x in enumerate(self.productInfoListBusy[1]):
            if x == int(EAN):
                for jIndex in range(len(self.productInfoListBusy)):
                    matchData[jIndex] = self.productInfoListBusy[jIndex][i]
                matchData[-1] = float(matchData[-2])*(1-0.28)

        return matchData
