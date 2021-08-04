import pandas
from os import walk 
import os

def checkInAlias(aliases,alias):
    possible = aliases.split(";")
    return bool(alias in possible)


def getFSNWisePhotos(folder,database):
    folders = []
    possible = []
    for (dirpath, dirnames, filenames) in walk(folder):
        for directory in dirnames:
            folders.append(os.path.join(folder,directory))
            possible.append(directory)
        break     

    count = 0
    tag = "FSN_Photo"
    databaseDF = pandas.read_excel(database)
    databaseDF[tag] = ""
    for i,alias in enumerate(possible):
        if pandas.isnull(alias):continue
        isAlias = databaseDF['Cummulative Alias'].apply(checkInAlias,args=(alias,))
        if isAlias.any():
            index = isAlias.index[isAlias == True].tolist()
            count += 1
            print ("Found",alias,i,count)
            for j in index:
                databaseDF[tag].iloc[j] = folders[i]

    print (count)
    databaseDF.to_excel(database.replace(".xls","New.xls"),index=False)

if __name__ == "__main__":
    getFSNWisePhotos("D:\\Automation\\websiteScraping\\FSNWise\\","D:\\Automation\\Bizmate\\Comp0009_ListofItems 08_01_2021New.xlsx")