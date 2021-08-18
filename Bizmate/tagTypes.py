import xlUtils
import xlsxwriter
import os
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import excelReadProcessing
import math
import pandas
import wx
import numpy

dict1 = {"helmet":"Helmets","gloves":"Gloves","covid-19":"Covid-19","lock":"Fittings & Spares","visor":"Visor",
        "fitting":"Fittings & Spares","o/f helmet":"Open Face Helmets",
          }
def mapDict(x,outputDict):
  if pandas.isnull(x.iloc[2]): x.iloc[2] = ""
  for val in dict1.keys():
    if (not pandas.isnull(x.iloc[1])) and val in x.iloc[1].lower():
      return x.iloc[2] + " " + dict1[val] 
  if pandas.isnull(x.iloc[0]):return numpy.NaN
  return x.iloc[2] + " " + outputDict[x.iloc[0]]

class tagTypes():
  def __init__(self):
    self.names = []
    self.newWords = []
    self.typeDf = []
    self.wordIndex = 0

  def getFilterNames(self):
    if len(self.newWords) == self.wordIndex:
      return None,[]
    word = ''
    while not word:
      self.wordIndex += 1
      if len(self.newWords) == self.wordIndex:
        return None
      word = self.newWords[self.wordIndex] 
    return word

  def keywords(self,typeFile,itemFile):
    self.typeDf = excelReadProcessing.getPD(typeFile)

    self.itemsDF = excelReadProcessing.getPD(itemFile)

    setKeyword = set()
    tag = 'Item Type'
    if tag not in self.itemsDF.columns: self.itemsDF[tag] = ""

    for name in self.itemsDF['Type'].to_list():
      if pandas.isnull(name):continue
      setKeyword.add(name)

    self.newWords = []
    self.wordIndex = -1
    for word in sorted(setKeyword):
      if word not in self.typeDf['Word'].values:
        self.newWords.append(word)

  def updateKeyword(self,word,output):
    df = {'Word':word,'Item Type':output}
    self.typeDf = self.typeDf.append(df,ignore_index=True)

  def writeKeywords(self,filename):
    self.typeDf = self.typeDf.sort_values(by = 'Word')
    self.typeDf.to_excel(filename,index=False)

  def updateNames(self,filename,outputFile):
    dfNames = excelReadProcessing.getPD(filename)
    outputDict = dict()
    for i in range(len(self.typeDf[self.typeDf.columns[0]].to_list())):
      outputDict[self.typeDf[self.typeDf.columns[0]].iloc[i]] = self.typeDf[self.typeDf.columns[1]].iloc[i]

    self.itemsDF['Item Type'] = self.itemsDF[['Type','Parent Group','Brand']].apply(lambda x: mapDict(x,outputDict),axis=1)
    self.itemsDF.to_excel(outputFile.replace(".xlsx","New.xlsx"),index=False)