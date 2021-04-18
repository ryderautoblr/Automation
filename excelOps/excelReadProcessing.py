import xlrd
import pandas

def getSheet(filename,sheetNo=0):
    sheet = xlrd.open_workbook(filename).sheet_by_index(sheetNo)
    return sheet

def getHeadings(rowNo,sheet):
    headings = []
    if rowNo < 0:
        return headings
    cols = sheet.ncols
    for c in range(cols):
        headings.append(sheet.cell_value(rowNo, c))
    return headings

def getData(sheet,startRowIndex=0):
    rows = sheet.nrows
    cols = sheet.ncols
    data = [[] for c in range(cols)]
    for c in range(cols):
        for r in range(startRowIndex,rows):
            data[c].append(sheet.cell_value(r, c))
    return data

def closeWorkbook(workbook):
    del workbook

def getMaxCols(sheet):
    return sheet.ncols

def getPD(filename):
    return pandas.read_excel(filename)

def getColumnNumbers(sheet,titleRowNo,titles):
    cNos = []
    for t in titles:
        titleFound = False
        for c in range(sheet.ncols):
            if t == sheet.cell_value(titleRowNo, c):
                cNos.append(c)
                titleFound = True
                break
        if not titleFound:
            cNos.append(-1)        
    return cNos