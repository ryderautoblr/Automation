import os
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import math
import pandas
import wx

class updateFSN():
  def __init__(self):
    self.names = []
    self.itemsDF = None
    self.newFSNs = []
    self.updateFSNs = dict()
    self.wordIndex = 0
    self.notFoundFSN = "notFoundFSN.txt"

  def nextFSN(self):
    if len(self.newFSNs['FSN']) == self.wordIndex:
      return None,[]
    fsnData = self.newFSNs.iloc[self.wordIndex].astype(str).to_list()
    fsn = self.newFSNs['FSN'].iloc[self.wordIndex]
    self.wordIndex += 1
    return fsn,fsnData

  def createFSNDatabase(self,newFSNFile,itemFile):
    self.itemsDF = pandas.read_excel(itemFile)
    if "None" not in self.itemsDF['Long Name'].astype(str).to_list():
      noneDict = {"Long Name":["None"]}
      df1 = pandas.DataFrame(noneDict)
      self.itemsDF = self.itemsDF.append(df1, ignore_index = True)

    self.names = self.itemsDF['Long Name'].astype(str).to_list()
    self.newFSNs = pandas.read_excel(open(newFSNFile, 'rb'),
              sheet_name='Sheet1')
    self.newFSNs = self.newFSNs.sort_values(['Model Name','Color','Size'])

    self.itemsDF['ListFSN'] = self.itemsDF['FSN'].str.split(";")
    existingFSNs = self.itemsDF['ListFSN'].explode().to_list()
    self.newFSNs = self.newFSNs[~self.newFSNs['FSN'].isin(existingFSNs)]

  def updateFSNData(self,longName,fsn):
    index = self.itemsDF.index[self.itemsDF['Long Name']==longName].tolist()
    for i in index:
      self.itemsDF['FSN'].iloc[i] = str(self.itemsDF['FSN'].iloc[i]) + ";" + fsn

  def writeKeywords(self,filename):
    self.itemsDF.to_excel(filename)
