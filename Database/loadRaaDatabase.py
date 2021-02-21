import xlrd
import os
import pathInit

class raaDatabase():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "RAA.xlsx"
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0)

        startRow = 3
        rows = sheet.nrows

        self.productInfoListBusy = [[] for i in range(4)] #Name, EAN/FSN, Size, MRP
        cNos = [0,[2,3,4],5,8]

        for r in range(startRow,rows):
            name = sheet.cell_value(r, cNos[0]).strip()
            for index,c in enumerate(cNos):
                if name:
                    if index == 1:
                        FSNs = []
                        for col in cNos[1]:
                            alias = sheet.cell_value(r,col)
                            if alias.startswith("HLM"):
                                FSNs.append(alias)
                        self.productInfoListBusy[index].append(FSNs)
                    else:
                        self.productInfoListBusy[index].append(str(sheet.cell_value(r, c)))

    def queryFSN(self,FSN):
        matchFound = False
        matchData = ['' for i in range(6)]
        for i,x in enumerate(self.productInfoListBusy[1]):
            for fsn in x:
                if fsn.strip() == FSN.strip():
                    matchFound = True
                    for jIndex in range(len(self.productInfoListBusy)):
                        if jIndex == 1:
                            matchData[jIndex] = fsn.strip()
                        else:
                            matchData[jIndex] = self.productInfoListBusy[jIndex][i]
                    matchData[-1] = float(matchData[-3])*(1-0.33)
                    matchData[-2] = "RAA"

        return matchData, matchFound

    def getNames(self):
        return self.productInfoListBusy[0]
