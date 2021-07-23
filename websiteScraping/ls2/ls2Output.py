import pickle
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import permute
import pandas
import re

dbfile = open('ls2DataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

data = []
for key in db.keys():

	productLink = [key]
	productName = [db[key]['name']]
	mrp = db[key]['mrp']
	mrp = re.findall(r'\d+[\.,]\d+', mrp)
	desc = db[key]['desc']
	descStr = ''
	for d in desc:
		descStr += d[0] + ":-" + d[1] + "\n"
	descStr = [descStr]
	images = [";".join(db[key]['imageLinks'])]
	sizes = ["M","L","XL"]
	
	permList = [productName,mrp,sizes,descStr,productLink,images]
	outputPerm = permute.permulteList(permList)
	data.extend(outputPerm)
	
df = pandas.DataFrame(data,columns=["Product","MRP","Size","Description","Link","Image Links"])

df.to_excel("Ls2Data.xlsx",index=False)
