import sys
sys.path.insert(1,"../../pathInit/")
import pathInit

import pyautogui
import time
import stringOps
import genericRobotApis
import selectFileAndRunGUI
import wx
import robotFunctions

class downloadFPOsRobot:
    def __init__(self):
        self.chromeObj = genericRobotApis.Chrome()
        self.webAddress = 'https://vendorhub.flipkart.com/v2/#/operations/po/details/'
        defaultPO = 'FABR1704996'
        self.openPO(defaultPO)
        self.downloadImg = robotFunctions.robotImage('download')
        self.GUI = selectFileAndRunGUI.selectFileAndRunGUI(self.on_run,"Select PO list Files")
        
    def on_run(self,files):
        self.chromeObj.accessChrome()
        for f in files:
            self.downloadPOs(f)

    def openPO(self,po):
        self.chromeObj.accessAddressBar()
        time.sleep(0.5)
        stringOps.copyStrToClipboard(self.webAddress + po)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        time.sleep(2)
        


    def downloadPOs(self,listPOFile):
        f = open(listPOFile)
        lines = f.readlines()
        lines = lines[1:]
        f.close()

        for line in lines:
            po = line.split(",")[0]
            self.openPO(po)
            self.downloadImg.accessImage()
            time.sleep(3)
            
if __name__ == '__main__':
    app = wx.App()
    downloadFPOsRobot()
    app.MainLoop()