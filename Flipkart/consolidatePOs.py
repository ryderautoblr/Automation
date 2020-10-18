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
import loadVegaDatabase
import loadAxorDatabase
import loadSteelbirdDatabase
import loadLS2Database
import flipkartPOs

def findMatch(databases,EAN,FSN):
    matchData = ['' for i in range(6)]
    matchFound = False

    #Get Match From Studds based on EAN
    if EAN.strip().isdigit():
        matchData, matchFound = databases[0].queryEAN(EAN)
        
    for i in range(1,len(databases)):
        #Get Match from database based on FSN
        if not matchFound:
            matchData, matchFound = databases[i].queryFSN(FSN)
            if matchFound: 
                EAN = FSN

    return matchData, matchFound

def matchPOwithDatabase(poData):
    
    studdsDatabase = loadStuddsDatabase.studdsDatabase()
    vegaDatabase = loadVegaDatabase.vegaDatabase()
    axorDatabase = loadAxorDatabase.axorDatabase()
    steelbirdDatabase = loadSteelbirdDatabase.steelbirdDatabase()
    ls2Database = loadLS2Database.ls2Database()

    databases = [studdsDatabase,vegaDatabase,axorDatabase,steelbirdDatabase,ls2Database]

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
    itemTypeList = []
    FinalXls = [flipkartTitle,busyNameMapped,flipkartFSN,EANs,busyEANMapped,flipkartSize,busySizeMapped,supplierMRP,busyMRPMapped,supplierPrice,busyLess28,qty,itemTypeList]
    outputCols = [1,4,6,8,12]
    outputFlipkartCols = [2,11,0,5,7,9]

    for r in range(len(poData[0])):
        for c in range(len(poData)):
            FinalXls[outputFlipkartCols[c]].append(poData[c][r])
        name = poData[2][r]

        # print (name)
        EAN = (name.split("_"))[-2]
        if "Helmet" in EAN:
            EAN = (name.split("_"))[-3]
        
        matchData, matchFound = findMatch(databases,EAN,flipkartFSN[-1])

        for jIndex,j in enumerate(outputCols):
            FinalXls[j].append(matchData[jIndex])
        busyLess28.append(matchData[-1])

        if matchFound:
            EANs.append(matchData[1])
        else:
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

def summarizeData(titlesWrite,writeCols,AllData,poNames,brands):
    EANCol = 3
    QTYCol = 11
    EANList = []

    brandsWisePO_qty = dict()
    brandsWisePO_index = dict()
    brandsWisePO_last_index = dict()
    for brand in brands:
        brandsWisePO_qty[brand] = [0 for i in range(len(poNames))]
        brandsWisePO_index[brand] = [-1 for i in range(len(poNames))]
        brandsWisePO_last_index[brand] = -1  

    #summarize data
    summarized_data = [[] for i in range(len(titlesWrite) + len(poNames) + 2)]
    for l in range(len(poNames)):
        if l>0: summarized_data[len(writeCols) + l] = [summarized_data[len(writeCols) + l].append('') for i in range(len(summarized_data[0]))]
        FinalXls = AllData[l]    
        for i in range(len(FinalXls[0])):
            item_r = i
            brand = FinalXls[-1][item_r]
            if FinalXls[EANCol][item_r] not in EANList:
                for c in range(len(writeCols)):
                    summarized_data[c].append(FinalXls[writeCols[c]][item_r])
                summarized_data[-1].append(FinalXls[-1][item_r])
                totalQtyPerPO = 0
                for j in range(len(FinalXls[0])):
                    if FinalXls[EANCol][j] == FinalXls[EANCol][item_r]:
                        totalQtyPerPO += FinalXls[QTYCol][j]
                for k in range(len(writeCols),len(writeCols) + l): # append null to previous qty cols
                    summarized_data[k].append('')
                summarized_data[len(writeCols) + l].append(totalQtyPerPO)
                brandsWisePO_qty[brand][l] += totalQtyPerPO
                EANList.append(FinalXls[EANCol][item_r])
            else:
                row = EANList.index(FinalXls[EANCol][item_r])
                totalQtyPerPO = 0
                for j in range(len(FinalXls[0])):
                    if FinalXls[EANCol][j] == FinalXls[EANCol][item_r]:
                        totalQtyPerPO += FinalXls[QTYCol][j]
                summarized_data[len(writeCols) + l][row] = totalQtyPerPO
                brandsWisePO_qty[brand][l] += totalQtyPerPO

    # sum for each row
    for r in range(len(summarized_data[0])):
        qty_sum = 0
        for c in range(len(poNames)):
            if summarized_data[len(titlesWrite) + c][r]:
                qty_sum += summarized_data[len(titlesWrite) + c][r]
        summarized_data[len(writeCols) + len(poNames)].append(qty_sum)

    # Get brand wise PO indicies
    for brand in brands:
        i = 0
        for l in range(len(poNames)):
            if brandsWisePO_qty[brand][l]:
                # print (brand,l,i)
                brandsWisePO_index[brand][l] = i
                brandsWisePO_last_index[brand] = i
                i += 1
            else:
                brandsWisePO_index[brand][l] = -1

    return summarized_data, brandsWisePO_qty, brandsWisePO_index, brandsWisePO_last_index

