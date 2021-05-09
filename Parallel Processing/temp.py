import pandas

df = pandas.read_excel("Comp0009_ListofItemsNewNew.xlsx")
longNames = df['Long Name'].astype(str).to_list()
splitData = 8

longNames2D = [[] for i in range(splitData)]
for i in range(len(longNames)):
    longNames2D[i%splitData].append(longNames[i])

def f(i):
	found = []
	print (i)
	
	for d in longNames2D[i]:
		if "Studds" in d:
			found.append(d)
	
	return found
    