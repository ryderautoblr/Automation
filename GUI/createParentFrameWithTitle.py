import wx

class createParentFrameWithTitle():
    def __init__(self,myTitle="RAA"):
        self.frame = wx.Frame(parent=None, title=myTitle,size=(1000,700))
