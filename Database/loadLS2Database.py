import xlrd
import os
import pathInit
import pandas

class ls2Database():
    def __init__(self):
        baseFolder = pathInit.getBaseFolder() + "Database\\"

        loc = baseFolder + "Flipkart LS2 Database with FSN.xlsx"
       
        df = pandas.read_excel(loc,sheet_name=2)

        newColNames = {"Model Name":"Name","Total FSN":"FSN/EAN","DP":"Flipkart Supplier Price"}
        self.mappedDF = df[['Model Name','Total FSN','MRP','Size','DP']]
        self.mappedDF.rename(columns = newColNames,inplace=True)
        self.mappedDF['FSN/EAN'] = self.mappedDF['FSN/EAN'].str.strip()
        self.mappedDF['Brand'] = "LS2"
        