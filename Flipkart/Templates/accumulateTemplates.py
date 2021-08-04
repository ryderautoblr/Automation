import pandas
from os import walk 
import os

def checkInAlias(aliases,alias):
    possible = aliases.split(";")
    return bool(alias in possible)

def getTemplates(folder,databaseFile):
    files = []
    for (dirpath, dirnames, filenames) in walk(folder):
        for file in filenames:
            if ".xls" in file:
                files.append(os.path.join(folder,file))
        break        
    
    finalDf = pandas.DataFrame()
    for f in files:
        df = pandas.read_excel(f, sheet_name=None)
        if 'Index' in df.keys():
            sheet = list(df.keys())[2]
            dfSheet = df[sheet]
            dfSheet = dfSheet.drop([0,1,2])
            # if dfSheet["Flipkart Product Link"].isnull().any():
            finalDf = finalDf.append(dfSheet,ignore_index=True)
        else:
            print ("Not Flipkart",df.keys())

    possibleCols = ["Flipkart Serial Number","Flipkart Product Link","Seller SKU ID"]
    finalDf = finalDf.drop_duplicates(subset=possibleCols)

    count = 0
    databaseDF = pandas.read_excel(databaseFile)
    possible = []
    for col in possibleCols:
        possible.extend(finalDf[col].to_list())

    cols = finalDf.columns
    for col in cols:
        if "Unnamed" not in col:
            databaseDF["Flipkart_" + col] = ''

    for i,alias in enumerate(possible):
        if pandas.isnull(alias):continue
        isAlias = databaseDF['Cummulative Alias'].apply(checkInAlias,args=(alias,))
        if isAlias.any():
            index = isAlias.index[isAlias == True].tolist()
            count += 1
            print ("Found",alias,i,count)
            for j in index:
                for col in cols:
                    if "Unnamed" not in col:
                        databaseDF["Flipkart_" + col].iloc[j] = finalDf[col].iloc[i%len(finalDf[cols[0]])]
            
    print (count)
    databaseDF.to_excel(databaseFile.replace(".xls","New.xls"),index=False)

if __name__ == "__main__":
    getTemplates('./',"D:\\Automation\\Bizmate\\Comp0009_ListofItems 08_01_2021.xlsx")