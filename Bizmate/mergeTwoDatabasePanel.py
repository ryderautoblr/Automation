import wx
import os
import createSelectFilePanel
import mergeTwoDatabase
import wx.lib.scrolledpanel as scrolled

class mergeTwoDatabasePanel(scrolled.ScrolledPanel):
  def __init__(self, parent): 
    super(mergeTwoDatabasePanel, self).__init__(parent) 
    self.SetupScrolling()

    self.busyFile = createSelectFilePanel.createSelectFilePanel(self,'Select First Database',0,0)
    self.FullDatabaseFile = createSelectFilePanel.createSelectFilePanel(self,'Select Second Database',0,100)   

    self.btnRun = wx.Button(self, label='Run', pos=(10, 200))
    self.btnRun.Bind(wx.EVT_BUTTON, self.on_run)

  def on_run(self, event):
    mergeTwoDatabase.mergeDatabase(self.busyFile.getFileName(),self.FullDatabaseFile.getFileName())
