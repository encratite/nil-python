import subprocess, os

def has_command(arguments):
	try:
		process = subprocess.Popen(arguments, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		process.wait()
		return True
	except OSError:
		return False
		
def run(arguments):
	try:
		process = subprocess.Popen(arguments, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		process.wait()
		return process.returncode == 0
	except OSError:
		return None
		
def command(input):
	print 'Executing %s' % input
	return os.system(input) != 0

def symlink(target, link_name):
	if os.path.exists(link_name):
		return True
		
	#print 'Creating a symlink to %s at %s' % (target, link_name)
	return command('sudo ln -s %s %s' % (target, link_name))

def install_packages(packages):
	apt = 'apt-get'
	if has_command(apt):
		for package in packages:
			result = run(['dpkg',  '-s',  package])
			if result == None:
				print 'Failed to execute package manager'
				sys.exit(1)
			if not result:
				print 'Installing missing package %s' % package
				os.system('sudo apt-get install %s' % package)
	else:
		print 'Unable to install the specified packages (%s) - only Ubuntu and Debian are currently supported.' % packages
		return False
