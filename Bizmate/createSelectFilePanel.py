import os
import wx

class createSelectFilePanel():
  def __init__(self, parent,title,offsetx,offsety):
    
    self.textFile = wx.TextCtrl(parent, pos=(offsetx + 10,offsety + 5),size=(800,45), style=wx.TE_MULTILINE)
    self.select_btn = wx.Button(parent, label=title, pos=(offsetx + 10,offsety + 55))
    self.select_btn.Bind(wx.EVT_BUTTON, self.on_select)
    self.parent = parent

  def on_select(self,event):
    filePathsStr = ""
    filePaths = []
    self.currentDirectory = os.getcwd()
    
    dlg = wx.FileDialog(
    self.parent, message="Choose a file",
    defaultDir=self.currentDirectory, 
    defaultFile="",
    style=wx.FD_OPEN | wx.FD_CHANGE_DIR
    )

    if dlg.ShowModal() == wx.ID_OK:
      paths = dlg.GetPaths()
      for path in paths:
        filePaths.append(path)

    dlg.Destroy()                
    filePathsStr = "\n".join(filePaths)
    self.textFile.SetValue(filePathsStr)

  def getFileName(self):
    return self.textFile.GetValue()

  def disable(self):
    self.textFile.Disable()
    self.select_btn.Disable()

  def enable(self):
    self.textFile.Enable()
    self.select_btn.Enable()



