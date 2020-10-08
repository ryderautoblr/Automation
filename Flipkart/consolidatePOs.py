import xlrd
import xlsxwriter
import copy
from os import walk
import time
import os
import excelReadProcessing
import argSortStrList
import datetime
import loadStuddsDatabase
import flipkartPOs

def matchPOwithDatabase(databases,poData):
    
    productInfoListBusy = databases[0]

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
    busyEAN = productInfoListBusy[1]

    for r in range(len(poData[0])):
        for c in range(len(poData)):
            FinalXls[outputFlipkartCols[c]].append(poData[c][r])
        name = poData[2][r]

        #To-Do Find Match
        matchFound = False

        # print (name)
        EAN = (name.split("_"))[-2]
        if "Helmet" in EAN:
            EAN = (name.split("_"))[-3]

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
    
    return FinalXls

def writeConsolidatedPOSheet(workbook,FinalXls,poName):

    worksheet = workbook.add_worksheet(poName)
    titlesWrite = ['Flipkart Name','RAA Name','Flipkart FSN','Flipkart EAN','RAA EAN','Flipkart Size','RAA Size',
                   'Flipkart Supplier MRP','RAA Supplier MRP','Flipkart Supplier Price','RAA Supplier Price', 'QTY', 'MisMatch']

    for c in range(len(titlesWrite)):
        worksheet.write(0, c, titlesWrite[c])
    
    argSort_busyNamesMapped = argSortStrList.argSortStrList(FinalXls[1])

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
    
    return FinalXls

def summarizeData(titlesWrite,writeCols,AllData,poNames):
    EANCol = 3
    QTYCol = 11
    EANList = []
    
    #summarize data
    summarized_data = [[] for i in range(len(titlesWrite) + len(poNames) + 1)]
    for l in range(len(poNames)):
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
        for c in range(len(poNames)):
            if summarized_data[len(titlesWrite) + c][r]:
                qty_sum += summarized_data[len(titlesWrite) + c][r]
        summarized_data[len(writeCols) + len(poNames)].append(qty_sum)

    # sum for each row
    for r in range(len(summarized_data[0])):
        qty_sum = 0
        for c in range(len(poNames)):
            if summarized_data[len(titlesWrite) + c][r]:
                qty_sum += summarized_data[len(titlesWrite) + c][r]
        summarized_data[len(writeCols) + len(poNames)].append(qty_sum)


    return summarized_data

def summarizeDataAndWrite(workbook,AllData,poNames,poDates):
    #Create PO Tables
    worksheet = workbook.add_worksheet()
    titlesWrite = ['Flipkart Name','RAA Name','Flipkart FSN','EAN','Size','Supplier MRP','Supplier Price']
    writeCols = [0,1,2,3,5,7,9]
    for c in range(len(titlesWrite)):
        worksheet.write(0, c, titlesWrite[c])

    summarized_data = summarizeData(titlesWrite,writeCols,AllData,poNames) #To-DO

    for l in range(len(poNames)):
        poName = poNames[l]
        worksheet.write(0, len(titlesWrite) + l, poName)
        worksheet.write(1, len(titlesWrite) + l, poDates[l])
        worksheet.write(2, len(titlesWrite) + l, 'QTY' + str(l+1))
    worksheet.write(2, len(titlesWrite) + len(poNames), 'Total Qty')

    argSort_busyNamesMapped = argSortStrList.argSortStrList(summarized_data[1])

    #sum for each column
    for c in range(len(summarized_data)):
        qty_sum = 0
        for r in range(len(summarized_data[0])):
            item_r = argSort_busyNamesMapped[r]
            worksheet.write(r+3,c,summarized_data[c][item_r])
            if summarized_data[c][item_r] and (c>=len(titlesWrite)):
                qty_sum += summarized_data[c][item_r]
        if (c >= len(titlesWrite)): worksheet.write(len(summarized_data[0]) + 3,c,qty_sum)


def consolidatePOs(loc):
    databases = []
    productInfoListBusy = loadStuddsDatabase.getStuddsDataBaseDetails()

    databases.append(productInfoListBusy)
    
    #create output
    now = datetime.datetime.now()
    workbook = xlsxwriter.Workbook('MergePO_' + now.strftime("%d_%m_%Y_%H_%M_%S") + '.xlsx')
    poDates = []
    poNames = []
    AllData = []

    for l in range(len(loc)):
        #open wb
        print (loc[l])
        poData, poName, poDate = flipkartPOs.getFlipkartPO(loc[l])
        poDates.append(poDate)
        poNames.append(poName)

        FinalXls = matchPOwithDatabase(databases,poData)
        writeConsolidatedPOSheet(workbook,FinalXls,poName)

        AllData.append(copy.deepcopy(FinalXls))

    summarizeDataAndWrite(workbook,AllData,poNames,poDates)
    workbook.close()
