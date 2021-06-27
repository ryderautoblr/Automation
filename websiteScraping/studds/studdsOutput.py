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

dbfile = open('studdsDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()


data = []
for key in db.keys():
	if "CRUISER" in key: print (key)
	category = [key]
	product = [x[0] + " (%s)" % x[1] for x in db[key]['products']]
	mrp = db[key]['mrp']
	mrp = re.findall(r'\d+\.\d+', mrp)
	size = [x[0] + " (%s)" % x[1] for x in db[key]['sizes']]
	description = ''
	link = [db[key]['link']]
	for desc in db[key]['description']:
		if len(desc) > 0:
			description += desc[0]
		if len(desc) > 1: 
			description += " :- " + desc[1] + "\n"
		if len(desc) == 1:
			description += "\n"

	description = [description]
	permList = [category,product,mrp,size,description,link]
	outputPerm = permute.permulteList(permList)
	if "CRUISER" in key: print (outputPerm,permList)
	data.extend(outputPerm)
	
df = pandas.DataFrame(data,columns=["Category","Product","MRP","Size","Description","Link"])
df['Photo Url'] = df["Product"].apply(getSubAttr)
df['Dimensions'] = df["Size"].apply(getSubAttr)

df.to_excel("StuddsData.xlsx",index=False)

# print (df)