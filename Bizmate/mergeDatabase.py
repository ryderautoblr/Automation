import os
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import math
import pandas
import wx

def removeBusyHeader(df):
  header = "Name"
  count = 0

  while True:
    if df[df.columns[0]].iloc[count] == header:
      break
    count += 1

  df.columns = df.iloc[count]
  df = df[count+1:]
  return df    

def getUniqueFSN(str1):
  listFSNs = list(set(str(str1).replace("'",";").replace("'",";").split(";")))
  finalFSNs = []
  for fsn in listFSNs:
    if fsn.startswith("HLM"):
      finalFSNs.append(fsn)
  return ";".join(finalFSNs)

def getUniqueFSNList(str1):
  listFSNs = list(set(str(str1).replace("[",";").replace("]",";").replace(",",";").replace("'",";").replace("'",";").split(";")))
  finalFSNs = []
  for fsn in listFSNs:
    if fsn.startswith("HLM"):
      finalFSNs.append(fsn)
  return finalFSNs
  
def mergeDatabase(busyFile,fullFile):
  busyFileDF = pandas.read_excel(busyFile)
  busyFileDF = removeBusyHeader(busyFileDF)
  busyFileDF = busyFileDF[busyFileDF["Name"].notnull()]
  fullFileDF = pandas.read_excel(fullFile)
  newDF = pandas.merge(busyFileDF,fullFileDF,how="outer",on="Name")
  cols = newDF.columns
  dropCols = []
  reNameCols = []
  for c in cols:
    if c.endswith("_y"): dropCols.append(c)
    else: reNameCols.append(c.replace("_x",""))
  
      
  newDF = newDF.drop(dropCols,axis=1)
  
  newDF.columns = reNameCols
  newDF["Alias Add1"] = newDF["Alias Add1"].fillna('')
  newDF["Alias Add2"] = newDF["Alias Add2"].fillna('')
  newDF["Alias Add3"] = newDF["Alias Add3"].fillna('')
  newDF['FSN'] = newDF['FSN'].map(str) + ";" + newDF["Alias"].map(str) + ";"  + newDF["Alias Add1"].map(str) + ";"   + newDF["Alias Add2"].map(str) + ";"  + newDF["Alias Add3"]
  newDF['FSN'] = newDF['FSN'].apply(getUniqueFSN)
  newDF['ListFSN'] = newDF['ListFSN'].map(str) + ";" + newDF['FSN'].map(str)
  newDF['ListFSN'] = newDF['ListFSN'].apply(getUniqueFSNList)
  
  newDF.to_excel(fullFile.replace(".xlsx","New.xlsx"),index=False)
