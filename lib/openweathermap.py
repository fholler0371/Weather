import time
import threading
import http_async
import json

class c_openweathermap:
	def __init__(self):
		self.valid = False
		self.key =  ''
		self.lat = None
		self.long = None
		self.busy = False
		self.callback_newdata = None
		self.running = False
		self.timer = None
		self.url = "https://api.openweathermap.org/data/2.5/onecall?"
		self.data = {"current":{}, "hourly":{}, "daily": {}}
		self.refresh = 900
		self.error_count = 0

	def start(self):
		self.running = True
		self.loop()

	def stop(self):
		self.running = False
		if not self.timer == None:
			try:
				self.timer.cancel()
			except:
				pass

	def callback(self, value):
		try:
			data = json.loads(value.decode())
			self.data["current"] =  data["current"]
			self.data["hourly"] =  data["hourly"]
			self.data["daily"] =  data["daily"]
			self.valid = True
			if not (self.callback_newdata == None):
				self.callback_newdata()
			timeout = self.refresh
			self.error_count = 0
		except:
			self.error_count += 1
			timeout = 1
			l = 1
			while l < self.error_count:
				l += 1
				timeout *= 2
			timeout *= 60
		self.timer = threading.Timer(timeout, self.loop)
		self.timer.start()

	def loop(self):
		http = http_async.th_http_async(self.url+'lat='+str(self.lat)+'&lon='+str(self.long)+'&exclude=minutely&apikey='+self.key, self.callback)
		http.start()
