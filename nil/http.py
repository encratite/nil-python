import urllib2

def download(url):
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	data = response.read()
	return data
	
	try:
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		data = response.read()
		return data
	except:
		return None
