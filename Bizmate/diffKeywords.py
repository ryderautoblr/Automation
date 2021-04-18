import xlUtils
import xlsxwriter
import os

class diffKeywords():
  def __init__(self):
    self.newKeywords = []
    self.wordIndicies = []
    self.wordIndex = 0

  def getNewWords(self):
    if len(self.wordIndicies) == self.wordIndex:
      return None,0

    index = self.wordIndicies[self.wordIndex]
    data = ""
    data += self.newKeywords[0][index-1] + "," + self.newKeywords[1][index-1] + "\n"
    data += self.newKeywords[0][index] + "," + self.newKeywords[1][index] + "\n"
    data += self.newKeywords[0][index+1] + "," + self.newKeywords[1][index+1]

    self.wordIndex += 1
    return data,index

  def getKeywords(self,newKeywordFile,oldKeywordFile):
    self.wordIndex = 0
    self.wordIndicies = []

    xlObj = xlUtils.xlUtils()
    sheetKeywordOld = xlObj.getSheet(oldKeywordFile,0)
    oldKeywords = xlObj.getData(0,sheetKeywordOld)

    sheetKeywordNew = xlObj.getSheet(newKeywordFile,0)
    self.newKeywords = xlObj.getData(0,sheetKeywordNew)

    offset = 0
    for i in range(len(self.newKeywords[0])):
      if oldKeywords[0][i-offset] != self.newKeywords[0][i]:
        self.wordIndicies.append(i)
        offset += 1

  def updateKeyword(self,index,word):
    self.newKeywords[1][index] = word

  def writeKeywords(self,filename):
    writeWorkbook = xlsxwriter.Workbook(filename)
    writeSheet = writeWorkbook.add_worksheet()

    for i,word in enumerate(self.newKeywords[0]):
      writeSheet.write(i,0,word)
      writeSheet.write(i,1,self.newKeywords[1][i])

    writeWorkbook.close()
