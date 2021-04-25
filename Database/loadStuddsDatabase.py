import xlrd
import os
import pathInit
import pandas

class studdsDatabase():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "studdsMRPDetailsUpdated.xlsx"
        df = pandas.read_excel(loc)


        newColNames = {"BusyName":"Name","Barcode":"FSN/EAN"}
        self.mappedDF = df[['BusyName','Barcode','MRP','Size']]
        self.mappedDF.rename(columns = newColNames,inplace=True)
        self.mappedDF['FSN/EAN'] = self.mappedDF['FSN/EAN'].str.strip()
        self.mappedDF['Brand'] = "Studds"
        self.discount = 1-0.28
        self.mappedDF['Flipkart Supplier Price'] = self.mappedDF['MRP'] * self.discount 