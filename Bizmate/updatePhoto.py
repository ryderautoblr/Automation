import os
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import math
import pandas
import wx
import numpy as np

class updatePhoto():
  def __init__(self):
    self.names = []
    self.itemsDF = None
    self.dfNew = []
    self.newData = []
    self.wordIndex = 0
    self.file = pathInit.getBaseFolder() + "\\Bizmate\\notFound.txt"
    self.existingPhotos = []
    
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
    itemsCols = self.itemsDF.columns.to_list()
    for i in range(len(webColumns)):
      webColumns[i] += "_website"
      if webColumns[i] not in itemsCols:
        self.itemsDF[webColumns[i]] = ""

    self.newData.columns = webColumns
   
    self.itemsDF.replace(np.nan,'nan',regex=True,inplace=True)
    self.newData.replace(np.nan,'nan',regex=True,inplace=True)

    
    self.dfNew = pandas.merge(self.itemsDF, self.newData, on=self.newData.columns.to_list(), how='right', indicator='Exist')
    self.dfNew = self.dfNew[self.dfNew['Exist']=="right_only"]
    self.dfNew = self.dfNew[self.newData.columns]
    # print (self.dfNew.iloc[0].to_list(),self.itemsDF[self.itemsDF['Color_website']==self.dfNew['Color_website'].iloc[0]].iloc[0].to_list()[22:])
    # for i in range(22,31):
    #   if self.dfNew.iloc[0].to_list()[i-22] == self.itemsDF[self.itemsDF['Color_website']==self.dfNew['Color_website'].iloc[0]].iloc[0].to_list()[i]:
    #     print ("here",i)
    # print (self.dfNew.iloc[0].to_list()[5],self.itemsDF[self.itemsDF['Color_website']==self.dfNew['Color_website'].iloc[0]].iloc[0].to_list()[27])

    lines = []
    if os.path.isfile(self.file):
      f = open(self.file,"r")
      lines = f.readlines()
      f.close()

    for line in lines:
      self.existingPhotos.append(line.strip())

    self.dfNew["isExist"] = self.dfNew.apply(lambda row : self.checkInExisting(row),axis=1)
    self.dfNew = self.dfNew[self.dfNew["isExist"]]
    self.dfNew.drop("isExist",inplace=True,axis=1)
    

  def checkInExisting(self,row):
    row = row.replace(np.nan, 'nan', regex=True)
    row = row.astype(str)
    data = ";".join(row)
    data = data.replace("\n",";")
    isPhoto = data in self.existingPhotos
    # print (isPhoto)
    return not isPhoto

  def updatePhotoData(self,longName,data):
    data = data.split("\n")
    if longName == "None":
      self.existingPhotos.append(";".join(data))
    index = self.itemsDF.index[self.itemsDF['Long Name']==longName].tolist()
    
    for i in index:
      for j,c in enumerate(self.dfNew.columns):
        self.itemsDF[c].iloc[i] = data[j]

  def writeKeywords(self,filename):
    self.itemsDF.to_excel(filename,index=False)
    f = open(self.file,"w")
    f.write("\n".join(self.existingPhotos))
    f.close()
