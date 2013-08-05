from __future__ import print_function
import threading
import socket as SocketPkg
import select
import time
from .websocket import WebSocket

class LiveRefreshServer(threading.Thread):

	def __init__(self,port=9999,debug=False):
		threading.Thread.__init__(self)
		
		self.active_connections = []
		
		self.settings_debug = debug
		self.settings_port = port


	def shutdown(self):
		if self.is_alive():
			self.debug("LiveRefresh","Shutting down socketection: {0}".format(self))
			self.socket.close()
			self.running = False
			self.join()

	def cleanup_connections(self):

		for thread in self.active_connections:
			if not thread.is_alive():
				self.active_connections.remove(thread)
				self.debug("LiveRefresh","Connection {0} was dead, removing...".format(thread.socket));

	def send_all(self,msg):
		for thread in self.active_connections:
			thread.send(msg)

	def run(self):

		self.running = True
		self.socket = None

		while self.running:

			if self.socket == None:
				self.socket = SocketPkg.socket(SocketPkg.AF_INET, SocketPkg.SOCK_STREAM)
				self.socket.setsockopt(SocketPkg.SOL_SOCKET, SocketPkg.SO_REUSEADDR, 1)
				self.socket.settimeout(30)
				
				self.debug("LiveRefresh","Listening for incomming connections...")
				
				self.socket.bind(('', self.settings_port))
			
			self.socket.listen(1)

			#self.cleanup_connections()

			try:
				socket, addr = self.socket.accept()
			except SocketPkg.timeout:
				if self.running:
					# We just exceeded the timeout on socketects
					continue
				else:
					break # Break out of the while (Server dies)
			except:
				continue # Fail silently (Broken pipe)
			
			self.debug("LiveRefresh","Incoming connection from {0}".format(addr))

			#self.socket.setblocking(0)

			socket_thread = WebSocket(socket,addr, self.settings_debug)
			#socket_thread.setDaemon(True)
			socket_thread.start()

			self.active_connections.append(socket_thread)

	def debug(self,prefix,msg):
		if self.settings_debug:
			print("[{0}] {1}".format(prefix,msg))
