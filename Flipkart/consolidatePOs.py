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

def matchPOwithDatabase(poDf,databasesDf):
    columnMap = {"Title":"Flipkart Name","FSN/ISBN13":"FSN","Size":"Flipkart Size","Supplier MRP":"Flipkart MRP",
                "Supplier Price":"Flipkart NLC","Pending Quantity":"Pending Quantity"}
    poDf.rename(columns=columnMap,inplace=True)

    outputDF = pandas.merge(poDf,databasesDf,on="FSN/EAN",how="left")
    cols = ["Name", "Flipkart Name","Brand", "FSN/EAN","FSN","EAN","Size","Flipkart Size","MRP","Flipkart MRP","Flipkart NLC","Flipkart Supplier Price","Pending Quantity"]
    outputDF = outputDF[cols]
    outputDF.sort_values(by=['Name'], inplace=True)

    return outputDF

def sumDF(df,cols):
    for c in cols:
        df[c] = pandas.to_numeric(df[c])
    df = df.append(df.sum(numeric_only=True), ignore_index=True)
    df["Total"] = df[cols].sum(axis=1)

    deleteColsIndex = []
    for i,name in enumerate(df.columns.to_list()):
        if "QTY" in name:
            if df[name].iloc[-1] == 0:
                deleteColsIndex.append(i)

    df.drop(deleteColsIndex,inplace=True)    
    return df

        
def consolidatePOs(loc):    
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
    poDates = []
    poNames = []
    AllDataDf = pandas.DataFrame()
    fileName = 'MergePO_' + now.strftime("%d_%m_%Y_%H_%M_%S") + '.xlsx'
    raaDF = pandas.DataFrame(['RAA'])
    raaDF.to_excel(fileName)
    writer = pandas.ExcelWriter(fileName,engine='openpyxl', mode='a')

    for l in range(len(loc)):
        #open wb
        print (loc[l])
        poData, poName, poDate = flipkartPOs.getFlipkartPO(loc[l])
        poDates.append(poDate)
        poNames.append(poName)

        outputDF = matchPOwithDatabase(poData,databasesDf)

        df = outputDF.copy()
        df = sumDF(df,["Pending Quantity"])   
        df.to_excel(writer,sheet_name=poName,index=False)

        outputDF.rename(columns={"Pending Quantity":poName + "-QTY"},inplace=True)
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
    df = sumDF(df,sumCols)    
    df.to_excel(writer,sheet_name="Summary",index=False)
        
    noBrandDf = AllDataDf[AllDataDf['Brand'].isnull()]
    noBrandDf = sumDF(noBrandDf,sumCols)
    noBrandDf.to_excel(writer,sheet_name="Not Found",index=False)

    AllDataDf = AllDataDf[AllDataDf['Brand'].notnull()]
    brands = AllDataDf['Brand'].unique()
    
    for b in brands:
        brandDf = AllDataDf[AllDataDf['Brand']==b]
        brandDf = sumDF(brandDf,sumCols)
        brandDf.to_excel(writer,sheet_name=b,index=False)

    writer.save()
    writer.close()
    