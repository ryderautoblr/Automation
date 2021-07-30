import updateKeywordsPanel
import diffKeywordsPanel
import wx
import busyToAppPanel
import tagKeywordsPanel
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import updateFSNPanel
import mergeDatabasePanel
import mergePhotoPanel
import mergeTwoDatabasePanel


class MyFrame(wx.Frame):    
  def __init__(self):
    super().__init__(parent=None, title='RAA GUI',size=(1000,1000))
    nb = wx.Notebook(self) 
    nb.AddPage(mergeDatabasePanel.mergeDatabasePanel(nb),"Merge Database") 
    nb.AddPage(updateKeywordsPanel.updateKeywordsPanel(nb),"Update Keywords") 
    nb.AddPage(tagKeywordsPanel.tagKeywordsPanel(nb),"Tag Keywords") 
    nb.AddPage(diffKeywordsPanel.diffKeywordsPanel(nb),"Diff Keywords") 
    nb.AddPage(busyToAppPanel.busyToAppPanel(nb),"Busy To App Update") 
    nb.AddPage(updateFSNPanel.updateFSNPanel(nb),"Update FSN Database") 
    nb.AddPage(mergePhotoPanel.mergePhotoPanel(nb),"Update Photo Database")
    nb.AddPage(mergeTwoDatabasePanel.mergeTwoDatabasePanel(nb),"Merge Two Database") 
    self.Show(True) 
    self.Centre()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()