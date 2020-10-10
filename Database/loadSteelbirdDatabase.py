import xlrd
import os
import pathInit

class steelbirdDatabase():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "Steelbird FSN.xlsx"
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0)

        startRow = 7
        rows = sheet.nrows

        self.productInfoListBusy = [[] for i in range(4)] #Name, EAN/FSN, Size, MRP
        cNos = [6,3,8,11]

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
                for jIndex in range(len(self.productInfoListBusy)):
                    matchData[jIndex] = self.productInfoListBusy[jIndex][i]
                matchData[-1] = float(matchData[-3])*(1-0.3392)
                matchData[-2] = "Steelbird"

        return matchData, matchFound
