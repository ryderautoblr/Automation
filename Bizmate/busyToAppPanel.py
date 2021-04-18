import wx
import os
import createSelectFilePanel
import xlUtils


class busyToAppPanel(wx.Panel):
  def __init__(self, parent): 
    super(busyToAppPanel, self).__init__(parent) 

    self.selectBusyList = createSelectFilePanel.createSelectFilePanel(self,'Select Busy Items Files',0,0)
    self.selectAppList = createSelectFilePanel.createSelectFilePanel(self,'Select App Items Files',0,100)   
    self.selectAppSample = createSelectFilePanel.createSelectFilePanel(self,'Select App Sample Files',0,200)   
    self.selectKeywords = createSelectFilePanel.createSelectFilePanel(self,'Select Keywords Files',0,300)   

    self.btnCheckCategories = wx.Button(self, label='Check Categories', pos=(10, 400))
    self.btnCheckCategories.Bind(wx.EVT_BUTTON, self.on_check_categories)

    self.btnUpdateAppFiles = wx.Button(self, label='Update App Files', pos=(200, 400))
    self.btnUpdateAppFiles.Bind(wx.EVT_BUTTON, self.on_update_app)
    self.btnUpdateAppFiles.Disable()

    self.textLog = wx.TextCtrl(self, pos=(10, 450),size=(800,200), style=wx.TE_MULTILINE)
    self.busyData = []

  def on_check_categories(self,event):
    xlObj = xlUtils.xlUtils()
    
    busyCategoryCol = ord('C') - ord('A')
    busyFileLoc = self.selectBusyList.getFileName()
    busySheet = xlObj.getSheet(busyFileLoc,0)
    self.busyData = xlObj.getData(7,busySheet)
    busyCategorySet = set()

    for data in self.busyData[busyCategoryCol]:
      if data.strip():
        busyCategorySet.add(data)

    appCategoryCol = ord('B') - ord('A')
    appListFileLoc = self.selectAppList.getFileName()
    appCategorySheet = xlObj.getSheet(appListFileLoc,1)
    appCategoryData = xlObj.getData(1,appCategorySheet)
    
    missingCategories = []
    for data in sorted(busyCategorySet):
      if data not in appCategoryData[appCategoryCol]:
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
    x = 1


