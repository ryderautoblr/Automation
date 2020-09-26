import wx
import os
import wx.lib.scrolledpanel as scrolled

class addSelectFilePanel():
    def __init__(self,panel,frame,x=5,y=5):
        self.frame = frame
        #create window
        w=500; h=95
        self.display = scrolled.ScrolledPanel(panel, pos=(x, y),size=(w,h))
        self.textWindow = wx.TextCtrl(self.display, size=(w,h), style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)

        #create button
        y = h+30
        self.selectFileBtn = wx.Button(panel, label='Select Files', pos=(x, y))
        self.selectFileBtn.Bind(wx.EVT_BUTTON, self.on_press_select_file)
        self.endX = x
        self.endY = y

    def on_press_select_file(self, event):

        filePathsStr = ""
        filePaths = []
        self.currentDirectory = os.getcwd()
        
        dlg = wx.FileDialog(
        self.frame, message="Choose files",
        defaultDir=self.currentDirectory, 
        defaultFile="",
        style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                filePaths.append(path)

        dlg.Destroy()
        filePathsStr = "\n".join(filePaths) + "\n"

        self.textWindow.AppendText(filePathsStr)

        return



        
