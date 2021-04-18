import wx
import os
import diffKeywords
import createSelectFilePanel

class diffKeywordsPanel(wx.Panel):
  def __init__(self, parent): 
    super(diffKeywordsPanel, self).__init__(parent) 

    self.selectKeywordsFileNew = createSelectFilePanel.createSelectFilePanel(self,'Select New Keywords Files',0,0)
    self.selectKeywordsFileOld = createSelectFilePanel.createSelectFilePanel(self,'Select Old Keywords Files',0,100)   

    self.btnRun = wx.Button(self, label='Run', pos=(10, 200))
    self.btnRun.Bind(wx.EVT_BUTTON, self.on_run)

    self.btnStart = wx.Button(self, label='Start/Next', pos=(100, 200))
    self.btnStart.Bind(wx.EVT_BUTTON, self.on_start)

    
    wx.StaticText(self,label="Old Keyword",pos=(10, 265))
    wx.StaticText(self,label="New Keyword",pos=(10, 515))

    self.textOldKeyword = wx.TextCtrl(self, pos=(150, 250),size=(800,200), style=wx.TE_MULTILINE)
    self.textNewKeyword = wx.TextCtrl(self, pos=(150, 500),size=(800,45))

    self.btnUpdate = wx.Button(self, label='Update', pos=(10, 550))
    self.btnUpdate.Bind(wx.EVT_BUTTON, self.on_update)

    self.btnSave = wx.Button(self, label='Save', pos=(100, 550))
    self.btnSave.Bind(wx.EVT_BUTTON, self.on_save)

    self.keywordsObj = diffKeywords.diffKeywords()
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
    self.selectKeywordsFileOld.disable()
    self.selectKeywordsFileNew.disable()

  def enableSelect(self):
    self.btnRun.Enable()
    self.selectKeywordsFileOld.enable()
    self.selectKeywordsFileNew.enable()

  def on_run(self, event):
    self.keywordsObj.getKeywords(self.selectKeywordsFileNew.getFileName(),self.selectKeywordsFileOld.getFileName())
    self.enableUpdate()

  def on_start(self, event):  
    data,index = self.keywordsObj.getNewWords()
    self.disableSelect()

    if data:
      self.wordIndex = index
      self.textOldKeyword.SetValue(data)
      self.textNewKeyword.SetValue("")
      self.btnUpdate.Enable()

    else:
      self.textNewKeyword.SetValue("Done! No New Words")
      self.btnUpdate.Disable()

  def on_update(self,event):
    self.keywordsObj.updateKeyword(self.wordIndex, self.textNewKeyword.GetValue())
    self.btnUpdate.Disable()
    
  def on_save(self,event):
    self.keywordsObj.writeKeywords(self.selectKeywordsFileNew.getFileName().replace(".xlsx","New.xlsx"))
    self.enableSelect()
