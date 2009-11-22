from __future__ import absolute_import

import os, time, threading, nil.directory, nil.file, nil.thread, nil.environment, nil.printer

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
		
		self.threads = nil.environment.get_processor_count()
		
		self.source('source')
		
		self.lock = threading.Lock()
		
	def include(self, directory):
		self.include_directories.append(directory)
		
	def source(self, directory):
		files = nil.directory.get_files_by_extension(directory, cpp_extension)
		if files != None:
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
			
		return os.path.join(self.object_directory, os.path.basename(output + object_extension))
		
	def command(self, command_string):
		nil.printer.line('Executing: %s' % command_string)
		return os.system(command_string) == 0
		
	def worker(self):
		while True:
			self.lock.acquire()
			if len(self.targets) == 0 or self.compilation_failed:
				self.lock.release()
				return
			source, object = self.targets[0]
			self.targets = self.targets[1 : ]
			self.lock.release()
			
			name = '%s: ' % threading.currentThread().name
			nil.printer.write(name)
			if not self.command('g++ -c %s -o %s%s' % (source, object, self.include_string)):
				self.lock.acquire()
				if not self.compilation_failed:
					nil.printer.line('Compilation failed')
					self.compilation_failed = True
				self.lock.release()
				return
			
		
	def compile(self):
		self.make_directory(self.object_directory)
		
		self.include_string = ''
		for directory in self.include_directories:
			self.include_string += ' -I%s' % directory
			
		self.object_string = ''
		for source, object in self.targets:
			self.object_string += ' %s' % object
		
		thread_string = 'thread'
		if self.threads > 1:
			thread_string += 's'
			
		print 'Compiling project with %d %s' % (self.threads, thread_string)
		
		self.start = time.time()
			
		threads = []
		self.compilation_failed = False
		counter = 1
		for i in range(0, self.threads):
			thread = nil.thread.create_thread(self.worker, 'Worker %d' % counter)
			threads.append(thread)
			counter += 1
			
		for thread in threads:
			thread.join()
			
		success = not self.compilation_failed
		
		difference = time.time() - self.start		
		if success:
			print 'Compilation finished after %.2f s' % difference
			
		return success
		
	def make_targets(self):
		self.make_directory(self.output_directory)
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
		self.library = 'lib%s.a' % self.output
		output = os.path.join(self.output_directory, self.library)
		try:
			os.unlink(output)
		except OSError:
			pass
		return self.command('ar -cq %s%s' % (output, self.object_string))
		
	def program(self):
		self.make_targets()
		return self.compile() and self.link_program()

	def static_library(self):
		self.make_targets()
		return self.compile() and self.make_static_library()
