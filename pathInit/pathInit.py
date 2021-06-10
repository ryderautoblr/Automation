import sys
import os


def getBaseFolder():
    currentDirectory = os.getcwd()
    baseFolder = currentDirectory.split("Automation")[0]
    baseFolder += "Automation\\"
    return baseFolder

baseFolder = getBaseFolder()
def addPath(relativePath):
	global baseFolder
	sys.path.insert(1,baseFolder + "\\" + relativePath + "\\")

addPath("GUI")
addPath("pathInit")
addPath("excelOps")
addPath("Database")
addPath("Flipkart")
addPath("Flipkart\\database")
addPath("robot")
addPath("stringOps")
addPath("Database\\LS2")
addPath("BeautifulSoup")
addPath("webUtils")
addPath("Others")