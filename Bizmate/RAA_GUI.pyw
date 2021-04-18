import updateKeywordsPanel
import diffKeywordsPanel
import wx
import busyToAppPanel
import tagKeywordsPanel

class MyFrame(wx.Frame):    
  def __init__(self):
    super().__init__(parent=None, title='RAA GUI',size=(1000,700))
    nb = wx.Notebook(self) 
    nb.AddPage(updateKeywordsPanel.updateKeywordsPanel(nb),"Update Keywords") 
    nb.AddPage(tagKeywordsPanel.tagKeywordsPanel(nb),"Tag Keywords") 
    nb.AddPage(diffKeywordsPanel.diffKeywordsPanel(nb),"Diff Keywords") 
    nb.AddPage(busyToAppPanel.busyToAppPanel(nb),"Busy To App Update") 
    self.Show(True) 
    self.Centre()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()