def writeSumaryTitles(worksheet,titlesWrite,poNames,poDates,brandsWisePO_index=[]):
    for c in range(len(titlesWrite)):
        worksheet.write(0, c, titlesWrite[c])


    last_index = -1
    for l in range(len(poNames)):
        index = -1    
        if not len(brandsWisePO_index):
            index = l
            last_index = index
        elif brandsWisePO_index[l] != -1:
            index = brandsWisePO_index[l]
            last_index = index
        if index >= 0:
            # print (l,index,poNames[l])
            worksheet.write(0, len(titlesWrite) + index, poNames[l])
            worksheet.write(1, len(titlesWrite) + index, poDates[l])
            worksheet.write(2, len(titlesWrite) + index, 'QTY' + str(index+1))
    worksheet.write(2, len(titlesWrite) + last_index + 1, 'Total Qty')


def summarizeDataAndWrite(workbook,AllData,poNames,poDates):
    #Create PO Tables
    worksheetSummary = workbook.add_worksheet("Summary")
    titlesWrite = ['Flipkart Name','RAA Name','Flipkart FSN','EAN','Size','Supplier MRP','Supplier Price']
    writeCols = [0,1,2,3,5,7,9]
    
    brands = ["Axor","LS2","Steelbird","Studds","Vega",""]

    summarized_data, brandsWisePO_qty, brandsWisePO_index, brandsWisePO_last_index = summarizeData(titlesWrite,writeCols,AllData,poNames,brands) #To-DO
    argSort_busyNamesMapped = argSortStrList.argSortStrList(summarized_data[1])

    brandwiseWorksheet = dict()
    item_row_for_worksheet = dict()


    writeSumaryTitles(worksheetSummary,titlesWrite,poNames,poDates)
    for brand in brands:
        brandwiseWorksheet[brand] = workbook.add_worksheet(brand)
        writeSumaryTitles(brandwiseWorksheet[brand],titlesWrite,poNames,poDates,brandsWisePO_index[brand])

        item_row_for_worksheet[brand] = 0
    
    for r in range(len(summarized_data[0])):
        qty_sum_row = 0

        item_r = argSort_busyNamesMapped[r]
        brand = summarized_data[-1][item_r]

        for c in range(len(summarized_data)):
            worksheetSummary.write(r+3,c,summarized_data[c][item_r])

            if summarized_data[c][item_r] and (c>=len(titlesWrite)) and (c<len(titlesWrite) + len(poDates)):
                qty_sum_row += summarized_data[c][item_r] #sum qty per row
                if brandsWisePO_index[brand][c - len(titlesWrite)] != -1:
                    brandwiseWorksheet[brand].write(item_row_for_worksheet[brand]+3,len(titlesWrite) + brandsWisePO_index[brand][c - len(titlesWrite)],summarized_data[c][item_r])            
            elif (c<len(titlesWrite)):
                brandwiseWorksheet[brand].write(item_row_for_worksheet[brand]+3,c,summarized_data[c][item_r])            
        brandwiseWorksheet[brand].write(item_row_for_worksheet[brand]+3,len(titlesWrite) + brandsWisePO_last_index[brand] + 1,summarized_data[-2][item_r])
        item_row_for_worksheet[brand] += 1

    # Get Brand wise and Total PO wise sum for all products in the PO
    totalSummaryQty = 0
    for l in range(len(poNames)):
        po_col_qty = 0
        for brand in brands:
            brandwiseWorksheet[brand].write(item_row_for_worksheet[brand]+3,len(titlesWrite) + brandsWisePO_index[brand][l],brandsWisePO_qty[brand][l])
            po_col_qty += brandsWisePO_qty[brand][l]
        worksheetSummary.write(len(summarized_data[0])+3,len(titlesWrite)+l,po_col_qty)
        totalSummaryQty += po_col_qty
    
    # Get Total sheet wise sum
    worksheetSummary.write(len(summarized_data[0])+3,len(titlesWrite)+len(poNames)+1,totalSummaryQty)
    for brand in brands:
        totalQtyPerBrand = 0
        for l in range(len(poNames)):
            totalQtyPerBrand += brandsWisePO_qty[brand][l]
        brandwiseWorksheet[brand].write(item_row_for_worksheet[brand]+3,len(titlesWrite) + brandsWisePO_last_index[brand] + 1,totalQtyPerBrand)
        
def consolidatePOs(loc):
    
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

        FinalXls = matchPOwithDatabase(poData)
        writeConsolidatedPOSheet(workbook,FinalXls,poName)

        AllData.append(copy.deepcopy(FinalXls))

    summarizeDataAndWrite(workbook,AllData,poNames,poDates)
    workbook.close()
