import wx
import os
import createSelectFilePanel
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import addGlobalSearchPanelTextBox
import updatePhoto
import wx.lib.scrolledpanel as scrolled


class mergePhotoPanel(scrolled.ScrolledPanel):
  def __init__(self, parent): 
    super(mergePhotoPanel, self).__init__(parent) 
    self.SetupScrolling()

    self.selectDatabaseFile = createSelectFilePanel.createSelectFilePanel(self,'Select Database',0,0)
    self.selectFSNNewFile = createSelectFilePanel.createSelectFilePanel(self,'Select New Photo File',0,100)   

    self.btnRun = wx.Button(self, label='Run', pos=(10, 200))
    self.btnRun.Bind(wx.EVT_BUTTON, self.on_run)

    self.btnStart = wx.Button(self, label='Start/Next', pos=(100, 200))
    self.btnStart.Bind(wx.EVT_BUTTON, self.on_start)

    wx.StaticText(self, label = "Total", pos = (200,200))
    wx.StaticText(self, label = "Done", pos = (400,200))
    self.totalLabel = wx.StaticText(self, label = "", pos = (300,200))
    self.doneLabel = wx.StaticText(self, label = "", pos = (500,200))

    wx.StaticText(self,label="Details",pos=(10, 250))
  
    self.textFSNDetails = wx.TextCtrl(self, pos=(150, 300),size=(800,195), style=wx.TE_MULTILINE)

    font1 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
    self.textFSNDetails.SetFont(font1)

    self.globalSearchItems = addGlobalSearchPanelTextBox.addGlobalSearchPanelTextBox(self,x=10,y=500)  
    self.cbNone = wx.CheckBox(self, label = 'None',pos = (800,self.globalSearchItems.endY-50))
    self.btnUpdate = wx.Button(self, label='Update', pos=(10, self.globalSearchItems.endY))
    self.btnUpdate.Bind(wx.EVT_BUTTON, self.on_update)

    self.btnSave = wx.Button(self, label='Save', pos=(100, self.globalSearchItems.endY))
    self.btnSave.Bind(wx.EVT_BUTTON, self.on_save)

    self.photoObj = updatePhoto.updatePhoto()
    self.wordIndex = 0

    self.disableUpdate()

  def disableUpdate(self):
    self.btnUpdate.Disable()
    self.btnStart.Disable()

  def enableUpdate(self):
    self.btnUpdate.Enable()
    self.btnStart.Enable()

  def disableSelect(self):
    self.btnRun.Disable()
    self.selectDatabaseFile.disable()
    self.selectFSNNewFile.disable()

  def enableSelect(self):
    self.btnRun.Enable()
    self.selectDatabaseFile.enable()
    self.selectFSNNewFile.enable()

  def on_run(self, event):
    self.photoObj.createDatabase(self.selectFSNNewFile.getFileName(),self.selectDatabaseFile.getFileName())
    self.globalSearchItems.setDatabase(self.photoObj.names)
    self.totalLabel.SetLabel(str(len(self.photoObj.dfNew[self.photoObj.dfNew.columns[0]])))
    self.enableUpdate()

  def on_start(self, event):  
    data = self.photoObj.nextData()
    self.disableSelect()
    self.totalLabel.SetLabel(str(len(self.photoObj.dfNew[self.photoObj.dfNew.columns[0]])))
    self.doneLabel.SetLabel(str(self.photoObj.wordIndex))

    if data:
      self.textFSNDetails.SetValue("\n".join(data))
      self.btnUpdate.Enable()
      
    else:
      self.globalSearchItems.labelSelected.SetLabel("Done! No New Words")
      self.btnUpdate.Disable()

  def on_update(self,event):
    if not self.cbNone.GetValue():
      self.photoObj.updatePhotoData(self.globalSearchItems.labelSelected.GetLabel(), self.textFSNDetails.GetValue())
    else:
      self.photoObj.updatePhotoData("None", self.textFSNDetails.GetValue())
    self.btnUpdate.Disable()
    self.cbNone.SetValue(False)
    
  def on_save(self,event):
    self.photoObj.writeKeywords(self.selectDatabaseFile.getFileName().replace(".xlsx","New.xlsx"))
    self.enableSelect()
