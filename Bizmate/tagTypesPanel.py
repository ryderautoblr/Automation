import wx
import os
import tagTypes
import createSelectFilePanel
import wx.lib.scrolledpanel as scrolled

class tagTypesPanel(scrolled.ScrolledPanel):
  def __init__(self, parent): 
    super(tagTypesPanel, self).__init__(parent) 
    self.SetupScrolling()

    self.selectKeywordsFile = createSelectFilePanel.createSelectFilePanel(self,'Select Type Files',0,0)
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
    
    self.textNewKeywordShort = wx.TextCtrl(self, pos=(150, 250),size=(800,45))
    self.textSearchNames = wx.TextCtrl(self, pos=(150, 300),size=(800,195), style=wx.TE_MULTILINE)
    self.cb1 = wx.CheckBox(self, label = 'Helmets',pos = (10,510))
    self.cb2 = wx.CheckBox(self, label = 'Visors',pos = (100,510))
    self.cb3 = wx.CheckBox(self, label = 'Fittings & Spares',pos = (200,510))
    self.cb4 = wx.CheckBox(self, label = 'Adventure Riding Gears',pos = (400,510))
    self.cb5 = wx.CheckBox(self, label = 'Gloves',pos = (600,510))
    self.cb6 = wx.CheckBox(self, label = 'Motorcycle Accessories',pos = (700,510))

    self.cbs = [self.cb1,self.cb2,self.cb3,self.cb4,self.cb5,self.cb6]
    
    self.btnUpdate = wx.Button(self, label='Update', pos=(10, 550))
    self.btnUpdate.Bind(wx.EVT_BUTTON, self.on_update)

    self.btnSkip = wx.Button(self, label='Skip', pos=(100, 550))
    self.btnSkip.Bind(wx.EVT_BUTTON, self.on_skip)

    self.btnSave = wx.Button(self, label='Save', pos=(200, 550))
    self.btnSave.Bind(wx.EVT_BUTTON, self.on_save)

    self.btnConvert = wx.Button(self, label='Convert', pos=(300, 550))
    self.btnConvert.Bind(wx.EVT_BUTTON, self.on_btnConvert)

    self.keywordsObj = tagTypes.tagTypes()
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
    word = self.keywordsObj.getFilterNames()
    self.disableSelect()
    self.totalLabel.SetLabel(str(len(self.keywordsObj.newWords)))
    self.doneLabel.SetLabel(str(self.keywordsObj.wordIndex))
    

    if word:
      self.textNewKeywordShort.SetValue(word)
      self.btnUpdate.Enable()
      self.btnSkip.Enable()
      for cb in self.cbs:
        cb.SetValue(False)

    else:
      self.textNewKeywordShort.SetValue("Done! No New Words")
      self.btnUpdate.Disable()
      self.btnSkip.Disable()
    self.btnStart.Disable()

  def on_update(self,event):
    selectedWord = ''
    for cb in self.cbs:
      if cb.GetValue():
        selectedWord = cb.GetLabel()
    self.keywordsObj.updateKeyword(self.textNewKeywordShort.GetValue(),selectedWord)#TO-DO
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
    self.keywordsObj.updateNames(self.selectKeywordsFile.getFileName().replace(".xlsx","New.xlsx"),self.selectBusyItemsFile.getFileName())
