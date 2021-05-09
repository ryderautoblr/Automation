import wx
import time
import pyautogui
import wx
import os
import wx.lib.scrolledpanel as scrolled
import re

class addGlobalSearchPanelTextBox(wx.Panel):
    def __init__(self, panel,keyword="",database = [],x=5,y=5):
        self.database = database
        self.database.append("None")
        self.labelFilter = wx.StaticText(panel, label = "Filter:", pos = (x,y))
        self.textFilter = wx.TextCtrl(panel, pos=(x+140, y),size=(800,30),style=wx.TE_PROCESS_ENTER)
        self.textFilter.Bind(wx.EVT_TEXT,self.OnText)
        self.textFilter.Bind(wx.EVT_TEXT_ENTER,self.onDown)

        y += 50
        self.labelFilter = wx.StaticText(panel, label = "Filtered:", pos = (x,y))
        self.textDetails = wx.TextCtrl(panel, pos=(x+140,y),size=(800,195), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.textDetails.Bind(wx.EVT_TEXT_ENTER,self.onEnter)
        y += 200

        self.labelSelected = wx.StaticText(panel, label = "", pos = (x,y))
        y += 50
        self.prev_value_cb = None
        
        self.endX = x
        self.endY = y
        self.inEvent = False
        self.isPopUp = False

    def setDatabase(self,database):
        self.database = database
        self.textDetails.SetValue("\n".join(database))

    def OnText(self, event):
        if self.inEvent: return
        current_value = self.textFilter.GetValue()
        if (len(current_value)>3) and (current_value != self.prev_value_cb) and (current_value not in self.database):
            self.inEvent = True
            self.prev_value_cb = current_value
            words = current_value.split(" ")
            filterList = self.database
            for w in words:
                if w:
                    r = re.compile(".*" + w, re.IGNORECASE)
                    filterList = list(filter(r.match,filterList))
            self.textDetails.SetValue("\n".join(filterList))
        self.inEvent = False

    def onEnter(self, event):
        curPos = self.textDetails.GetInsertionPoint()
        lineNum = len(self.textDetails.GetRange( 0, self.textDetails.GetInsertionPoint() ).split("\n"))-1
        lineText = self.textDetails.GetLineText(lineNum)
        self.labelSelected.SetLabel(lineText)    

    def onDown(self,event):
        self.textDetails.SetFocus()
        self.textDetails.SetInsertionPoint(0)
