import threading

def write(text):
	lock.acquire()
	print text,
	lock.release()
	
def line(text):
	write('%s\n' % text)
	
lock = threading.Lock()
