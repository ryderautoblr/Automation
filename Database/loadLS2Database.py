import xlrd
import os
import pathInit

class ls2Database():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "Flipkart LS2 Database with FSN.xlsx"
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_name("Products With FSN")

        startRow = 1
        rows = sheet.nrows

        self.productInfoListBusy = [[] for i in range(5)] #Name, EAN/FSN, Size, MRP, NLC
        cNos = [3,0,2,4,6]

        for r in range(startRow,rows):
            name = sheet.cell_value(r, cNos[0]).strip()
            for index,c in enumerate(cNos):
                if name:
                    self.productInfoListBusy[index].append(str(sheet.cell_value(r, c)))

    def queryFSN(self,FSN):
        matchFound = False
        matchData = ['' for i in range(6)]
        for i,x in enumerate(self.productInfoListBusy[1]):
            if x.strip() == FSN.strip():
                matchFound = True
                for jIndex in range(len(self.productInfoListBusy)-1):
                    matchData[jIndex] = self.productInfoListBusy[jIndex][i]
                matchData[-1] = float(self.productInfoListBusy[-1][i])
                matchData[-2] = "LS2"

        return matchData, matchFound
