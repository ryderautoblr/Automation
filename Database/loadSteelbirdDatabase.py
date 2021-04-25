import xlrd
import os
import pathInit
import pandas

class steelbirdDatabase():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "Steelbird FSN.xlsx"

        df = pandas.read_excel(loc)

        newColNames = {"model_name":"Name","product_id":"FSN/EAN","size":"Size"}
        df.columns = df.iloc[4] # To-Do better logic
        self.mappedDF = df[['model_name','product_id','MRP','size']]
        self.mappedDF.dropna(subset=["MRP"],inplace=True)
        self.mappedDF.drop(4,inplace=True)
        self.mappedDF = self.mappedDF.rename(columns = newColNames,inplace=False)
        self.mappedDF['FSN/EAN'] = self.mappedDF['FSN/EAN'].str.strip()
        self.mappedDF['Brand'] = "Steelbird"
        self.discount = 1-0.3392
        self.mappedDF['Flipkart Supplier Price'] = self.mappedDF['MRP'] * self.discount 
