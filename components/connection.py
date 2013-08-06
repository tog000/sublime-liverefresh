"""
Based on code by Brian Thorne 2012
 
"""
from __future__ import print_function
import socket
import logging
import select
import threading
import time
import base64
import hashlib
import sublime
try: import queue
except ImportError:
	try:
		import Queue as queue
	except ImportError:
		print("LiveRefresh cannot start")

class Connection(threading.Thread):

	def __init__(self,socket,debug=False):
		super(Connection, self).__init__()
		self.socket = socket
		self.settings_debug = debug
		self.queue = queue.Queue()

	def run(self):
		
		to_read,to_write,exception = select.select([self.socket],[],[])
		
		for ready_socket in to_read:
			header = self.socket.recv(4096)

			if not header: return;

			# Determine if we want to send file or open websocket
			if header.find(b'GET') == 0 and header.find(b'js') > 0:
				self.serve_file(header)
			else:
				self.start_websocket(header)

	def serve_file(self,header):
		parts = str(header).split(' ')
		if parts[1].find(".js") >= 0: 
			
			filename = parts[1][parts[1].rfind("/")+1:]

			path = "{0}/LiveRefresh/js/{1}".format(sublime.packages_path(),filename)

			with open(path) as f: 
				contents = f.read()
				
			header='''HTTP/1.1 200 OK\r
Content-Type: text/javascript\r
Content-Length: {0}\r

{1}\r
\r
'''.format(len(contents),contents)

			self.socket.send(header.encode('utf_8'))

			self.debug("Connection","Served javascript file: {0}".format(filename))
	

	def start_websocket(self,header):

		self.debug("WebSocket","Initializing WebSocket...")

		if not header:
			self.debug("WebSocket","Client {0} disconnected.".format(self.socket))
			return

		# get to the key
		key = None
		for line in header.splitlines():
			if b'Sec-WebSocket-Key:' in line:
				key = line.split(b': ')[1]
				break
		if key == None:
			return
		response_string = self.calculate_websocket_hash(key)

		header='''HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: {0}\r
\r
'''.format(response_string)

		self.socket.sendall(header.encode())
		self.running = True

		self.debug("WebSocket","Connection established {0}.".format(self.socket))

		while self.running:

			try:

				msg = self.queue.get()

				try:
					self.socket.sendall(self.pack(msg))
				except:
					logging.exception("Catched error. Sending through WebSocket")
					break

			except queue.Empty:
				logging.exception("Catched error. Message queue was empty")
				pass

	def calculate_websocket_hash(self,key):
		magic_websocket_string = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
		result_string = key + magic_websocket_string
		sha1_digest = hashlib.sha1(result_string).digest()
		response_data = base64.encodestring(sha1_digest).strip()
		response_string = response_data.decode('utf8')
		return response_string.strip()

	def is_bit_set(self,int_type, offset):
		mask = 1 << offset
		return not 0 == (int_type & mask)

	def set_bit(self,int_type, offset):
		return int_type | (1 << offset)

	def bytes_to_int(self,data):
		# note big-endian is the standard network byte order
		return int.from_bytes(data, byteorder='big')


	def pack(self,data):
		frame_head = bytearray(2)

		# set final fragment
		frame_head[0] = self.set_bit(frame_head[0], 7)

		# set opcode 1 = text
		frame_head[0] = self.set_bit(frame_head[0], 0)

		# payload length
		assert len(data) < 126, "haven't implemented that yet"
		frame_head[1] = len(data)

		# add data
		frame = frame_head + data.encode('utf-8')
		self.debug("Connection",list(hex(b) for b in frame))
		return frame

	def receive(self,s):
		
		to_read,to_write,exception = select.select([self.request],[],[],0.1)

		if len(to_read)>0:

			# read the first two bytes
			frame_head = s.recv(2)

			# very first bit indicates if this is the final fragment
			self.debug("Connection","final fragment: {0}".format(self.is_bit_set(frame_head[0], 7)))

			# bits 4-7 are the opcode (0x01 -> text)
			self.debug("Connection","opcode: {0}".format(frame_head[0] & 0x0f))

			# mask bit, from client will ALWAYS be 1
			assert self.is_bit_set(frame_head[1], 7)

			# length of payload
			# 7 bits, or 7 bits + 16 bits, or 7 bits + 64 bits
			payload_length = frame_head[1] & 0x7F
			if payload_length == 126:
				raw = s.recv(2)
				payload_length = self.bytes_to_int(raw)
			elif payload_length == 127:
				raw = s.recv(8)
				payload_length = self.bytes_to_int(raw)
			self.debug("WebSocket",'Payload is {0} bytes'.format(payload_length))

			
			masking_key = s.recv(4)
			self.debug("WebSocket","mask: ", masking_key,self.bytes_to_int(masking_key))

			# finally get the payload data:
			masked_data_in = s.recv(payload_length)
			data = bytearray(payload_length)

			# The ith byte is the XOR of byte i of the data with
			# masking_key[i % 4]
			for i, b in enumerate(masked_data_in):
				data[i] = b ^ masking_key[i%4]

			return data

	def debug(self,prefix,msg):
		if self.settings_debug:
			print("[{0}] {1}".format(prefix,msg))