import urllib.request

def getImage(url,name,verbose=False):
	done = False
	name = name.replace(" ","_")
	if verbose: print ("Downloading!!", url,"as",name)
	for i in range(5):
		try:
			urllib.request.urlretrieve(url, name)
			done = True
		except:
			print ("Error Downloading!!", url,"as",name)
			continue
		break
	return done