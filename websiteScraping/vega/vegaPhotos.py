import pickle
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import downloadUtils
import pandas
import os

dbfile = open('vegaDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

folder = os.getcwd().replace("\\","/") + "/VegaPhotos/"
pathInit.createFolder(folder)

def getPhotoDetails(name,hierarcy):
	photoName = name
	photoName = photoName.replace("/","").replace(" ","_")
	hierarcyFolders = hierarcy.split(">>")[1:-1]
	hierarcyFolders = [x.strip() for x in hierarcyFolders]
	hierarcyFolders = "/".join(hierarcyFolders) + "/"
	hierarcyFolders = hierarcyFolders.replace(" ","_")

	photoPath = folder + hierarcyFolders + photoName
	
	return photoName,photoPath


count = 0
for key in db.keys():
	images = db[key]['imageLinks']
	productName = db[key]['name']
	hierarcy = db[key]['hierarchy']

	photoName,photoPath = getPhotoDetails(productName,hierarcy)

	pathInit.createFolder(photoPath)
	photoNames = []

	for i,imageLink in enumerate(images):
		photoNameTemp = photoName + "_" + str(i) + ".png"
		name = photoPath + "/" + photoNameTemp
		# print (name)
		# downloadUtils.getImage(imageLink,name)
		photoNames.append(photoNameTemp)

	# print ("Done!",photoPath, photoName,count)
	count += 1
	# break

# exit()
df = pandas.read_excel("VegaData.xlsx")

photoDirs = []
photoNamesList = []


for i in range(len(df["Product"])):
	productName = df["Product"].iloc[i]
	hierarcy = df["Hierarchy"].iloc[i]
	photoName,photoPath = getPhotoDetails(productName,hierarcy)
	photoDirs.append(photoPath)
	imageLinkData = df["Image Links"].iloc[i]
	if pandas.isnull(imageLinkData): 
		photoNamesList.append('')
		continue
	imageCount = len(imageLinkData.split(";"))
	photoNames = [photoName + "_" + str(x) + ".png" for x in range(imageCount)]
	photoNamesList.append(";".join(photoNames))

df['Photo Paths'] = photoDirs
df['Photo Names'] = photoNamesList

df.to_excel("VegaData.xlsx",index=False)
