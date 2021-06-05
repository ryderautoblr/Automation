import wx
import os
import createSelectFilePanel
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import addGlobalSearchPanelTextBox
import updateFSN

class updateFSNPanel(wx.Panel):
  def __init__(self, parent): 
    super(updateFSNPanel, self).__init__(parent) 

    self.selectDatabaseFile = createSelectFilePanel.createSelectFilePanel(self,'Select Database',0,0)
    self.selectFSNNewFile = createSelectFilePanel.createSelectFilePanel(self,'Select New FSN File',0,100)   

    self.btnRun = wx.Button(self, label='Run', pos=(10, 200))
    self.btnRun.Bind(wx.EVT_BUTTON, self.on_run)

    self.btnStart = wx.Button(self, label='Start/Next', pos=(100, 200))
    self.btnStart.Bind(wx.EVT_BUTTON, self.on_start)

    wx.StaticText(self, label = "Total", pos = (200,200))
    wx.StaticText(self, label = "Done", pos = (400,200))
    self.totalLabel = wx.StaticText(self, label = "", pos = (300,200))
    self.doneLabel = wx.StaticText(self, label = "", pos = (500,200))

    wx.StaticText(self,label="FSN",pos=(10, 265))
    wx.StaticText(self,label="FSN Details",pos=(10, 300))
  
    self.textNewFSN = wx.TextCtrl(self, pos=(150, 250),size=(800,45))
    self.textFSNDetails = wx.TextCtrl(self, pos=(150, 300),size=(800,195), style=wx.TE_MULTILINE)

    font1 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
    self.textNewFSN.SetFont(font1)
    self.textFSNDetails.SetFont(font1)

    self.globalSearchItems = addGlobalSearchPanelTextBox.addGlobalSearchPanelTextBox(self,x=10,y=500)  
    self.cbNone = wx.CheckBox(self, label = 'None',pos = (800,self.globalSearchItems.endY-50))
    self.btnUpdate = wx.Button(self, label='Update', pos=(10, self.globalSearchItems.endY))
    self.btnUpdate.Bind(wx.EVT_BUTTON, self.on_update)

    self.btnSave = wx.Button(self, label='Save', pos=(100, self.globalSearchItems.endY))
    self.btnSave.Bind(wx.EVT_BUTTON, self.on_save)

    self.updateFSNObj = updateFSN.updateFSN()
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
    self.updateFSNObj.createFSNDatabase(self.selectFSNNewFile.getFileName(),self.selectDatabaseFile.getFileName())
    self.globalSearchItems.setDatabase(self.updateFSNObj.names)
    self.totalLabel.SetLabel(str(len(self.updateFSNObj.newFSNs['FSN'])))
    self.enableUpdate()

  def on_start(self, event):  
    fsn,data = self.updateFSNObj.nextFSN()
    self.disableSelect()
    self.totalLabel.SetLabel(str(len(self.updateFSNObj.newFSNs['FSN'])))
    self.doneLabel.SetLabel(str(self.updateFSNObj.wordIndex))

    if fsn:
      self.textNewFSN.SetValue(fsn)
      self.textFSNDetails.SetValue("\n".join(data))
      self.btnUpdate.Enable()
      
    else:
      self.globalSearchItems.labelSelected.SetLabel("Done! No New Words")
      self.btnUpdate.Disable()

  def on_update(self,event):
    if not self.cbNone.GetValue():
      self.updateFSNObj.updateFSNData(self.globalSearchItems.labelSelected.GetLabel(), self.textNewFSN.GetValue())
    else:
      self.updateFSNObj.updateFSNData("None", self.textNewFSN.GetValue())
    self.btnUpdate.Disable()
    self.cbNone.SetValue(False)
    
  def on_save(self,event):
    self.updateFSNObj.writeKeywords(self.selectDatabaseFile.getFileName().replace(".xlsx","New.xlsx"))
    self.enableSelect()
