import subprocess, os

def has_command(arguments):
	try:
		process = subprocess.Popen(arguments, bufsize = 0, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		process.wait()
		return process.returncode == 0
	except OSError:
		return False
		
def command(input):
	print 'Executing %s' % input
	return os.system(input) != 0

def symlink(target, link_name):
	if os.path.exists(target):
		return
		
	command('sudo ln -s %s %s' % (target, link_name))
