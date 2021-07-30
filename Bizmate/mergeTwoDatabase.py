import os
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import math
import pandas
import wx
import numpy as np
import argparse

def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("--f1")
	parser.add_argument("--f2")
	args = parser.parse_args()
	return args

def checkIfNan(name):
	return (name == 'nan') or (np.nan == name) or (pandas.isnull(name))

def mergeDatabase(file1,file2):
	df1 = pandas.read_excel(file1)
	df2 = pandas.read_excel(file2)
	newDf = pandas.merge(df1,df2,how='outer',on="Long Name")
	# print (newDf.iloc[570].to_list())

	cols = newDf.columns
	for i in range(len(newDf[cols[0]])):
		# if i != 570: continue
		for j in range(len(cols)):
			if "_x" in cols[j]: continue
			if "_y" in cols[j]:
				if not checkIfNan(newDf[cols[j]].iloc[i]):
					# print (newDf[cols[j]].iloc[i],cols[j])
					newDf[cols[j].replace("_y","_x")].iloc[i] = newDf[cols[j]].iloc[i]

	# print (newDf.iloc[570].to_list())


	for j in range(len(cols)):
		if "_y" in cols[j]: del newDf[cols[j]]
		if "_x" in cols[j]: newDf.rename(columns={cols[j]: cols[j].replace("_x","")}, inplace=True)

	# print (newDf.iloc[570].to_list())
	
	newDf.to_excel(file1.replace(".xls","New.xls"),index=False)
	
if __name__ == "__main__":
	args = getArgs()
	print (args)
	mergeDatabase(args.f1,args.f2)