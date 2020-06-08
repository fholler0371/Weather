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
import urllib.parse

import time
import threading


class c_opencagedata():
	def __init__(self):
		self.valid = False
		self.url = 'https://api.opencagedata.com/geocode/v1/json'
		self.data = {'components': {}, 'formatted': {}, 'geometry': {}}
		self.key = ''
		self.callback = None

	def forward(self, addr):
		q = urllib.parse.quote_plus(addr)
		self.data = {'components': {}, 'formatted': {}, 'geometry': {}}
		http = http_async.th_http_async(self.url+'?key='+self.key+'&limit=1&q='+q, self.callback_http)
		http.start()

	def callback_http(self, value):
		if value:
			try:
				self.data['components'] = json.loads(value.decode())['results'][0]['components']
				self.data['formatted'] = json.loads(value.decode())['results'][0]['formatted']
				self.data['geometry'] = json.loads(value.decode())['results'][0]['geometry']
				self.valid = True
			except:
				self.valid = False
		else:
			self.valid = False
		if not self.callback == None:
			self.callback()
