import wx
import os
import sys

sys.path.insert(1,"../pathInit/")
import pathInit
import createParentFrameWithTitle
import addSelectFilePanel
import consolidatePOs

class consolidatePOsGUI():
    def __init__(self):
        self.mainFrame = createParentFrameWithTitle.createParentFrameWithTitle("Consolidate Flipkart POs")
        self.panel = wx.Panel(self.mainFrame.frame)
        self.selectFile = addSelectFilePanel.addSelectFilePanel(self.panel,self.mainFrame.frame)

        #run algorithm
        x = 5
        y = self.selectFile.endY + 30
        self.runBtn = wx.Button(self.panel, label='Run', pos=(x, y))
        self.runBtn.Bind(wx.EVT_BUTTON, self.on_run)

        #show
        self.mainFrame.frame.Show()


    def on_run(self, event):
        loc = self.selectFile.getSelectedFiles()
        consolidatePOs.consolidatePOs(loc)
        return

if __name__ == '__main__':
    app = wx.App()
    consolidatePOsGUI()
    app.MainLoop()
