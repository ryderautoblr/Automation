import pickle
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import permute
import pandas
import re

def getSubAttr(attr):
	if attr is None: return ""
	subAttrs = attr.split(" (")
	if len(subAttrs) == 2:
		return subAttrs[1].split(")")[0]
	return ""

dbfile = open('axorDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

data = []
for key in db.keys():
	productLink = [key]
	productName = [db[key]['name']]
	color = [db[key]['color']]
	mrp = [db[key]['mrp']]
	desc = [db[key]['desc']]
	sizes = db[key]['size'] # to permute
	images = [";".join(db[key]['imageLinks'])]

	
	permList = [productName,mrp,sizes,desc,productLink,images]
	outputPerm = permute.permulteList(permList)
	data.extend(outputPerm)
	
df = pandas.DataFrame(data,columns=["Product","MRP","Size","Description","Link","Image Links"])

df.to_excel("AxorData.xlsx",index=False)
