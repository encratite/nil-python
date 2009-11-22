import sys, os, subprocess
import nil.environment, nil.setup

python_version = '2.6'

package = 'nil'

nil.environment.unix_like()
	
if not nil.setup.has_command(['/usr/bin/python%s' % python_version, '-V']):
	print 'Unable to detect Python %s.' % python_version
	sys.exit(1)
	
path = os.path.join(os.path.dirname(nil.environment.get_script_path()), package)
link_name = '/usr/local/lib/python2.6/dist-packages/%s' % package

nil.setup.symlink(path, link_name)
