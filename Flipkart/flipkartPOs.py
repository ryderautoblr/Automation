import xlrd
import excelReadProcessing
import pandas
import numpy as np

def getPOTitleRowNo(df):
    titleRowNo = -1 #get Title 
    for r in range(sheet.nrows):
        if sheet.cell_value(r,0) == 'S. no.':
            titleRowNo = r
    return titleRowNo

def getFlipkartPO(loc,isSkipZeroQty=True):
    df = pandas.read_excel(loc)

    #read PO Date:
    poDate = df.iloc[0][-2]

    indexes = df[df['Flipkart']=="S. no."].index.values
    df.columns = df.iloc[indexes[0]]
    df.drop(df.head(indexes[0]+1).index,inplace=True)
    df.drop(df.tail(3).index,inplace=True)
    
    #get PO columns of interest
    titles = ['FSN/ISBN13','Pending Quantity','Title','Size','Supplier MRP','Supplier Price']
    df = df[titles]
        
    #get PO Data
    poName = loc.split("_")[-1]
    poName = poName.split(".")[0]
    
    df = df[df['Pending Quantity'] != 0]
    df["EAN"] = df["Title"].str.split("_").str[-2]
    df["EAN"] = np.where(("Helmet" in df.EAN),df["Title"].str.split("_").str[-3],df.EAN)
    df["FSN/EAN"] = np.where(df.EAN.str.isdigit(),df["EAN"],df["FSN/ISBN13"])
    return df, poName, poDate