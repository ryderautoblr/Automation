import wx
import os
import createSelectFilePanel
import pandas
import wx.lib.scrolledpanel as scrolled
import numpy
import re


def getNameWithoutSize(name):
  words = name.split(" ")
  if ("(" in words[-1]) and (")" in words[-1]):
    return " ".join(words[:-1]) 
  return name

def concat(row):
  row = row.astype(str)
  data = ";".join(row)
  values = data.split(";")
  finalValues = []
  for v in values:
    if "nan" != v:
      v = v.strip()
      if v not in finalValues:
        if v:
          finalValues.append(v)

  finalValues = sorted(finalValues, key=len)

  return ";".join(finalValues)

def concatNan(row):
  row = row.replace(numpy.NaN,"")
  data = []
  for val in row:
    if val: data.append(val)

  if len(data) and data[0].replace(".","").replace(",","").isdigit():
    vals = []
    for x in data:
      if x:
        vals.append(float(x.replace(",","")))
    data = max(vals)
    return data
  return ";".join(data)

def getIds(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    if val.replace(".","").isdigit() and (len(val) != 13):
      ids.append(val)
  return ids

def getMRP(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    val2 = re.findall(r'\d+[\.|,]\d+', val)
    if (val2) and (val2 not in ids):
      ids.append(val2[0])
    if not(val2) and x:
      val2 = re.findall(r'\d+', val)
      if (val2) and (val2 not in ids):
        ids.append(val2[0])
  return ids  


def getSize(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    val = val.replace("(","").replace(")","").strip()
    if val and (val not in ids):
      ids.append(val)
  return ids

def getImage(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    if val and ("http" not in val):
      val = "https://drive.google.com/file/d/{{LINK}}/view".replace("{{LINK}}",val)
    if val and (val not in ids):
      ids.append(val)
  return ids

def getCategory(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    if val and (val not in ids):
      ids.append(val)
  return ids

def getEAN(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    if val.replace(".","").isdigit() and (len(val) == 13):
      ids.append(val)
  return ids

def getFSN(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    if (not val.replace(".","").isdigit()) and len(val.split(" "))==1 and len(val)>12:
      ids.append(val)
  return ids

def getASIN(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    if (not val.replace(".","").isdigit()) and len(val.split(" "))==1 and len(val)<=12 and (not val.startswith("LS2")):
      ids.append(val)
  return ids

def getAlias(x):
  vals = x.split(";")
  ids = []
  for val in vals:
    if len(val.split(" "))>1:
      ids.append(val)
  return ids

def getParamLen(x,func):
  return len(func(x)) 

def getParamTillLen(x,maxLen,func):
  vals = func(x)
  for i in range(len(vals),maxLen):
    vals.append("")
  if len(vals) != maxLen: print ("error")
  return vals

def splitDfCol(df,tag,tagNew,func):
    df[tagNew] = df[tag].apply(lambda x: getParamLen(x,func))  
    maxTag = df[tagNew].max()
    cols = [tagNew.replace("Len","") + str(i) for i in range(maxTag)]
    tempDF = df[tag].apply(getParamTillLen,args=(maxTag,func,))
    df[cols] = pandas.DataFrame(tempDF.tolist())
    # print (df[cols[0]].to_list())
    # print(maxTag)
    return df

class busyToAppPanel(scrolled.ScrolledPanel):
  def __init__(self, parent): 
    super(busyToAppPanel, self).__init__(parent) 
    self.SetupScrolling()

    self.selectBusyList = createSelectFilePanel.createSelectFilePanel(self,'Select Busy Items Files',0,0)
    self.selectAppList = createSelectFilePanel.createSelectFilePanel(self,'Select App Items Files',0,100)   
    
    self.btnCheckCategories = wx.Button(self, label='Check Categories', pos=(10, 200))
    self.btnCheckCategories.Bind(wx.EVT_BUTTON, self.on_check_categories)

    self.btnUpdateCols = wx.Button(self, label='Update Columns', pos=(200, 200))
    self.btnUpdateCols.Bind(wx.EVT_BUTTON, self.on_update_cols)
    self.btnUpdateCols.Disable()

    self.btnUpdateAppFiles = wx.Button(self, label='Update App Files', pos=(400, 200))
    self.btnUpdateAppFiles.Bind(wx.EVT_BUTTON, self.on_update_app)
    self.btnUpdateAppFiles.Disable()

    self.btnUpdateBizmateFiles = wx.Button(self, label='Create Bizmate Data', pos=(600, 200))
    self.btnUpdateBizmateFiles.Bind(wx.EVT_BUTTON, self.on_update_bizmate)
    self.btnUpdateBizmateFiles.Disable()

    self.textLog = wx.TextCtrl(self, pos=(10, 250),size=(800,200), style=wx.TE_MULTILINE)
    self.busyData = []

  def on_check_categories(self,event):
    busyFileLoc = self.selectBusyList.getFileName()
    self.busyDf = pandas.read_excel(busyFileLoc)
    busyCategorySet = set()

    for data in self.busyDf["Parent Group"]:
      if pandas.isnull(data): continue
      if data.strip():
        busyCategorySet.add(data)

    appListFileLoc = self.selectAppList.getFileName()
    self.appDf = pandas.read_excel(appListFileLoc,None)
    appCategoryData = self.appDf["Category Details"]["Category"].to_list()
    
    missingCategories = []
    for data in sorted(busyCategorySet):
      if data not in appCategoryData:
        missingCategories.append(data)

    logDetails = ""
    if len(missingCategories):
      logDetails += "Missing Categories\n\n"
      missingStr = "\n".join(missingCategories)
      logDetails += missingStr
    else:
      logDetails += "All Categories Are Present! You may continue!"
      self.btnUpdateCols.Enable()

    self.textLog.SetValue(logDetails)

  def on_update_cols(self,event):
    self.appProductsDf = self.appDf["Product Details"].copy()
    self.appProductsDf["Long Name"] = self.appProductsDf["Product Name"]
    self.newDf = pandas.merge(self.busyDf,self.appProductsDf,on=["Long Name"],how="outer")

    ########################
    #Update Col Mappings
    #########################
    name = "ColumnMappings.xlsx"
    self.colMapDf = pandas.read_excel(name)
    self.tempDf = pandas.DataFrame(columns = self.newDf.columns)
    self.newCols = pandas.concat([self.tempDf,self.colMapDf])

    self.newCols.to_excel(name,index=False)
    self.btnUpdateAppFiles.Enable()

  def on_update_app(self,event):
    tagSet = set()
    tagDict = dict()
    for col in self.colMapDf.columns:
      for val in self.colMapDf[col].to_list():
        if not pandas.isnull(val): 
          if val not in tagDict.keys():
            tagDict[val] = []
          tagDict[val].append(col)
        
    self.finalDf = pandas.DataFrame(columns=list(tagDict.keys()))
    for c in self.finalDf.columns:
      self.finalDf[c] = self.newDf[tagDict[c]].apply(lambda x: concat(x),axis=1)

    idx = self.finalDf.index[self.finalDf["Long Name"] == "None"].to_list()
    for i in idx:
      self.finalDf.drop(index=i,inplace=True)

    self.finalDf.replace(numpy.NaN,"",inplace=True)
    self.finalDf = splitDfCol(self.finalDf,"Alias","AliasIdsLen",getIds)
    self.finalDf = splitDfCol(self.finalDf,"Alias","EANLen",getEAN)
    self.finalDf = splitDfCol(self.finalDf,"Alias","FSNLen",getFSN)
    self.finalDf = splitDfCol(self.finalDf,"Alias","ASINLen",getASIN)
    self.finalDf = splitDfCol(self.finalDf,"Alias","AliasNames",getAlias)
    self.finalDf = splitDfCol(self.finalDf,"Size","SizeLen",getSize)
    self.finalDf = splitDfCol(self.finalDf,"Category","CategoryLen",getCategory)
    self.finalDf = splitDfCol(self.finalDf,"MRP","MRPLen",getMRP)
    self.finalDf = splitDfCol(self.finalDf,"SP","SPLen",getMRP)
    self.finalDf = splitDfCol(self.finalDf,"PP","PPLen",getMRP)
    self.finalDf = splitDfCol(self.finalDf,"Brand","BrandLen",getCategory)
    self.finalDf = splitDfCol(self.finalDf,"Style","StyleLen",getCategory)
    self.finalDf = splitDfCol(self.finalDf,"Colour","ColourLen",getCategory)
    self.finalDf = splitDfCol(self.finalDf,"Type","TypeLen",getCategory)
    self.finalDf = splitDfCol(self.finalDf,"GST","GSTLen",getMRP)
    self.finalDf = splitDfCol(self.finalDf,"Link","LinkLen",getCategory)
    
    self.finalDf["Long Name Without Size"] = self.finalDf["Long Name"].apply(getNameWithoutSize)

    for i in range(len(self.finalDf["Long Name Without Size"])-1):
      index = self.finalDf.index[self.finalDf["Long Name Without Size"] == self.finalDf["Long Name Without Size"].iloc[i]].to_list()
      targetIndex = -1
      for val in index:
        if self.finalDf["Image"].iloc[val] and (not pandas.isnull(self.finalDf["Image"].iloc[val])):
          targetIndex = val
      if targetIndex != -1:
        # print (targetIndex)
        for val in index:
          self.finalDf["Image"].iloc[val] = self.finalDf["Image"].iloc[targetIndex]


    self.finalDf = splitDfCol(self.finalDf,"Image","ImageLen",getImage)

    
    name = "Consolidated.xlsx"
    self.finalDf.to_excel(name,index=False)

    self.name2 = "ColMappingFromBizmateToConsolidated.xlsx"
    self.colMapBiztoConDf = pandas.read_excel(self.name2)

    appCols = self.appDf["Product Details"].columns.to_list()
    
    conCols = self.colMapBiztoConDf.columns.to_list()
    for col in appCols:
      if col not in conCols:
        self.colMapBiztoConDf[col] = ""

    conCols = self.colMapBiztoConDf.columns.to_list()
    dropCols = []
    for col in conCols:
      if col not in appCols:
        dropCols.append(col)
    self.colMapBiztoConDf.drop(dropCols,inplace=True,axis=1)

    self.colMapBiztoConDf.to_excel(self.name2,index=False)
    self.btnUpdateBizmateFiles.Enable()

  def on_update_bizmate(self,event):
    self.colMapBiztoConDf = pandas.read_excel(self.name2)

    self.bizmateDF = self.appDf["Product Details"]
    for col in self.colMapBiztoConDf.columns.to_list():
      if self.colMapBiztoConDf[col].iloc[0] == "TODO":
        continue
      if "All" in self.colMapBiztoConDf[col].iloc[0]:
        tag = self.colMapBiztoConDf[col].iloc[0].replace("All","")
        i = 1
        if "Image" not in tag: i = 0
        tagTemp = tag + str(i)

        cols = []
        while tagTemp in self.finalDf.columns:
          cols.append(tagTemp)
          i += 1
          tagTemp = tag + str(i)
        print (cols)
        self.bizmateDF[col] = self.finalDf[cols].apply(lambda x: concatNan(x),axis=1)
        continue

      self.bizmateDF[col] = self.finalDf[self.colMapBiztoConDf[col].iloc[0]]

    self.appDf["Product Details"].to_excel(self.selectAppList.getFileName().replace(".xls","New.xlsx"),index=False)
    

      