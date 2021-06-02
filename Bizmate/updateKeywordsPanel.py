import wx
import os
import createKeywords
import createSelectFilePanel

class updateKeywordsPanel(wx.Panel):
  def __init__(self, parent): 
    super(updateKeywordsPanel, self).__init__(parent) 

    self.selectKeywordsFile = createSelectFilePanel.createSelectFilePanel(self,'Select Keywords Files',0,0)
    self.selectBusyItemsFile = createSelectFilePanel.createSelectFilePanel(self,'Select Busy Items File',0,100)   

    self.btnRun = wx.Button(self, label='Run', pos=(10, 200))
    self.btnRun.Bind(wx.EVT_BUTTON, self.on_run)

    self.btnStart = wx.Button(self, label='Start/Next', pos=(100, 200))
    self.btnStart.Bind(wx.EVT_BUTTON, self.on_start)

    wx.StaticText(self, label = "Total", pos = (200,200))
    wx.StaticText(self, label = "Done", pos = (400,200))
    self.totalLabel = wx.StaticText(self, label = "", pos = (300,200))
    self.doneLabel = wx.StaticText(self, label = "", pos = (500,200))

    
    wx.StaticText(self,label="Busy Keyword",pos=(10, 265))
    wx.StaticText(self,label="Found in \nHelmet Names",pos=(10, 315))
    wx.StaticText(self,label="New Keyword",pos=(10, 515))

    self.textNewKeywordShort = wx.TextCtrl(self, pos=(150, 250),size=(800,45))
    self.textSearchNames = wx.TextCtrl(self, pos=(150, 300),size=(800,195), style=wx.TE_MULTILINE)
    self.textNewKeyword = wx.TextCtrl(self, pos=(150, 500),size=(800,45))

    self.btnUpdate = wx.Button(self, label='Update', pos=(10, 550))
    self.btnUpdate.Bind(wx.EVT_BUTTON, self.on_update)

    self.btnSkip = wx.Button(self, label='Skip', pos=(100, 550))
    self.btnSkip.Bind(wx.EVT_BUTTON, self.on_skip)

    self.btnSave = wx.Button(self, label='Save', pos=(200, 550))
    self.btnSave.Bind(wx.EVT_BUTTON, self.on_save)

    self.btnConvert = wx.Button(self, label='Convert', pos=(300, 550))
    self.btnConvert.Bind(wx.EVT_BUTTON, self.on_btnConvert)

    self.keywordsObj = createKeywords.createKeywords()
    self.wordIndex = 0

    self.disableUpdate()

  def disableUpdate(self):
    self.btnUpdate.Disable()
    self.btnSkip.Disable()
    self.btnStart.Disable()

  def enableUpdate(self):
    self.btnUpdate.Enable()
    self.btnSkip.Enable()
    self.btnStart.Enable()

  def disableSelect(self):
    self.btnRun.Disable()
    self.selectBusyItemsFile.disable()
    self.selectKeywordsFile.disable()

  def enableSelect(self):
    self.btnRun.Enable()
    self.selectBusyItemsFile.enable()
    self.selectKeywordsFile.enable()

  def on_run(self, event):
    self.keywordsObj.keywords(self.selectKeywordsFile.getFileName(),self.selectBusyItemsFile.getFileName())
    self.totalLabel.SetLabel(str(len(self.keywordsObj.newWords)))
    self.enableUpdate()

  def on_start(self, event):  
    word,names = self.keywordsObj.getFilterNames()
    self.disableSelect()
    self.totalLabel.SetLabel(str(len(self.keywordsObj.newWords)))
    self.doneLabel.SetLabel(str(self.keywordsObj.wordIndex))
    

    if word:
      self.textNewKeywordShort.SetValue(word)
      namesStr = "\n".join(names)
      self.textSearchNames.SetValue(namesStr)
      self.textNewKeyword.SetValue("")
      self.btnUpdate.Enable()
      self.btnSkip.Enable()

    else:
      self.textNewKeyword.SetValue("Done! No New Words")
      self.btnUpdate.Disable()
      self.btnSkip.Disable()
    self.btnStart.Disable()

  def on_update(self,event):
    self.keywordsObj.updateKeyword(self.textNewKeywordShort.GetValue(),self.textNewKeyword.GetValue())
    self.btnStart.Enable()
    self.btnUpdate.Disable()
    self.btnSkip.Disable()

  def on_skip(self,event):
    self.btnStart.Enable()
    self.btnUpdate.Disable()
    self.btnSkip.Disable()
    
  def on_save(self,event):
    self.keywordsObj.writeKeywords(self.selectKeywordsFile.getFileName().replace(".xlsx","New.xlsx"))
    self.enableSelect()

  def on_btnConvert(self,event):
    self.keywordsObj.updateNames(self.selectBusyItemsFile.getFileName(),self.selectKeywordsFile.getFileName().replace(".xlsx","New.xlsx"),self)
