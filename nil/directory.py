import os, nil.file

def get_list(path):
	entries = sorted(os.listdir(path))
	directories = []
	files = []
	for entry in entries:
		current_path = os.path.join(path, entry)
		if os.path.isdir(current_path):
			directories.append(current_path)
		else:
			files.append(current_path)
	return directories, files
	
def get_files_by_extension(path, extension):
	directories, files = get_list(path)
	return filter(lambda path: nil.file.get_extension(path) == extension, files)