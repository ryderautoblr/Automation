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


class tagKeywords():
  def __init__(self):
    self.names = []
    self.newWords = []
    self.keywordsDF = []
    self.wordIndex = 0

  def getFilterNames(self):
    if len(self.newWords) == self.wordIndex:
      return None,[]
    word = ''
    while not word:
      self.wordIndex += 1
      if len(self.newWords) == self.wordIndex:
        return None,[]
      word = self.newWords[self.wordIndex] 
    modWord = " " + word + " "
    namesFilter = []
    for name in self.names:
      if pandas.isnull(name): continue
      newName = " " + name + " "
      if modWord in newName:
        namesFilter.append(name)
    return word,namesFilter

  def keywords(self,keywordFile,itemFile):
    self.keywordsDF = excelReadProcessing.getPD(keywordFile)

    itemsDF = excelReadProcessing.getPD(itemFile)

    setKeyword = set()
    for name in itemsDF['Long Name']:
      if pandas.isnull(name):continue
      words = name.split(" ")
      setKeyword.update(words)

    self.newWords = []
    self.wordIndex = 0
    for word in sorted(setKeyword):
      if word not in self.keywordsDF['Word'].values:
        self.newWords.append(word)

    print (len(self.newWords))
    self.names = itemsDF['Long Name']
    
  def updateKeyword(self,word,isBrand,isStyle,isColour,isSize,isType):
    df = {'Word':word,'Brand':isBrand,'Style':isStyle,'Colour':isColour,'Size':isSize,'Type':isType}
    self.keywordsDF = self.keywordsDF.append(df,ignore_index=True)

  def writeKeywords(self,filename):
    self.keywordsDF = self.keywordsDF.sort_values(by = 'Word')
    self.keywordsDF.to_excel(filename,index=False)

  def updateNames(self,filename,panel):
    dfNames = excelReadProcessing.getPD(filename)
    count = 0

    keysDict = self.keywordsDF.set_index('Word').T.to_dict('list')
    
    headers = ['Brand','Style','Colour','Size','Type']
    newDF = pandas.DataFrame(columns=headers)

    total = len(dfNames['Long Name'])

    progdlg = wx.ProgressDialog('Creating Tags','Progress',total,parent=panel,style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)
    for i,name in enumerate(dfNames['Long Name']):
      if not progdlg.Update(i):
        # Cancelled by user.
        break
    
      df = dict() 
      for h in headers:
        df[h] = []
      if not pandas.isnull(name): 
        words = name.split(" ")
        for w in words:
          if w:
            for i,tag in enumerate(keysDict[w]):
              if tag:
                df[headers[i]].append(w)

      for h in headers:
        df[h] = " ".join(df[h])
      newDF = newDF.append(df,ignore_index=True)
    

    for h in headers:
      if h == 'Size':dfNames['NewSize'] = newDF[h]
      else: dfNames[h] = newDF[h]
    dfNames["Item Code"] = dfNames[['Brand','Style']].apply(lambda x: " ".join(x),axis=1)
    dfNames.to_excel(filename.replace(".xlsx","New.xlsx"),index=False)
    progdlg.Destroy()
    