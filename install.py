import sys, os, subprocess
import nil.environment

python_version = '2.6'

def command(input):
	print 'Executing %s' % input
	return os.system(input) != 0

package = 'nil'

if nil.environment.is_windows():
	print 'This script is intended to be used with Linux only.'
	sys.exit(1)
	
if not nil.environment.has_command(['/usr/bin/python%s' % python_version, '-V']):
	print 'Unable to detect Python %s.' % python_version
	sys.exit(2)
	
path = os.path.join(os.path.dirname(nil.environment.get_script_path()), package)

command('sudo ln -s %s /usr/local/lib/python2.6/dist-packages/%s' % (path, package))
