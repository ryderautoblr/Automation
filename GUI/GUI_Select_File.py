import wx
import os
import wx.lib.scrolledpanel as scrolled

class MyFrame():
    def __init__(self):
        self.frame = wx.Frame(parent=None, title='Hello World',size=(1000,500))
        panel = wx.Panel(self.frame)

        self.panel2 = scrolled.ScrolledPanel(panel, pos=(5, 5),size=(500,95))

        self.textFile = wx.TextCtrl(self.panel2, size=(500,95), style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)
        my_btn = wx.Button(panel, label='Select Invoice', pos=(5, 105))
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)

        languages = ['C', 'C++', 'Python', 'Java', 'Perl', 'asdfghjkloiuytrreqvxbncmiuwuysbyu'] 
        self.combo = wx.ComboBox(panel,choices = languages, pos=(155, 105), size=(100,50))

        self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo) 

        self.label = wx.StaticText(panel,label = "Your choice:" ,style = wx.ALIGN_CENTRE, pos=(455, 105)) 

        self.panel2.SetupScrolling()
        self.frame.Show()

    def OnCombo(self, event): 
        self.label.SetLabel("You selected"+self.combo.GetValue()+" from Combobox")  
 

    def on_press(self, event):

        filePathsStr = ""
        filePaths = []
        self.currentDirectory = os.getcwd()
        
        dlg = wx.FileDialog(
        self.frame, message="Choose a file",
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

        self.textFile.AppendText(filePathsStr)

        self.textFile.SetDefaultStyle(wx.TextAttr(wx.RED))
        self.textFile.AppendText("Red text\n")
        self.textFile.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.LIGHT_GREY))
        self.textFile.AppendText("Red on grey text\n")
        self.textFile.SetDefaultStyle(wx.TextAttr(wx.BLUE))
        self.textFile.AppendText("Blue on grey text\n")

        # for child in self.panel2.GetChildren():
        #     child.Destroy()

        
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
