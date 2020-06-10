"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Version 1.0
"""

import http_async
import json
import time
import threading

class c_weatherbit():
	def __init__(self):
		self.valid = False
		self.open = 0
		self.key = ''
		self.lang = 'de'
		self.units = 'M'
		self.country = 'DE'
		self.postal_code = '10178'
		self.refresh = 900
		self.error_count = 0
		self.url = 'https://api.weatherbit.io/v2.0/'
		self.data = {'last' : 0, 'current' : {}, 'alerts': {}, 'forecast' : {}}
		self.running = False
		self.timer = None
		self.busy = False
		self.callback_newdata = None
		self.lat = None
		self.long = None

	def get_params(self):
		if self.lat == None or self.long == None:
			return '?key='+self.key+'&lang='+self.lang+'&units='+self.units+'&postal_code='+self.postal_code+'&country='+self.country
		else:
			return '?key='+self.key+'&lang='+self.lang+'&units='+self.units+'&lat='+str(self.lat)+'&lon='+str(self.long)

	def callback_current(self, value):
		while self.busy:
			time.sleep(0.1)
		self.busy = True
		self.open -= 1
		if value:
			try:
				self.data['current'] = json.loads(value.decode())['data'][0]
			except:
				pass
				print('current json')
				print(value)
		else:
			print('current')
		self.check_all()
		self.busy = False

	def callback_alerts(self, value):
		while self.busy:
			time.sleep(0.1)
		self.busy = True
		self.open -= 1
		if value:
			try:
				self.data['alerts'] = json.loads(value.decode())['alerts']
			except:
				pass
				print('alerts json')
				print(value)
		else:
			print('alerts')
		self.check_all()
		self.busy = False

	def callback_forecast(self, value):
		while self.busy:
			time.sleep(0.1)
		self.busy = True
		self.open -= 1
		if value:
			try:
				self.data['forecast'] = json.loads(value.decode())['data']
			except:
				pass
				print('forecast json')
				print(value)
		else:
			print('forecast')
		self.check_all()
		self.busy = False

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
	def loop(self):
		print("loop")
		if self.open == 0:
			self.open = 3
			http = http_async.th_http_async(self.url+'current'+self.get_params(), self.callback_current)
			http.start()
			http = http_async.th_http_async(self.url+'alerts'+self.get_params(), self.callback_alerts)
			http.start()
			http = http_async.th_http_async(self.url+'forecast/daily'+self.get_params(), self.callback_forecast)
			http.start()

	def check_all(self):
		if self.open == 0:
			if (not self.data['current'] == {}) and (not self.data['alerts'] == {}) and (not self.data['forecast'] == {}):
				self.valid = True
				self.data['last'] = int(time.time())
				self.error_count = 0
				if not self.callback_newdata == None:
					self.callback_newdata()
			else:
				print('error')
				self.error_count = 1 + self.error_count
			if self.running:
				if self.error_count == 0:
					timeout = self.refresh
				else:
					timeout = 1
					l = 1
					while l < self.error_count:
						l += 1
						timeout *= 2
					timeout *= 60
				print(timeout)
				self.timer = threading.Timer(timeout, self.loop)
				self.timer.start()
