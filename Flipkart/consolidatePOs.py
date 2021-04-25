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
import pandas
import numpy as np
import math
import datetime
import locale

def matchPOwithDatabase(poDf,databasesDf):
    columnMap = {"Title":"Flipkart Name","FSN/ISBN13":"FSN","Size":"Flipkart Size","Supplier MRP":"Flipkart MRP",
                "Supplier Price":"Flipkart NLC","Pending Quantity":"Pending Quantity"}
    poDf.rename(columns=columnMap,inplace=True)

    outputDF = pandas.merge(poDf,databasesDf,on="FSN/EAN",how="left")
    outputDF.sort_values(by=['Name'], inplace=True)

    return outputDF

def sumDF(df,cols,dateDict):
    for c in cols:
        df[c] = pandas.to_numeric(df[c])
    df = df.append(df.sum(numeric_only=True), ignore_index=True)
    df["Total"] = df[cols].sum(axis=1)

    cols = df.columns
    dateDF = pandas.DataFrame(dateDict)
    df = dateDF.append(df)
    df = df[cols]

    for i,name in enumerate(df.columns.to_list()):
        if "QTY" in name:
            if df[name].iloc[-1] == 0:
                df.drop(name,axis=1,inplace=True)
    
    return df

        
def consolidatePOs(loc):    
    cols = ["Name", "Flipkart Name","Brand", "FSN/EAN","FSN","EAN","Size","Flipkart Size","MRP","Flipkart MRP","Flipkart NLC","Flipkart Supplier Price","Pending Quantity"]
    
    studdsDatabase = loadStuddsDatabase.studdsDatabase()
    vegaDatabase = loadVegaDatabase.vegaDatabase()
    axorDatabase = loadAxorDatabase.axorDatabase()
    steelbirdDatabase = loadSteelbirdDatabase.steelbirdDatabase()
    ls2Database = loadLS2Database.ls2Database()

    databases = [studdsDatabase,vegaDatabase,axorDatabase,steelbirdDatabase,ls2Database]
    databasesDf = pandas.DataFrame()
    for i in range(len(databases)):
        databasesDf = databasesDf.append(databases[i].mappedDF,ignore_index=True)
    
    #create output

    now = datetime.datetime.now()
    allData = []
    dateObjs = []
    AllDataDf = pandas.DataFrame()
    fileName = 'MergePO_' + now.strftime("%d_%m_%Y_%H_%M_%S") + '.xlsx'
    raaDF = pandas.DataFrame(['RAA'])
    raaDF.to_excel(fileName)
    writer = pandas.ExcelWriter(fileName,engine='openpyxl', mode='a')

    locale.setlocale(locale.LC_ALL, "pt_br")
    for l in range(len(loc)):
        #open wb
        print (loc[l])
        poData, poName, poDate = flipkartPOs.getFlipkartPO(loc[l])
        dateObj = datetime.datetime.strptime(poDate,"%d-%m-%y")
        allData.append((dateObj,poData,poName,poDate))
        dateObjs.append(dateObj)
    
    indexes = np.argsort(dateObjs)
    poDateDict = dict()
    for i in range(len(allData)):
        poData = allData[indexes[i]][1]
        poName = allData[indexes[i]][2]
        poDate = allData[indexes[i]][3]
        
        outputDF = matchPOwithDatabase(poData,databasesDf)
        outputDF = outputDF[cols]

        df = outputDF.copy()
        dateDict = {"Pending Quantity":[poDate]}
        df = sumDF(df,["Pending Quantity"],dateDict)   
        df.to_excel(writer,sheet_name=poName,index=False)

        outputDF.rename(columns={"Pending Quantity":poName + "-QTY"},inplace=True)
        poDateDict[poName+"-QTY"] = [poDate]
        AllDataDf = AllDataDf.append(outputDF)
    
    aggregation_functions = dict()
    sumCols = []
    for name in AllDataDf.columns:
        if "QTY" in name:
            aggregation_functions[name] = 'sum'
            sumCols.append(name)
        else:
            aggregation_functions[name] = 'first'

    AllDataDf = AllDataDf.groupby(AllDataDf['FSN']).aggregate(aggregation_functions)
    AllDataDf.sort_values(by=['Name'], inplace=True)

    df = AllDataDf.copy()
    df = sumDF(df,sumCols,poDateDict)    
    df.to_excel(writer,sheet_name="Summary",index=False)
        
    noBrandDf = AllDataDf[AllDataDf['Brand'].isnull()]
    noBrandDf = sumDF(noBrandDf,sumCols,poDateDict)
    noBrandDf.to_excel(writer,sheet_name="Not Found",index=False)

    AllDataDf = AllDataDf[AllDataDf['Brand'].notnull()]
    brands = AllDataDf['Brand'].unique()
    
    for b in brands:
        brandDf = AllDataDf[AllDataDf['Brand']==b]
        brandDf = sumDF(brandDf,sumCols,poDateDict)
        brandDf.to_excel(writer,sheet_name=b,index=False)

    writer.save()
    writer.close()
    