from __future__ import absolute_import
import time

def timestamp():
	time_data = time.localtime()
	output = '%d-%02d-%02d %02d:%02d:%02d' % (time_data.tm_year, time_data.tm_mon, time_data.tm_mday, time_data.tm_hour, time_data.tm_min, time_data.tm_sec)
	return output