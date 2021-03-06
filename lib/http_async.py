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
