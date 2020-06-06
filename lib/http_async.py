from threading import Thread
import requests

class th_http_async(Thread):
	def __init__(self, url, callback = None):
		Thread.__init__(self)
		self.name = "http_async"
		self.url = url
		self.cb = callback

	def run(self):
		try:
			r = requests.get(self.url)
			if not None == self.cb:
				if r.status_code == 200:
					self.cb(r.content)
				else:
					self.cb(False)
		except:
			if not None == self.cb:
				self.cb(False)
