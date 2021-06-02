import wx
import os
import createSelectFilePanel
import mergeDatabase

class mergeDatabasePanel(wx.Panel):
  def __init__(self, parent): 
    super(mergeDatabasePanel, self).__init__(parent) 

    self.busyFile = createSelectFilePanel.createSelectFilePanel(self,'Select Busywin Database',0,0)
    self.FullDatabaseFile = createSelectFilePanel.createSelectFilePanel(self,'Select Final Database',0,100)   

    self.btnRun = wx.Button(self, label='Run', pos=(10, 200))
    self.btnRun.Bind(wx.EVT_BUTTON, self.on_run)

  def on_run(self, event):
    mergeDatabase.mergeDatabase(self.busyFile.getFileName(),self.FullDatabaseFile.getFileName())
