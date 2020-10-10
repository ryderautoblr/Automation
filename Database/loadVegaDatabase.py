import xlrd
import os
import pathInit

class vegaDatabase():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "VEGA MASTER LIST WITH FLIPKART FSN.xlsx"
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0)

        startRow = 1
        rows = sheet.nrows

        self.productInfoListBusy = [[] for i in range(4)] #Name, EAN/FSN, Size, MRP
        cNos = [2,0,-1,1]

        for r in range(startRow,rows):
            name = sheet.cell_value(r, cNos[0]).strip()
            for index,c in enumerate(cNos):
                if name:
                    if index == 2: #Get Size
                        size = name.split("-")[-1].strip()
                        self.productInfoListBusy[index].append(size)
                    else: #other fields 
                        self.productInfoListBusy[index].append(str(sheet.cell_value(r, c)))

    def queryFSN(self,FSN):
        matchFound = False
        matchData = ['' for i in range(6)]
        for i,x in enumerate(self.productInfoListBusy[1]):
            if x.strip() == FSN.strip():
                matchFound = True
                for jIndex in range(len(self.productInfoListBusy)):
                    matchData[jIndex] = self.productInfoListBusy[jIndex][i]
                matchData[-1] = float(matchData[-3])*(1-0.3)
                matchData[-2] = "Vega"

        return matchData, matchFound
