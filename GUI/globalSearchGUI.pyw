import wx
import os
import sys

sys.path.insert(1,"../pathInit/")
import pathInit
import createParentFrameWithTitle
import addGlobalSearchPanel
import loadRaaDatabase

class globalSearchGUI():
    def __init__(self,title,database=[],toFind=["hi"]):
        self.database = None
        if not database:
            self.raaDatabase = loadRaaDatabase.raaDatabase()
            self.database = self.raaDatabase.getNames()
        else:
            self.database = database

        self.toFind = toFind
        self.mainFrame = createParentFrameWithTitle.createParentFrameWithTitle(title)
        self.panel = wx.Panel(self.mainFrame.frame)
        self.seacrh = addGlobalSearchPanel.addGlobalSearchPanel(self.panel,self.mainFrame.frame,self.database,self.toFind)

        #show
        self.mainFrame.frame.Raise()
        self.mainFrame.frame.Show()

if __name__ == '__main__':
    app = wx.App()
    globalSearchGUI("hi")
    app.MainLoop()
