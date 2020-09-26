import xlrd
import xlsxwriter
import copy
from os import walk
import time
import os

isPendingQty = True

def argSortStrList(str_list):
    sorted_list = sorted(str_list)
    argSort = []
    prev_index=-1
    for i in range(len(sorted_list)):
        if (i>0) and (sorted_list[i-1]==sorted_list[i]):
            argSort.append(str_list.index(sorted_list[i],prev_index+1))
            prev_index = argSort[-1]
        else:
            argSort.append(str_list.index(sorted_list[i]))
            prev_index = argSort[-1]
    return argSort


def getCNos(sheet):
    cNos = []
    titleRowNo = -1
    for r in range(sheet.nrows):
        if sheet.cell_value(r,0) == 'S. no.':
            titleRowNo = r
    if isPendingQty:
        titles = ['FSN/ISBN13','Pending Quantity','Title','Size','Supplier MRP','Supplier Price']
    else:
        titles = ['FSN/ISBN13','QTY','Title','Size','Supplier MRP','Supplier Price']

    for t in titles:
        titleFound = False
        for c in range(sheet.ncols):
            if t == sheet.cell_value(titleRowNo, c):
                cNos.append(c)
                titleFound = True
                break
        if (not titleFound) and (t=='QTY'):
            for c in range(sheet.ncols):
                if sheet.cell_value(titleRowNo, c) == 'Quantity':
                    cNos.append(c)
                    titleFound = True
                    break
            

    return cNos

loc = "studdsMRPDetailsUpdated.xlsx"
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

#print (busyEAN[-2])
loc = ["C:/Users/Admin/Desktop/Flipkart/purchase_order_FMR1216928.xls","C:/Users/Admin/Desktop/Flipkart/purchase_order_FHM01216929.xls",
       "C:/Users/Admin/Desktop/Flipkart/purchase_order_FMB1216930.xls","C:/Users/Admin/Desktop/Flipkart/purchase_order_FKS01216931.xls"]


loc = []
for (dirpath, dirnames, filenames) in walk("./"):
    for file in filenames:
        if file.endswith(".xls"):
            loc.append(file)
    break

print (len(loc))

poDate = []

workbook = xlsxwriter.Workbook('MergePO.xlsx')
AllData = []
for l in range(len(loc)):
    print (l,loc[l])
    wb = xlrd.open_workbook(loc[l]) 
    sheet = wb.sheet_by_index(0)
    print(sheet.cell_value(1,sheet.ncols-2))
    poDate.append(sheet.cell_value(1,sheet.ncols-2))

    startRow = 11
    cols = sheet.ncols
    rows = sheet.nrows-3

    cNos = getCNos(sheet)
    busyNameMapped = []
    busyEANMapped = []
    busySizeMapped = []
    busyMRPMapped = []
    busyLess28 = []
    flipkartTitle = []
    flipkartFSN = []
    EANs = []
    flipkartSize = []
    supplierMRP = []
    supplierPrice = []
    qty = []
    FinalXls = [flipkartTitle,busyNameMapped,flipkartFSN,EANs,busyEANMapped,flipkartSize,busySizeMapped,supplierMRP,busyMRPMapped,supplierPrice,busyLess28,qty]
    outputCols = [1,4,6,8]
    outputFlipkartCols = [2,11,0,5,7,9]

    for r in range(startRow,rows):
        if sheet.cell_value(r, cNos[1]) == 0: continue  #skip if quantity is 0
        for index,c in enumerate(cNos):
            FinalXls[outputFlipkartCols[index]].append(sheet.cell_value(r, c))
        name = sheet.cell_value(r, cNos[2])
        # print (name)
        EAN = (name.split("_"))[-2]
        if "Helmet" in EAN:
            EAN = (name.split("_"))[-3]
        matchFound = False
        if EAN.strip().isdigit():
            for i,x in enumerate(busyEAN):
                if x.strip():
                    if int(float(x)) == int(EAN):
                        matchFound = True
                        for jIndex,j in enumerate(outputCols):
                            FinalXls[j].append(productInfoListBusy[jIndex][i])
                        busyLess28.append(float(busyMRPMapped[-1])*(1-0.28))

        if not matchFound:
            for jIndex,j in enumerate(outputCols):
                FinalXls[j].append('')
            busyLess28.append('')
        EANs.append(EAN)
                        
    
    worksheet = workbook.add_worksheet()
    titlesWrite = ['Flipkart Name','RAA Name','Flipkart FSN','Flipkart EAN','RAA EAN','Flipkart Size','RAA Size',
                   'Flipkart Supplier MRP','RAA Supplier MRP','Flipkart Supplier Price','RAA Supplier Price', 'QTY', 'MisMatch']

    for c in range(len(titlesWrite)):
        worksheet.write(0, c, titlesWrite[c])
    
    argSort_busyNamesMapped = argSortStrList(busyNameMapped)

    for r in range(len(argSort_busyNamesMapped)):
        item_r = argSort_busyNamesMapped[r]
        for c in range(len(FinalXls)):
            worksheet.write(r+1, c, FinalXls[c][item_r])
        misMatchFlag = ''
        if str(FinalXls[10][item_r]).strip():
            if float(FinalXls[9][item_r].replace("INR","")) != round(float(FinalXls[10][item_r]),1):misMatchFlag+=";Supplier Price"
            if float(FinalXls[7][item_r].replace("INR","")) != round(float(FinalXls[8][item_r]),1):misMatchFlag+=";Supplier MRP"
            if (FinalXls[5][item_r]) != (FinalXls[6][item_r]):misMatchFlag+=";Size"
        if misMatchFlag:
            worksheet.write(r+1, len(FinalXls), misMatchFlag)
    
    AllData.append(copy.deepcopy(FinalXls))

