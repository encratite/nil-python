import os, nil.directory, nil.file

cpp_extension = 'cpp'
object_extension = 'o'

class builder:
	def __init__(self, output):
		self.include_directories = ['.']
		self.source_files = []
		self.libraries = []
		
		self.output_directory = 'output'
		self.object_directory = 'object'
		
		self.output = output
		
		self.source('source')
		
	def include(self, directory):
		self.include_directories.append(directory)
		
	def source(self, directory):
		files = nil.directory.get_files_by_extension(directory, cpp_extension)
		self.source_files += files
		
	def library(self, library):
		self.libraries.append(library)
		
	def make_directory(self, directory):
		try:
			os.mkdir(directory)
		except:
			pass
			
	def get_object(self, path):
		extension = nil.file.get_extension(path)
		if extension == cpp_extension:
			output = path[0 : - len(extension)]
		else:
			output = path
			
		return os.path.join(self.output_directory, os.path.basename(output + object_extension))
		
	def command(self, command_string):
		print 'Executing: %s' % command_string
		return os.system(command_string) == 0
		
	def compile(self):
		self.make_directory(self.output_directory)
		
		include_string = ''
		for directory in self.include_directories:
			include_string += ' -I%s' % directory
			
		object_string = ''
		
		for source, object in self.targets:
			if not self.command('g++ -c %s -o %s%s' % (source, object, include_string)):
				print 'Compilation failed'
				return False
			object_string += ' %s' % object
			
		self.object_string = object_string
			
		return True
		
	def make_targets(self):
		self.targets = map(lambda path: (path, self.get_object(path)), self.source_files)
		
	def get_library_string(self):
		library_string = ''
		for library in self.libraries:
			library_string += ' -L%s' % library
		return library_string
		
	def link_program(self):
		library_string = self.get_library_string()
		
		output_path = os.path.join(self.output_directory, self.output)
		if not self.command('g++ -o %s%s%s' % (output_path, library_string, self.object_string)):
			print 'Failed to link'
			return False

		return True
		
	def make_static_library(self):
		output = os.path.join(self.output_directory, 'lib%s.a%s' % self.output)
		return self.command('ar -rsc %s%s' % (output, self.object_string))
		
	def program(self):
		self.make_targets()
		return self.compile() and self.link_program()

	def static_library(self):
		self.make_targets()
		return self.compile() and self.make_static_library()
