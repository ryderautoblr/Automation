import wx
import time
import pyautogui
import wx
import os
import wx.lib.scrolledpanel as scrolled
import re

class addGlobalSearchPanel(wx.Panel):
    def __init__(self, panel,frame,database,toFind,x=5,y=5):
        self.frame = frame
        self.database = database
        self.toFind = toFind
        self.toFindIndex = -1
        self.matches = [() for i in range(len(self.toFind))]
        self.labelToMatch = wx.StaticText(panel, label = "Match:", pos = (x,y))
        
        y += 50

        self.database = database
        self.database.append("None")
        self.combobox = wx.ComboBox(panel, choices = self.database, pos = (x,y),style = wx.TE_PROCESS_ENTER)

        y += 30
        self.labelSelected = wx.StaticText(panel, label = "", pos = (x,y))

        y += 30
        self.nextBtn = wx.Button(panel, label='Next', pos=(x, y))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.OnNext)

        x += 150
        self.prevBtn = wx.Button(panel, label='Prev', pos=(x, y))
        self.prevBtn.Bind(wx.EVT_BUTTON, self.OnPrev)

        x += 150
        self.saveBtn = wx.Button(panel, label='Save', pos=(x, y))
        self.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)

        panel.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        panel.Bind(wx.EVT_TEXT, self.OnText)
        panel.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        self.prev_value_cb = None
        
        self.endX = x
        self.endY = y
        
    def loadData(self):
        self.labelToMatch.SetLabel("To Find: " + self.toFind[self.toFindIndex])

    def saveData(self):
        if self.toFindIndex > -1:
            self.matches[self.toFindIndex] = (self.toFind[self.toFindIndex],self.combobox.GetValue())

    def OnSave(self,event):
        f = open("matches.txt","w")
        print (self.matches)
        for m in self.matches:
            if m:
                f.write(m[0] + " --> " + m[1] + "\n")
        f.close()

    def OnNext(self,event):
        self.saveData()
        self.toFindIndex += 1
        self.toFindIndex = min(self.toFindIndex,len(self.toFind)-1)
        self.loadData()

    def OnPrev(self,event):
        self.saveData()
        self.toFindIndex += -1
        self.toFindIndex = max(self.toFindIndex,0)
        self.loadData()

    def OnText(self, event):
        current_value = self.combobox.GetValue()
        if (len(current_value)>3) and (current_value != self.prev_value_cb) and current_value not in self.database:
            self.prev_value_cb = current_value
            words = current_value.split(" ")
            filterList = self.database
            for w in words:
                if w:
                    r = re.compile(".*" + w, re.IGNORECASE)
                    filterList = list(filter(r.match,filterList))
            self.combobox.SetItems(filterList)
            self.combobox.SetValue(current_value)
            pyautogui.press('end')
    
    def OnEnter(self,event):
        self.combobox.Popup()        
            
    def OnCombo(self, event):
        self.labelSelected.SetLabel("Match Selected: " + self.combobox.GetValue())
        