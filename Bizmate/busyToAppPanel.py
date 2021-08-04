import wx
import os
import createSelectFilePanel
import pandas
import wx.lib.scrolledpanel as scrolled

class busyToAppPanel(scrolled.ScrolledPanel):
  def __init__(self, parent): 
    super(busyToAppPanel, self).__init__(parent) 
    self.SetupScrolling()

    self.selectBusyList = createSelectFilePanel.createSelectFilePanel(self,'Select Busy Items Files',0,0)
    self.selectAppList = createSelectFilePanel.createSelectFilePanel(self,'Select App Items Files',0,100)   
    
    self.btnCheckCategories = wx.Button(self, label='Check Categories', pos=(10, 200))
    self.btnCheckCategories.Bind(wx.EVT_BUTTON, self.on_check_categories)

    self.btnUpdateAppFiles = wx.Button(self, label='Update App Files', pos=(200, 200))
    self.btnUpdateAppFiles.Bind(wx.EVT_BUTTON, self.on_update_app)
    self.btnUpdateAppFiles.Disable()

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

    appCategoryCol = ord('B') - ord('A')
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
      self.btnUpdateAppFiles.Enable()

    self.textLog.SetValue(logDetails)

  def on_update_app(self,event):
    self.appProductsDf = self.appDf["Product Details"]
    self.appProductsDf["Long Name"] = self.appProductsDf["Product Name"]
    self.newDf = pandas.merge(self.busyDf,self.appProductsDf,on=["Long Name"],how="outer")
    print (self.newDf,self.busyDf,self.appProductsDf)



