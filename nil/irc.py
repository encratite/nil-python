from __future__ import absolute_import
import socket, random, time, nil.thread

colon = ':'
delimiter = ' '

def do_nothing(*arguments):
	pass
	
def strip_tags(input):
	output = ''	
	
	i = 0
	last_index = len(input) - 1
	while i <= last_index:
		current_char = input[i]
		if ord(current_char) < ord(' '):
			if current_char == '\x03' and last_index - i >= 2:
				next_char = input[i + 1]
				next_char_value = ord(next_char)
				if next_char == '1':
					i += 1
					second_digit = ord(input[i + 1])
					if second_digit >= ord('0') and second_digit <= ord('5'):
						i += 1
				elif next_char == '0':
					i += 2
				elif next_char_value >= ord('2') and next_char_value <= ord('9'):
					i += 1
		else:
			output += current_char
		i += 1
	return output
	
class irc_user:
	def __init__(self, input):
		self.raw = input
		self.error = False
		
		tokens = input[1 : ].split('!')
		if len(tokens) != 2:
			self.error = True
			return
		
		self.nick = tokens[0]
		
		tokens = tokens[1].split('@')
		if len(tokens) != 2:
			self.error = True
			return
			
		self.ident = tokens[0]
		self.address = tokens[1]

class irc_client:
	def __init__(self):
		self.on_raw_packet = do_nothing
		self.on_failed_connect = do_nothing
		self.on_connect = do_nothing
		self.on_disconnect = do_nothing
		self.on_entry = do_nothing
		self.on_notice = do_nothing
		self.on_join = do_nothing
		self.on_invite = do_nothing
		self.on_channel_message = do_nothing
		self.on_private_message = do_nothing
		self.on_nick_name_in_use = self.change_nick
		self.on_quit = do_nothing
		
		self.auto_reconnect = True
		self.auto_reconnect_delay = 5
		self.read_size = 1024
		self.last_line = None
		self.timeout = 600
		
		self.nick_change_delay = 5
		
		self.ping_counter = 0
		self.maximum_ping_count = None
		
		nil.thread.create_thread(lambda: self.timeout_thread())
		
	def timeout_thread(self):
		while True:
			if self.last_line != None and time.time() - self.last_line > self.timeout:
				print 'Timeout occured'
				nil.thread.create_thread(lambda: self.perform_reconnect())
				time.sleep(self.auto_reconnect_delay)
				continue
			time.sleep(1)
		
	def connect(self, server, port, nick, user, local_host, real_name):
		self.server = server
		self.port = port
		self.nick = nick
		self.user = user
		self.local_host = local_host
		self.real_name = real_name
		
		while True:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			try:
				self.socket.connect((server, port))
				self.on_connect()
				break
			except:
				self.on_failed_connect()
				if self.auto_reconnect:
					time.sleep(self.auto_reconnect_delay)
				else:
					return
					
		self.send_line('NICK %s' % nick)
		self.send_line('USER %s "%s" "%s" :%s' % (user, local_host, server, real_name))
		self.receive_data()
		
	def reconnect(self):
		self.connect(self.server, self.port, self.nick, self.user, self.local_host, self.real_name)
		
	def send_line(self, line):
		self.socket.send('%s\r\n' % line)
		
	def join(self, channel):
		self.send_line('JOIN %s' % channel)
		
	def message(self, target, message):
		self.send_line('PRIVMSG %s :%s' % (target, message))
		
	def got_disconnected(self):
		self.on_disconnect()
		time.sleep(self.auto_reconnect_delay)
		self.reconnect()
		
	def perform_reconnect(self):
		try:
			self.socket.close()
		except IOError:
			pass
		self.got_disconnected()
		
	def receive_data(self):
		self.buffer = ''
		while True:
			try:
				new_data = self.socket.recv(self.read_size)
				self.last_line = time.time()
			except IOError:
				self.perform_reconnect()
				return
			if len(new_data) == 0:
				self.perform_reconnect()
				return
			self.buffer += new_data
			self.process_new_data()
			
	def process_new_data(self):
		while True:
			offset = self.buffer.find('\n')
			if offset == -1:
				break
			line = self.buffer[0 : offset].replace('\r', '')
			self.buffer = self.buffer[offset + 1 : ]
			self.process_line(line)
			
	def process_line(self, line):
		self.on_raw_packet(line)
		
		if len(line) == 0:
			return
		offset = line.find(colon, 1)
		if offset == -1:
			tokens = line.split(delimiter)
		else:
			tokens = line[0 : offset - 1].split(delimiter)
			tokens.append(line[offset + 1 : ])
			
		self.process_command(tokens)
		
	def process_command(self, tokens):
		commands = [
			('376', self.event_end_of_motd),
			('422', self.event_end_of_motd),
			('433', self.event_nick_name_in_use),
			('NOTICE', self.event_notice),
			('INVITE', self.event_invite),
			('JOIN', self.event_join),
			('PRIVMSG', self.event_message),
			('MODE', self.event_mode),
			('QUIT', self.event_quit)
		]
		
		if tokens[0] == 'PING' and len(tokens) == 2:
			self.send_line('PONG %s' % tokens[1])
			self.ping_counter += 1
			if self.maximum_ping_count != None and self.ping_counter >= self.maximum_ping_count:
				print 'Exceeded maximum ping count, reconnecting'
				self.perform_reconnect()
			return
			
		if len(tokens) < 3:
			return
			
		self.ping_counter = 0
			
		for command, function in commands:
			if command == tokens[1]:
				function(tokens)
				break
				
	def nick(self, new_nick):
		self.send_line('NICK %s' % new_nick)
				
	def change_nick(self):
		new_nick = '%s%d' % (self.nick, random.randint(10, 99))
		self.nick(new_nick)
				
	def event_end_of_motd(self, tokens):
		actual_nick = tokens[2]
		if actual_nick != self.nick:
			print 'Somebody else is using our nick, trying to reclaim it'
			self.desired_nick = self.nick
			self.nick = actual_nick
			nil.thread.create_thread(self.reclaim_nick)
		else:
			self.nick = actual_nick
		self.on_entry()
		
	def reclaim_nick(self):
		while True:
			if self.nick == self.desired_nick:
				print 'Successfully reclaimed our nick'
				break
			self.change_nick(self.desired_nick)
			time.sleep(self.nick_change_delay)
		
	def event_nick_name_in_use(self, tokens):
		self.on_nick_name_in_use()
		
	def event_notice(self, tokens):
		user = irc_user(tokens[0])
		if user.error:
			return
		text = tokens[-1]
		self.on_notice(user, text)
		
	def event_invite(self, tokens):
		user = irc_user(tokens[0])
		if user.error:
			return
		channel = tokens[-1]
		self.on_invite(user, channel)
		
	def event_join(self, tokens):
		user = irc_user(tokens[0])
		if user.error:
			return
		own_join = (user.nick == self.nick)
		channel = tokens[-1]
		self.on_join(channel, user, own_join)
		
	def event_message(self, tokens):
		user = irc_user(tokens[0])
		if user.error:
			return
		target = tokens[2]
		message = tokens[-1]
		if target == self.nick:
			self.on_private_message(user, message)
		else:
			self.on_channel_message(target, user, message)
			
	def event_mode(self, tokens):
		pass
		
	def event_quit(self, tokens):
		user = irc_user(tokens[0])
		if user.error:
			return
		message = tokens[-1]
		self.on_quit(user, message)
