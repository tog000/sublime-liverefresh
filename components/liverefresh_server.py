from __future__ import print_function
import threading
import socket as SocketPkg
import select
import time
from .connection import Connection
import logging
try: import queue
except ImportError:
	try:
		import Queue as queue
	except ImportError:
		print("LiveRefresh cannot start")

class LiveRefreshServer(threading.Thread):

	counter = 0

	def __init__(self,port=9999,debug=False):
		super(LiveRefreshServer, self).__init__()
		self.settings_debug = debug
		self.settings_port = port
		self.active_connections = []

	def run(self):
		self.socket = SocketPkg.socket(SocketPkg.AF_INET, SocketPkg.SOCK_STREAM)
		self.socket.setsockopt(SocketPkg.SOL_SOCKET, SocketPkg.SO_REUSEADDR, 1)
		
		self.socket.bind(('', self.settings_port))
		self.socket.listen(1)

		self.debug("LiveRefresh","Listening for incomming connections...")

		while True:
			try:
				new_socket, addr = self.socket.accept()
				LiveRefreshServer.counter += 1
				new_thread = Connection(new_socket,self.settings_debug)
				new_thread.start()
				self.active_connections.append(new_thread.queue)
			except:
				logging.exception("Catched error while waiting for connections")

	def send_all(self,msg):
		for queue in self.active_connections:
				queue.put_nowait(msg)

	def debug(self,prefix,msg):
		if self.settings_debug:
			print("[{0}] {1}".format(prefix,msg))