import pickle
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import downloadUtils
import pandas
import os

dbfile = open('axorDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

folder = os.getcwd().replace("\\","/") + "/AxorPhotos/"
pathInit.createFolder(folder)

def getPhotoDetails(name,color):
	photoName = name + "_C_" + color
	photoName = photoName.replace("/","").replace(" ","_")

	photoPath = folder + photoName
	
	return photoName,photoPath


count = 0
for key in db.keys():
	images = db[key]['imageLinks']
	productName = db[key]['name']
	color = db[key]['color']

	photoName,photoPath = getPhotoDetails(productName,color)

	pathInit.createFolder(photoPath)
	photoNames = []

	for i,imageLink in enumerate(images):
		photoName = photoName + "_" + str(i) + ".png"
		name = photoPath + "/" + photoName
		# downloadUtils.getImage(imageLink,name)
		photoNames.append(photoName)

	print ("Done!",photoPath, photoName,count)
	count += 1
	# break

df = pandas.read_excel("AxorData.xlsx")

photoDirs = []
photoNamesList = []


for i in range(len(df["Product"])):
	productName = df["Product"].iloc[i]
	color = df["Color"].iloc[i]
	photoName,photoPath = getPhotoDetails(productName,color)
	photoDirs.append(photoPath)
	imageLinkData = df["Image Links"].iloc[i]
	imageCount = len(imageLinkData.split(";"))
	photoNames = [photoName + "_" + str(x) + ".png" for x in range(imageCount)]
	photoNamesList.append(";".join(photoNames))

df['Photo Paths'] = photoDirs
df['Photo Names'] = photoNamesList

df.to_excel("AxorData.xlsx",index=False)
