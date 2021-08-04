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
	parser.add_argument("--f")
	args = parser.parse_args()
	return args

def checkIfNan(name):
	return (name == 'nan') or (np.nan == name) or (pandas.isnull(name))

def mergeMultipleAlias(row):
	aliasColNames = ["Name",	"Alias",	"Alias Add1",	"Alias Add2",	"Alias Add3","Long Name","FSN"]

	row = row[aliasColNames]
	row = row.replace(np.nan, '', regex=True)
	row = row.astype(str)
	data = ";".join(row)
	return data


def updateAlias(f):
	df1 = pandas.read_excel(f)
	df1["Cummulative Alias"] = df1.apply(lambda row : mergeMultipleAlias(row),axis=1)
	df1.to_excel(f.replace(".xls","New.xls"),index=False)
	
if __name__ == "__main__":
	args = getArgs()
	print (args)
	updateAlias(args.f)