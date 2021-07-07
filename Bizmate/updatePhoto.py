import os
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import math
import pandas
import wx

class updatePhoto():
  def __init__(self):
    self.names = []
    self.itemsDF = None
    self.dfNew = []
    self.newData = []
    self.wordIndex = 0
    self.file = "notFound.txt"
    
  def nextData(self):
    if len(self.dfNew[self.dfNew.columns[0]]) == self.wordIndex:
      return []
    data = self.dfNew.iloc[self.wordIndex].astype(str).to_list()
    self.wordIndex += 1
    return data

  def createDatabase(self,newDataFile,itemFile):
    self.itemsDF = pandas.read_excel(itemFile)
    if "None" not in self.itemsDF['Long Name'].astype(str).to_list():
      noneDict = {"Long Name":["None"]}
      df1 = pandas.DataFrame(noneDict)
      self.itemsDF = self.itemsDF.append(df1, ignore_index = True)
    self.names = self.itemsDF['Long Name'].astype(str).to_list()

    self.newData = pandas.read_excel(open(newDataFile, 'rb'))

    webColumns = self.newData.columns.to_list()
    webColumns.append("Temp")
    itemsCols = self.itemsDF.columns.to_list()
    for i in range(len(webColumns)):
      webColumns[i] += "_website"
      if webColumns[i] not in itemsCols:
        self.itemsDF[webColumns[i]] = ""

    self.newData.columns = webColumns

    self.dfNew = pandas.merge(self.itemsDF, self.newData, on=self.newData.columns.to_list(), how='right', indicator='Exist')
    self.dfNew = self.dfNew[self.dfNew['Exist']=="right_only"]
    self.dfNew = self.dfNew[self.newData.columns]

    f = open(self.file,"r")
    lines = f.readlines()
    f.close()

    for line in lines:
      self.existingPhotos.append(line.strip())

    self.dfNew["isExist"] = self.dfNew.apply(lambda row : self.checkInExisting(row))
    self.dfNew = self.dfNew[self.dfNew["isExist"]]
    

  def checkInExisting(self,row):
    data = ";".join(row)
    return data in self.existingPhotos


  def updatePhotoData(self,longName,data):
    if longName == "None": 
      self.existingPhotos.append(";".join(data))
    index = self.itemsDF.index[self.itemsDF['Long Name']==longName].tolist()
    
    dataCols = data.split("\n")
    for i in index:
      for j,c in enumerate(self.dfNew.columns):
        self.itemsDF[c].iloc[i] = dataCols[j]

  def writeKeywords(self,filename):
    self.itemsDF.to_excel(filename,index=False)
    f = open(self.file,"w")
    f.write("\n".join(self.existingPhotos))
    f.close()
