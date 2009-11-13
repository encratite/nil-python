import threading

class create_thread(threading.Thread):
	def __init__(self, function, name = None):
		threading.Thread.__init__(self, name = name)
		self.function = function
		self.start()
		
	def run(self):
		self.function()
