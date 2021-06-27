import pickle
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import downloadUtils

dbfile = open('axorDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

folder = "./AxorPhotos/"
pathInit.createFolder(folder)

count = 0
for key in db.keys():
	images = db[key]['imageLinks']
	productName = db[key]['name']
	color = db[key]['color']
	photoName = productName + "_C_" + color
	photoName = photoName.replace("/","").replace(" ","_")
	pathInit.createFolder(folder + photoName)
	for i,imageLink in enumerate(images):
		name = folder + photoName + "/" + photoName + "_" + str(i) + ".png"
		downloadUtils.getImage(imageLink,name)
	print ("Done!", photoName,count)
	count += 1
	# break