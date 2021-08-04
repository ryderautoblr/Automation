import pandas
import os
import numpy as np
def getPhotoPaths(path,currentLinks,photoDf):
    links = []
    if pandas.isnull(path):return currentLinks
    if not pandas.isnull(currentLinks): 
        links.extend(currentLinks)
    else:
        currentLinks = []

    namesList = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        namesList = filenames
        break  
    for n in namesList:
        tempPath = os.path.normpath(path + "/" + n)
        index = photoDf.index[photoDf["System Path"]==tempPath].tolist()
        for i in index:
            links.append(photoDf["Link"].iloc[i])
    
    if len(namesList) != (len(links) - len(currentLinks)):
        print ("Not Matched",namesList,links)
    return ";".join(links)


def getLinks(photoXls,databaseXls):
    databaseDf = pandas.read_excel(databaseXls)
    photoDf = pandas.read_excel(photoXls)

    staticPath = "D:/Automation/websiteScraping/"
    folders = ["Aaron",'VegaPhotos', 'Ls2Photos', 'AxorPhotos', 'StuddsPhotos','FSNWise']
    folderParent = {'VegaPhotos':'vega', 'Ls2Photos':'ls2', 'AxorPhotos':'axor', 'StuddsPhotos':'studds','FSNWise':'',"Aaron":''}
    
    photoDf["System Path"] = ""
    for i in range(photoDf.shape[0]):
        folderPath = photoDf["Folder"].iloc[i]
        fileName = photoDf["Name"].iloc[i]
        hierarchy = folderPath.split("/")
        for j,h in enumerate(hierarchy):
            if h in folders:
                newPath = os.path.normpath(staticPath + "/" + folderParent[h] + "/" + "/".join(hierarchy[j:]) + "/" + fileName)
                photoDf["System Path"].iloc[i] = newPath

    databaseDf["Photo Links GDrive"] = databaseDf.apply(lambda row : getPhotoPaths(row['FSN_Photo'], row['Photo Links GDrive'], photoDf), axis=1)
    databaseDf.to_excel(databaseXls.replace(".xls","New.xls"),index=False)

if __name__ == '__main__':
    getLinks("ImagePaths.xlsx","Comp0009_ListofItems 08_04_2021.xlsx")