import xlrd
import excelReadProcessing

def getPOTitleRowNo(sheet):
    titleRowNo = -1 #get Title 
    for r in range(sheet.nrows):
        if sheet.cell_value(r,0) == 'S. no.':
            titleRowNo = r
    return titleRowNo

def getFlipkartPO(loc):
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)

    #read PO Date:
    poDate = sheet.cell_value(1,sheet.ncols-2)

    #get PO columns of interest
    titleRowNo = getPOTitleRowNo(sheet)
    titles = ['FSN/ISBN13','Pending Quantity','Title','Size','Supplier MRP','Supplier Price']
    cNos = excelReadProcessing.getColumnNumbers(sheet,titleRowNo,titles)

    if len(cNos) != len(titles):
        print ("Error: PO Process Error: Not able to find a column heading")

    #get PO Data
    poName = loc.split("_")[-1]
    poName = poName.split(".")[0]
    
    cols = sheet.ncols
    rows = sheet.nrows-3

    poData = [[] for i in range(len(titles))]

    for r in range(titleRowNo+1,rows):
        if sheet.cell_value(r, cNos[1]) == 0: continue  #skip if quantity is 0
        for index,c in enumerate(cNos):
            poData[index].append(sheet.cell_value(r, c))

    return poData, poName, poDate