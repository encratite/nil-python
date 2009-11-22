import sys, os

def is_windows():
	return sys.platform == 'win32'
	
def get_processor_count():
	if is_windows():
		return int(os.environ.get('NUMBER_OF_PROCESSORS', 1))
	else:
		return int(os.sysconf('SC_NPROCESSORS_ONLN'))

def get_script_path():
	return os.path.join(os.getcwd(), sys.argv[0])

def unix_like():
	if is_windows():
		print 'This script is intended to be used with UNIX-like operating systems (Linux, BSD, etc.) only.'
		sys.exit(1)
