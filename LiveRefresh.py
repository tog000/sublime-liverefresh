import sublime, sublime_plugin
import time
from .components.liverefresh_server import LiveRefreshServer

class LiveRefresh(sublime_plugin.EventListener):  

	server_thread = None

	def __init__(self):
		super(LiveRefresh,self).__init__()

	def start_server(self):
		settings = sublime.load_settings('LiveRefresh.sublime-settings')
		port = int(settings.get('port'))
		debug = settings.get('debug') == "True"

		server_thread = LiveRefreshServer(port=port, debug=debug)
		#self.server_thread.setDaemon(True)
		server_thread.start()

		# Assign to a "static" variable (why are callbacks being called on different instance of LiveRefresh?)
		LiveRefresh.server_thread = server_thread

	def on_post_save_async(self, view):
		LiveRefresh.server_thread.send_all("refresh")

def plugin_loaded():
	lr = LiveRefresh()
	lr.start_server()