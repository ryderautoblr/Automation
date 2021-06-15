
def permuteTwo(a,b=None):
	cperm = []
	for ea in a:
		if type(ea) is not list:
			ea = [ea]
		if b is not None:
			if len(b) == 0: 
				eaCopy = ea.copy()
				eaCopy.append('')
				cperm.append(eaCopy)
				# return a
			for eb in b:
				eaCopy = ea.copy()
				eaCopy.append(eb)
				cperm.append(eaCopy)
		else:
			cperm.append(ea)
	# print (cperm)
	return cperm

def permulteList(list2D):
	outputPerm = None
	for list1D in list2D:
		if outputPerm is None:
			outputPerm = permuteTwo(list1D)
		else:
			outputPerm = permuteTwo(outputPerm,list1D)
	return outputPerm

