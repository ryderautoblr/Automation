import pickle
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import downloadUtils

dbfile = open('studdsDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

folder = "./StuddsPhotos/"
pathInit.createFolder(folder)


for key in db.keys():
	products = db[key]['products']
	key = key.replace(" ","_")
	pathInit.createFolder(folder + key)
	for p in products:
		name = folder + key + "/" + p[0] + ".png"
		link = p[1]
		downloadUtils.getImage(link,name)
	# break