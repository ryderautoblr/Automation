import wx
import os

class addSelectFilePanel():
	def __init__(self,panel):
		#create window
		self.display = scrolled.ScrolledPanel(panel, pos=(5, 5),size=(500,95))
		self.textWindow = wx.TextCtrl(self.display, size=(500,95), style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)

		#create button
		self.selectFileBtn = wx.Button(panel, label='Select Files', pos=(5, 105))
        self.selectFileBtn.Bind(wx.EVT_BUTTON, self.on_press_select_file)

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
        


        
