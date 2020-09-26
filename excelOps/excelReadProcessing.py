import xlrd

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