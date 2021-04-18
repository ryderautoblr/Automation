import xlrd

sheet = xlrd.open_workbook("keywordsOriginal.xlsx").sheet_by_index(0)

keywordsDict = dict()
for row in range(sheet.nrows):
	oldWord = sheet.cell_value(row,0)
	newWord = sheet.cell_value(row,1)
	keywordsDict[oldWord] = newWord

sheet = xlrd.open_workbook("Comp0009_ListofItems.xlsx").sheet_by_index(0)

for row in range(3,sheet.nrows):
	words = sheet.cell_value(row,0).split(" ")
	newWords = []
	for word in words:
		newWords.append(keywordsDict[word])

	newName = " ".join(newWords)
	print (sheet.cell_value(row,0),newName) 