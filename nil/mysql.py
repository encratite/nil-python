import MySQLdb
import threading

class mysql(object):
	def __init__(self):
		self.lock = threading.Lock()
		
	def connect(self, new_host, new_user, new_password, new_database):
		self.connection = MySQLdb.connect(host = new_host, user = new_user, passwd = new_password, db = new_database)
		self.cursor = self.connection.cursor()
		
	def disconnect(self):
		try:
			self.cursor.close()
			self.connection.close()
		except:
			pass
			
	def query(self, query):
		self.lock.acquire()
		try:
			self.cursor.execute(query)
			output = self.cursor.fetchall()
		except:
			self.lock.release()
			return False
		self.connection.commit()
		self.lock.release()
		return output
		
	def insert_id(self):
		return self.connection.insert_id()
		
def escape(input):
	return MySQLdb.escape_string(input)