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

class createKeywords():
  def __init__(self):
    self.names = []
    self.newWords = []
    self.updateDict = dict()
    self.keywordsData = []
    self.wordIndex = 0

  def getFilterNames(self):
    if len(self.newWords) == self.wordIndex:
      return None,[]
    word = self.newWords[self.wordIndex]
    self.wordIndex += 1
    modWord = " " + word + " "
    namesFilter = []
    for name in self.names:
      newName = " " + name + " "
      if modWord in newName:
        namesFilter.append(name)
    return word,namesFilter

  def keywords(self,keywordFile,itemFile):
    sheetKeyword = excelReadProcessing.getSheet(keywordFile,0)
    self.keywordsData = excelReadProcessing.getData(sheetKeyword)

    sheetItem = excelReadProcessing.getSheet(itemFile,0)
    itemsData = excelReadProcessing.getData(sheetItem,3)

    setKeyword = set()
    for name in itemsData[0]:
      words = name.split(" ")
      setKeyword.update(words)


    self.newWords = []
    self.wordIndex = 0
    for word in sorted(setKeyword):
      if word not in self.keywordsData[0]:
        self.newWords.append(word)

    
    self.names = itemsData[0]
    self.updateDict = dict()

  def updateKeyword(self,word,newWord):
    self.updateDict[word] = newWord

  def writeKeywords(self,filename):
    writeWorkbook = xlsxwriter.Workbook(filename)
    writeSheet = writeWorkbook.add_worksheet()

    for i,word in enumerate(self.keywordsData[0]):
      self.updateDict[word] = self.keywordsData[1][i]

    for row,key in enumerate(sorted(self.updateDict.keys())):
        writeSheet.write(row,0,key)
        writeSheet.write(row,1,self.updateDict[key])

    writeWorkbook.close()

  def updateNames(self,filename,keywordFile,panel):
    df = excelReadProcessing.getPD(filename)
    sheet = excelReadProcessing.getSheet(keywordFile,0)
    keywordsData = excelReadProcessing.getData(sheet,1)

    keysDict = dict()
    for index,word in enumerate(keywordsData[0]):
      keysDict[word] = keywordsData[1][index]

    progdlg = wx.ProgressDialog('Creating Long Names','Progress',len(df['Name']),parent=panel,style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)
    for i,name in enumerate(df['Name']):
      if not progdlg.Update(i):
        # Cancelled by user.
        break
      if pandas.isnull(name): 
        df['Long Name'].iloc[i] = ""
        continue
      words = name.split(" ")
      newWords = []
      for w in words:
        if w:
          newWords.append(keysDict[w])
      df['Long Name'].iloc[i] = " ".join(newWords)
      
    df.to_excel(filename.replace(".xlsx","New.xlsx"),index=False)
    progdlg.Destroy()