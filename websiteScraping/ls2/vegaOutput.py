import pickle
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import permute
import pandas
import re

dbfile = open('vegaDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

data = []
for key in db.keys():

	productLink = [key]
	productName = [db[key]['name']]
	hierarchy = [db[key]['hierarchy']]
	mrp = db[key]['mrp']
	mrp = re.findall(r'\d+[\.,]\d+', mrp)
	desc = db[key]['desc']
	descStr = ''
	for d in desc:
		descStr += d[0] + ":-" + d[1] + "\n"
	descStr = [descStr]
	sizes = db[key]['size'] # to permute
	images = [";".join(db[key]['imageLinks'])]
	
	permList = [productName,hierarchy,mrp,sizes,descStr,productLink,images]
	outputPerm = permute.permulteList(permList)
	data.extend(outputPerm)
	
df = pandas.DataFrame(data,columns=["Product","Hierarchy","MRP","Size","Description","Link","Image Links"])

df.to_excel("VegaData.xlsx",index=False)
