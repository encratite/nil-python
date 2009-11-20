import threading

def write(text):
	lock.acquire()
	print text
	lock.release()
	
lock = threading.Lock()
