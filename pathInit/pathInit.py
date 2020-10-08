import sys
import os

sys.path.insert(1,"../StringOps/")
sys.path.insert(1,"../GUI/")
sys.path.insert(1,"../pathInit/")
sys.path.insert(1,"../excelOps/")
sys.path.insert(1,"../Database/")

def getBaseFolder():
    currentDirectory = os.getcwd()
    baseFolder = currentDirectory.split("Automation")[0]
    baseFolder += "Automation\\"
    return baseFolder