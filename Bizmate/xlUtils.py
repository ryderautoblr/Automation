import xlrd

class xlUtils():
  def getSheet(self,filename,sheetNo):
    sheet = xlrd.open_workbook(filename).sheet_by_index(sheetNo)
    return sheet

  def getHeadings(self,rowNo,sheet):
    headings = []
    if rowNo < 0:
        return headings
    cols = sheet.ncols
    for c in range(cols):
        headings.append(sheet.cell_value(rowNo, c))
    return headings

  def getData(self,startRowIndex,sheet):
    rows = sheet.nrows
    cols = sheet.ncols
    data = [[] for c in range(cols)]
    for c in range(cols):
        for r in range(startRowIndex,rows):
            data[c].append(sheet.cell_value(r, c))
    return data
