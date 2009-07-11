import threading

class create_thread(threading.Thread):
	def __init__(self, function):
		threading.Thread.__init__(self)
		self.function = function
		self.start()
		
	def run():
		self.function()