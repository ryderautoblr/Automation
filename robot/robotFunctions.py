import pyautogui
import os
from matplotlib import pyplot as plt
from matplotlib.widgets import RectangleSelector
import pathInit
import time

class checkAndCreateTemplate():
    def __init__(self,imageName):
        self.x1=-1
        self.w=-1
        self.y1=-1
        self.h=-1
        self.imageName = imageName

        self.im = pyautogui.screenshot()
        fig, current_ax = plt.subplots()    
        plt.title('Select ' + imageName)
        plt.imshow(self.im)
        
        rs = RectangleSelector(current_ax, self.line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
        
        plt.show()
        if self.x1 == -1: 
            print ('No Image Selected!! Try Again')
            exit(-1)

    def line_select_callback(self,eclick, erelease):
        self.x1, self.y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.w = abs(x2-self.x1)
        self.h = abs(y2-self.y1)
        im = self.im.crop((self.x1,self.y1,x2,y2))
        im.save(self.imageName)

def createTemplate(imageName):
    loc = None
    if os.path.isfile(imageName): loc = pyautogui.locateOnScreen(imageName)
    if loc is None:
        objTemplate = checkAndCreateTemplate(imageName)
        return objTemplate.x1,objTemplate.y1,objTemplate.w,objTemplate.h
    return loc[0],loc[1],loc[2],loc[3]

class robotImage:
    def __init__(self,imageName):
        self.imageName = pathInit.getBaseFolder() + 'Temp\\' + imageName + '.png'
        self.x1,self.y1,self.w,self.h = createTemplate(self.imageName)

    def accessImage(self):
        pyautogui.click(self.x1 + self.w/2,self.y1 + self.h/2)

    def getBox(self):
        return self.x1,self.y1,self.w,self.h

    def locateOnScreen(self):
        loc = None
        while loc is None:
            time.sleep(0.2)
            loc = pyautogui.locateOnScreen(self.imageName)
