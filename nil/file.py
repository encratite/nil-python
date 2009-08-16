def write_file(path, data):
	try:
		file = open(path, 'w+b')
		file.write(data)
		file.close()
		return True
	except IOError:
		return None
		
def read_file(path):
	try:
		file = open(path, 'rb')
		output = file.read()
		file.close()
		return output
	except IOError:
		return None
		
def read_lines(path):
	data = read_file(path)
	if data == None:
		return data
	data = data.replace('\r', '')
	data = data.split('\n')
	return data
	
def get_extension(path):
	offset = path.rfind('.')
	if offset == -1:
		return None
	else:
		return path[offset + 1 : ]
		
def append(path, data):
	try:
		file = open(path, 'ab')
		file.write(data)
		file.close()
		return True
	except IOError:
		return None