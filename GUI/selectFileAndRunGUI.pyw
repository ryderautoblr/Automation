import wx
import os
import sys

sys.path.insert(1,"../pathInit/")
import pathInit
import createParentFrameWithTitle
import addSelectFilePanel
import consolidatePOs

class HI:
    def on_run(self,files):
        print ("hi",files)
        return

class selectFileAndRunGUI():
    def __init__(self,funcOnRun,title):
        self.funcOnRun = funcOnRun
        self.mainFrame = createParentFrameWithTitle.createParentFrameWithTitle(title)
        self.panel = wx.Panel(self.mainFrame.frame)
        self.selectFile = addSelectFilePanel.addSelectFilePanel(self.panel,self.mainFrame.frame)

        #run algorithm
        x = 5
        y = self.selectFile.endY + 30
        self.runBtn = wx.Button(self.panel, label='Run', pos=(x, y))
        self.runBtn.Bind(wx.EVT_BUTTON, self.on_run)

        #show
        self.mainFrame.frame.Raise()
        self.mainFrame.frame.Show()

    def on_run(self, event):
        loc = self.selectFile.getSelectedFiles()
        self.funcOnRun(loc)
        return

if __name__ == '__main__':
    app = wx.App()
    hiObj = HI()
    selectFileAndRunGUI(hiObj.on_run,"hi")
    app.MainLoop()
