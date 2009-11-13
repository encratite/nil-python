import sys, os

def is_windows():
	return sys.platform == 'win32'
	
def get_processor_count():
	if is_windows():
		return int(os.environ.get('NUMBER_OF_PROCESSORS', 1))
	else:
		return int(os.sysconf('SC_NPROCESSORS_ONLN'))
