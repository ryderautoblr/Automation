import wx
import time
import pyautogui
import wx
import os
import wx.lib.scrolledpanel as scrolled
import re

class addGlobalSearchPanel(wx.Panel):
    def __init__(self, panel,keyword="",database = [],x=5,y=5):
        self.database = database
        
        deleteNames = []
        for name in self.database:
            if keyword not in name:
                deleteNames.append(name)
        for name in deleteNames:
            self.database.remove(name)
        
        self.database.append("None")
        self.combobox = wx.ComboBox(panel, choices = self.database, pos = (x,y))
        y +=50
        self.textNewFSN = wx.TextCtrl(panel, pos=(x, y),size=(800,30))
        self.textNewFSN.Bind(wx.EVT_TEXT,self.OnText)

        y += 50
        self.labelSelected = wx.StaticText(panel, label = "", pos = (x,y))
        panel.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        # panel.Bind(wx.EVT_TEXT, self.OnText)
        panel.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        self.prev_value_cb = None
        
        self.endX = x
        self.endY = y + 50
        self.inEvent = False
        self.isPopUp = False

    def OnText(self, event):
        if self.inEvent: return
        current_value = self.textNewFSN.GetValue()
        self.showOptions()
        if (len(current_value)>3) and (current_value != self.prev_value_cb) and (current_value not in self.database):
            self.inEvent = True
            self.prev_value_cb = current_value
            words = current_value.split(" ")
            filterList = self.database
            for w in words:
                if w:
                    r = re.compile(".*" + w, re.IGNORECASE)
                    filterList = list(filter(r.match,filterList))
            self.combobox.SetItems(filterList)
            self.textNewFSN.SetInsertionPoint()
            #self.combobox.SetValue(current_value)
            #pyautogui.press('end')
        self.inEvent = False
    
    def showOptions(self):
        if not self.isPopUp:
            self.isPopUp = True
            self.combobox.Popup()    

    def hideOptions(self):
        if self.isPopUp:
            self.isPopUp = False
            self.combobox.Popup()

    def OnEnter(self,event):
        self.isPopUp = not self.isPopUp
        self.combobox.Popup()
            
    def OnCombo(self, event):
        self.labelSelected.SetLabel("Match Selected: " + self.combobox.GetValue())
        