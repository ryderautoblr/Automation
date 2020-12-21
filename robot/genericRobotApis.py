import robotFunctions
import pyautogui

class Chrome:
    def __init__(self):
        self.chromeImgObj = robotFunctions.robotImage('chrome')
        self.accessChrome()
        self.refreshImgObj = robotFunctions.robotImage('refresh')
        x,y,w,h = self.refreshImgObj.getBox()
        self.addressX = x + w/2 + 100
        self.addressY = y + h/2
    
    def accessChrome(self):
        self.chromeImgObj.accessImage()

    def accessAddressBar(self):
        pyautogui.click(self.addressX,self.addressY)
