def extract_all(input, left, right):
	i = 1
	output = []
	while True:
		element = extract_string(input, left, right, i)
		if element == None:
			break
		output.append(element)
		i += 1
	return output

def extract_string(input, left, right, occurence = 1):
	offset = 0
	for i in range(0, occurence):
		offset = input.find(left, offset)
		if offset == -1:
			return None
		offset += len(left)
	offset2 = input.find(right, offset)
	if offset2 == -1:
		return None
	return input[offset : offset2]
	
def extract_strings(input, patterns):
	output = []
	offset = 0
	while True:
		current_output = []
		for left, right in patterns:
			offset = input.find(left, offset)
			if offset == -1:
				return output
			offset += len(left)
			end_offset = input.find(right, offset)
			if end_offset == -1:
				return output
			string = input[offset : end_offset]
			current_output.append(string)
			offset = end_offset + len(right)
		output.append(current_output)
	return output
	
def consolify_string(input):
	output = ''
	lower_limit = ord(' ')
	upper_limit = ord('~')
	for i in input:
		current_value = ord(i)
		if current_value < lower_limit or current_value > upper_limit:
			output += '\\x%02x' % ord(i)
		else:
			output += i
	return output