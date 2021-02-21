import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import selectFileAndRunGUI
import wx
import flipkartPOs
import loadRaaDatabase

class updateDatabase:
    def __init__(self):
        self.GUI = selectFileAndRunGUI.selectFileAndRunGUI(self.on_run,"Select PO list Files")

    def getUniqueFSNData(self,loc):
        FSNData = []
        FSNs = []

        count = 0
        for l in range(len(loc)):
            #open wb
            print (loc[l],count)
            count += 1
            poData, _, _ = flipkartPOs.getFlipkartPO(loc[l],isSkipZeroQty=False)
            
            for i in range(len(poData[0])):
                data = []
                if poData[0][i] not in FSNs:
                    FSNs.append(poData[0][i])
                    for c in range(len(poData)):
                        data.append(poData[c][i])
                    FSNData.append(data) 
        print (FSNData)      
        return FSNData


    def findMatches(self,FSNData):
        count = 0
        raaDatabase = loadRaaDatabase.raaDatabase()
        for r in range(len(FSNData)):
            fsn = FSNData[r][0]
            matchData, matchFound = raaDatabase.queryFSN(fsn)
            if not matchFound:
                print (FSNData[r])
                count += 1
        print (count)

    def on_run(self,loc):
        FSNData = self.getUniqueFSNData(loc)
        self.findMatches(FSNData)
        
        
if __name__ == '__main__':
    app = wx.App()
    updateDatabase()
    app.MainLoop()