import xlrd
import os
import pathInit
import pandas

class vegaDatabase():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "VEGA MASTER LIST WITH FLIPKART FSN.xlsx"
        df = pandas.read_excel(loc)

        newColNames = {"MODEL":"Name","FSN":"FSN/EAN"}
        self.mappedDF = df.rename(columns = newColNames,inplace=False)
        self.mappedDF = self.mappedDF[["Name","FSN/EAN","MRP"]]
        self.mappedDF['Size'] = self.mappedDF['Name'].str.split("-").str[-1]
        self.mappedDF['FSN/EAN'] = self.mappedDF['FSN/EAN'].str.strip()
        self.mappedDF['Brand'] = "Vega"
        self.discount = 1-0.3
        self.mappedDF['Flipkart Supplier Price'] = self.mappedDF['MRP'] * self.discount 
