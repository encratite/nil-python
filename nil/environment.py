import sys, os, subprocess

def is_windows():
	return sys.platform == 'win32'
	
def get_processor_count():
	if is_windows():
		return int(os.environ.get('NUMBER_OF_PROCESSORS', 1))
	else:
		return int(os.sysconf('SC_NPROCESSORS_ONLN'))

def get_script_path():
	return os.path.join(os.getcwd(), sys.argv[0])

def has_command(arguments):
	try:
		process = subprocess.Popen(arguments, bufsize = 0, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		process.wait()
		return process.returncode == 0
	except OSError:
		return False
