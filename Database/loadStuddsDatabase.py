import xlrd
import os
import pathInit

def getStuddsDataBaseDetails():
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

    productInfoListBusy = [busyName,busyEAN,busySize,busyMRP]
    cNos = [6,10,8,9]

    for r in range(startRow,rows):
        for index,c in enumerate(cNos):
            if sheet.cell_value(r, 6).strip():
                productInfoListBusy[index].append(str(sheet.cell_value(r, c)))

    return productInfoListBusy