#Create PO Tables
worksheet = workbook.add_worksheet()
titlesWrite = ['Flipkart Name','RAA Name','Flipkart FSN','EAN','Size','Supplier MRP','Supplier Price']
writeCols = [0,1,2,3,5,7,9]
EANCol = 3
QTYCol = 11
EANList = []
for c in range(len(titlesWrite)):
    worksheet.write(0, c, titlesWrite[c])

#summarize data
summarized_data = [[] for i in range(len(titlesWrite) + len(loc) + 1)]
for l in range(len(loc)):
    if l>0: summarized_data[len(writeCols) + l] = [summarized_data[len(writeCols) + l].append('') for i in range(len(summarized_data[0]))]
    FinalXls = AllData[l]    
    for i in range(len(FinalXls[0])):
        item_r = i
        if FinalXls[EANCol][item_r] not in EANList:
            for c in range(len(writeCols)):
                summarized_data[c].append(FinalXls[writeCols[c]][item_r])
            totalQtyPerPO = 0
            for j in range(len(FinalXls[0])):
                if FinalXls[EANCol][j] == FinalXls[EANCol][item_r]:
                    totalQtyPerPO += FinalXls[QTYCol][j]
            for k in range(len(writeCols),len(writeCols) + l): # append null to previous qty cols
                summarized_data[k].append('')
            summarized_data[len(writeCols) + l].append(totalQtyPerPO)
            EANList.append(FinalXls[EANCol][item_r])
        else:
            row = EANList.index(FinalXls[EANCol][item_r])
            totalQtyPerPO = 0
            for j in range(len(FinalXls[0])):
                if FinalXls[EANCol][j] == FinalXls[EANCol][item_r]:
                    totalQtyPerPO += FinalXls[QTYCol][j]
            summarized_data[len(writeCols) + l][row] = totalQtyPerPO

# sum for each row
for r in range(len(summarized_data[0])):
    qty_sum = 0
    for c in range(len(loc)):
        if summarized_data[len(titlesWrite) + c][r]:
            qty_sum += summarized_data[len(titlesWrite) + c][r]
    summarized_data[len(writeCols) + len(loc)].append(qty_sum)

for l in range(len(loc)):
    poName = loc[l].split("_")[-1]
    poName = poName.split(".")[0]
    worksheet.write(0, len(titlesWrite) + l, poName)
    worksheet.write(1, len(titlesWrite) + l, poDate[l])
    worksheet.write(2, len(titlesWrite) + l, 'QTY' + str(l+1))
worksheet.write(2, len(titlesWrite) + len(loc), 'Total Qty')

argSort_busyNamesMapped = argSortStrList(summarized_data[1])

#sum for each column
for c in range(len(summarized_data)):
    qty_sum = 0
    for r in range(len(summarized_data[0])):
        item_r = argSort_busyNamesMapped[r]
        worksheet.write(r+3,c,summarized_data[c][item_r])
        if summarized_data[c][item_r] and (c>=len(titlesWrite)):
            qty_sum += summarized_data[c][item_r]
    if (c >= len(titlesWrite)): worksheet.write(len(summarized_data[0]) + 3,c,qty_sum)

    
workbook.close()