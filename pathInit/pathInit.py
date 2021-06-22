import sys
import os

def createFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def getBaseFolder():
    currentDirectory = os.getcwd()
    baseFolder = currentDirectory.split("Automation")[0]
    baseFolder += "Automation\\"
    return baseFolder

baseFolder = getBaseFolder()
def addPath(relativePath):
	global baseFolder
	sys.path.insert(1,baseFolder + "\\" + relativePath + "\\")

def getSubDirs(path):
    subfolders = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        if os.path.isdir(dirpath):
            subfolders.append(dirpath)
    return subfolders

def getAllFiles(path):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for f in filenames:
            file = os.path.join(dirpath, f)
            if os.path.isfile(file):
                files.append(file)
    return files

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