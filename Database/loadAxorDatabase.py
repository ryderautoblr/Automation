import xlrd
import os
import pathInit
import pandas

class axorDatabase():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "AXOR FSN.xlsx"
       
        df = pandas.read_excel(loc)

        newColNames = {"Model Name":"Name","FSN":"FSN/EAN"}
        self.mappedDF = df.rename(columns = newColNames,inplace=False)
        self.mappedDF['Size'] = self.mappedDF['Name'].str.split("-").str[-1]
        self.mappedDF['FSN/EAN'] = self.mappedDF['FSN/EAN'].str.strip()
        self.mappedDF['Brand'] = "Axor"
        self.discount = 1-0.33
        self.mappedDF['Flipkart Supplier Price'] = self.mappedDF['MRP'] * self.discount 
