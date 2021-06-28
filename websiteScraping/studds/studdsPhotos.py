import pickle
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import downloadUtils
import os
import pandas

dbfile = open('studdsDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

folder = os.getcwd().replace("\\","/") + "/StuddsPhotos/"
pathInit.createFolder(folder)

def getPhotoDetails(category,name):
	photoName = name + ".png"
	photoName = photoName.replace("/","").replace(" ","_")

	photoPath = folder + category.replace(" ","_")
	
	return photoName,photoPath

for key in db.keys():
	products = db[key]['products']
	
	pathInit.createFolder(folder + key)
	for p in products:
		photoName,photoPath = getPhotoDetails(key,p[0])
		name = photoPath + "/" + photoName
		link = p[1]
		# downloadUtils.getImage(link,name)
	# break

photoDirs = []
photoNamesList = []

df = pandas.read_excel("StuddsData.xlsx")

for i in range(len(df["Category"])):
	productName = df["Product"].iloc[i]
	if pandas.isnull(productName): 
		photoDirs.append("")
		photoNamesList.append("")
		continue

	category = df["Category"].iloc[i]
	productName = productName.split(" (")[0]


	
	photoName,photoPath = getPhotoDetails(category,productName)
	photoDirs.append(photoPath)
	photoNamesList.append(photoName)

df['Photo Paths'] = photoDirs
df['Photo Names'] = photoNamesList

df.to_excel("StuddsData.xlsx",index=False)
